from outputstyle import *  # used for printing colored and bold text
import database as db  # used to access local database
import re
import emojis
import pandas as pd  # used for dataframe
from PIL import Image
import numpy as np
from textblob_de import TextBlobDE
from wordcloud import WordCloud
from nltk.corpus import stopwords
stopset = stopwords.words("german")
from fpdf import FPDF
import matplotlib.pyplot as plt



def off(*args) -> None:
	"""
	Prints error message and safely exits the program
	"""
	exit(BOLD(RED("Error: ")) + " ".join(args))


def export(location: str, data, name:str) -> None:
	path = f"data/testing/exports/{location}/"
	try:
		if name.endswith(".csv"):
			data.to_csv(path + name, index=True)
		elif name.endswith(".txt"):
			with open(path + name, "w") as textfile:
				textfile.write(str(data))
	except FileNotFoundError:
		import os
		os.makedirs(path, exist_ok=True)
		export(location, data, name)

def db_export() -> None:
	"""
	Exports the database to a .csv file
	"""
	export("database", db.chat, "chat_df.csv")
	export("database", db.cstats_df, "cstats_df.csv")
	export("database", pd.DataFrame(db.senders), "senders_df.csv")
	# cwords_df.to_csv("data/testing/exports/database/cwords_df.csv", index=True)

def fileformat(path_to_file: str) -> str:
	"""
	Checks if the fileformat is correct and returns correct path
	"""
	if path_to_file.endswith(".txt"):
		return path_to_file
	elif path_to_file.endswith(".zip"):
		from zipfile import ZipFile
		with ZipFile(path_to_file, "r") as zip_ref:
			zip_ref.extractall("data")
		return "data/_chat.txt"
	else:
		off("Only .txt or .zip files are supported")


def new_message(input_line: str) -> bool:
	"""
	Checks if the input is the beginning of a new message (date in front) or not
	"""
	if re.match("^.? ?\[([\d./]*), ([\d:]*)\] ([\w ]*)", input_line):
		return True  # the beginning of a new message
	return False  # continuation of the previous message


def convert_line(input: str) -> list[str]:
	"""
	Converts a WA chat history line into a list with these entries:
	datetime, sender, message, polarity, emojis_unique, emoji_count, url_count
	"""
	# match pattern and devide into groups: 1:date, 2:time, 3:sender, 4:message
	x = re.search("^.? ?\[([\d./]*), ([\d:]*)\] ([\w ]*): (\u200E?.*)$", input)
	result = [" ".join([x.group(1), x.group(2)])]  # combine date and time
	result.append(x.group(3).title())  # capitalize first letters of sender
	message = re.sub("https?://\S+", "xURL", x.group(4))  # replace URLs
	result.append(message)  # add message
	result.append(TextBlobDE(message).polarity)  # add emojis
	result.append(emojis.get(message))  # get set of unique emoji in message
	result.append(emojis.count(message))  # count amount of emoji in message
	result.append(len(re.findall("xURL", message)))  # count URLs
	return result


def convert_to_list(path_to_file: str) -> list[list[str]]:
	"""
	Converts a .txt-file of messages into a list of lists: Each list element contains 
	these elements: [datetime, sender, message, polarity, emojis, emoji_count, url_count]
	"""
	chat_listed, last_message = list(), str()
	try:  # try to open the file
		with open(path_to_file, "r", encoding="utf-8") as file:
			for line in file:  # read line by line
				if new_message(line):  # the line is the beginning of a new message
					if last_message != "":  # buffer is not empty
						# add previous message to list
						chat_listed.append(convert_line(last_message))
					last_message = line.strip().strip("\n").strip()  # add new message to buffer
				else:  # the line is a continuation of the previous message
					# add line to previous message
					last_message += " " + line.strip().strip("\n").strip()
			# the last message is not added to the list
			if chat_listed[-1] != convert_line(last_message):
				# add last message to list
				chat_listed.append(convert_line(last_message))
	except FileNotFoundError:  # the file does not exist
		off("File not found")
	except (UnicodeDecodeError, UnicodeError):  # the file is not in UTF-8
		off("File not in UTF-8 format\nTry again or upload the",GREEN("original .zip file"))
	return chat_listed


def convert_to_df(path: str) -> pd.DataFrame:
	"""
	Converts a list of lists into a dataframe with the following columns:
	[datetime, sender, message, polarity, emojis, emoji_count, url_count] and returns it
	"""
	chat_listed = convert_to_list(path)
	df = pd.DataFrame(chat_listed, columns=db.df_cols)
	df["datetime"] = pd.to_datetime(df["datetime"])

	export("myfuncs/convert_to_df", df, "df_converted.csv")
	return df


def cleanse_df(dataframe: pd.DataFrame, sender: str) -> pd.DataFrame:
	"""
	Cleans the dataframe of non-message enties and replaces URLs and enters 
	collected data into the stats dataframe
	"""
	count = 0  # counter for media messages cleaned
	df = dataframe.copy()
	for key, val in db.cstats_match.items():
		if key != "media_count":
			key_df = df[df == val[1]] if val[0] == "exact" else df[df.str.contains(val[1])]
			df = df.drop(key_df.index)  # remove non-messages from clean_df
			db.chat = db.chat.drop(key_df.index) # remove non-messages from chat_df
			if key in db.cstats_df.columns:  # add counted data to cstats_df.if it exists
				db.cstats_df.at[sender, key] = key_df.shape[0]
				count += key_df.shape[0]
		else:  # media messages are counted separately
			db.cstats_df.at[sender, key] = count
	
	export("myfuncs/cleanse_df", df, f"df_clean_{sender}.csv")
	return df.rename(sender)  # return the cleaned dataframe


def calc_stats(sender_df: pd.DataFrame) -> pd.DataFrame:
	"""
	Calculates different statistics about the chat and enters collected data 
	into the stats dataframe
	"""
	s = sender_df.name # get column name (sender)
	db.cstats_df.at[s,"msg_count"] = sender_df.shape[0]
	db.cstats_df.at[s,"chars_avg"] = round(sender_df.str.replace(" ", "").str.len().mean(), 1)
	db.cstats_df.at[s,"words_avg"] = round(sender_df.str.split().str.len().mean(), 1)
	db.cstats_df.at[s,"chars_max"] = sender_df.str.replace(" ", "").str.len().max()
	db.cstats_df.at[s,"words_max"] = len(sender_df[sender_df.str.len().idxmax()].split())
	db.cstats_df.at[s,"link"] = db.chat.loc[db.chat["sender"] == s, "url_count"].sum()
	db.cstats_df.at[s,"emoji"] = db.chat.loc[db.chat["sender"] == s, "emoji_count"].sum()
	emoji_set = set().union(*list(db.chat.loc[db.chat["sender"] == s, "emojis"]))
	db.cstats_df.at[s,"emoji_unique"] = (len(emoji_set), emoji_set)
	db.cstats_df.at[s,"polarity_avg"] = round(db.chat.loc[db.chat["sender"] == s, "polarity"].mean(), 1)
	
	export("myfuncs/calc_stats", db.cstats_df, f"cstats_df_{s}.csv")
	return sender_df


def get_sum_stats() -> None:
	"""
	Calculates summary statistics about the chat and enters collected data
	into the stats dataframe
	"""
	for stat in db.stats_dict.keys():
		if "max" in stat or "unique" in stat or "missed" in stat:
			continue
		elif "avg" in stat:
			db.cstats_df.at["sum", stat] = round(db.cstats_df[stat].mean(), 1)
		else:
			db.cstats_df.at["sum", stat] = db.cstats_df[stat].sum()
	
	export("myfuncs/get_sum_stats", db.cstats_df, "cstats_df.csv")
	return


# ----------------------------------------------------------------
#                          word statistics
# ----------------------------------------------------------------

def word_cloud(words: str, name: str) -> None:
	"""
	Creates a word cloud of the given words and saves it to the plots folder
	"""
	wc = WordCloud(background_color="white", colormap="summer",  scale=2, stopwords=stopset)
	plt.imshow(wc.generate(words), interpolation="bilinear")
	plt.title(f"{name} message word cloud:", fontsize=17)
	plt.axis("off")
	n = name.lower().replace(" ", "")
	plt.savefig(f"data/output/plots/{n}", dpi=300, bbox_inches="tight", pad_inches=0)
	plt.close()
	return


def calc_word_stats(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Calculates different statistics about the chat and enters collected data
	"""
	# get all words in the chat
	words_str = " ".join(df.str.replace("\W", " ", regex=True).str.replace("xURL", " "))
	word_cloud(words_str, df.name)
	word_freq = pd.Series(words_str.lower().split()).value_counts().rename(df.name+ " common words")

	export("myfuncs/calc_word_stats", word_freq, f"common_words{df.name}.csv")
	return word_freq


# --------------------------------------------
# Functions used to print the ouptut in a specific format
# --------------------------------------------


def say(*args) -> str:
	"""
	Returns a bold printed string of strings/numbers which are divided with 
	spaces, commas and the word "and"
	"""
	listing = str()
	for i, arg in enumerate(args):
		if i != 0:
			listing += ", " if i+1 < len(args) else " and "
	listing += BOLD(str(arg))
	return listing


def calc_numerus(amount: int, term: str) -> str:
	"""
	Returns the correct plural form of a word depending on the amount passed
	"""
	if term not in ("media", "polarity"): # special cases
		if amount > 1: # if more than one, add an "s"
			return str(amount) + " " + term + "s"
		return "one " if amount == 1 else "not a single " + term
	return str(amount) + " " + term


def get_stat_pair(stat_idx: int, sender_idx: int) -> tuple[int, str]:
	"""
	Returns the value and term of a specific statistic.
	"""
	return db.cstats_df.iat[sender_idx, stat_idx], list(db.stats_dict.keys())[stat_idx]


def get_reports() -> list[str]:
	"""
	Creates a report about the sender at the given index which includes the 
	statistics about their messages or a summary report and returns it.
	"""
	reports_list, i = list(), int()
	def y(*indices): return say(*[calc_numerus(*get_stat_pair(x, i)) for x in indices])

	for s in db.senders: # for each sender create a sender report
		sl = [GREEN(f"\t{say(s)} report:"),
			f"{s} sent {y(0,6,18)} in this chat.",
			f"The average length of a message is {y(1,2)}.",
			f"The longest message {s} sent contained {y(3,4)}.",
			f"{s} sent {y(11,7,8,10,9)}",
			f"and shared {y(12,13,14,17)}",
			f"{y(15)} were deleted by {s} in this chat."]
		if db.cstats_df.at[s, list(db.stats_dict.keys())[16]] > 0:
			sl.append(f"You missed {y(16)} by {s}.")
		reports_list.append("\n\t".join(sl)) # add report to list
	
	# General report about the chat
	i = len(db.senders)
	sl = [GREEN(f"\tThis WA Chat was between {say(*db.senders)}:"),
		f"Their chat contained {y(0,6,18)}.",
		f"The average legth of a message is {y(1,2)}.",
		f"The {say(f'{i} senders')} sent {y(11,7,8,10,9)},",
		f"they shared {y(12,13,14,17)}",
		f"and deleted {y(15)} in this chat."]
	reports_list.append("\n\t".join(sl)) # add report to the list
	
	export("myfuncs/get_reports", "\n\n".join(reports_list), "reports.txt")
	return reports_list




# --------------------------------------------
#		Functions used to create pdf ouptut
# --------------------------------------------


def print_df_to_pdf(pdf: FPDF, df: pd.DataFrame, cell_width: int = 25, cell_height: int = 6) -> None:
	"""
	Prints a dataframe to a table in a pdf file
	"""
	pdf.set_font("Arial", "B", 10)
	for col in df.columns:	# Loop over to print column names
		pdf.cell(cell_width, cell_height, col, align="C", border=1)
	pdf.ln(cell_height) # next row of table

	pdf.set_font("Arial", "", 8)
	for row in df.itertuples():	# Loop over to print each data in the table
		for col in df.columns:
			value = str(getattr(row, col))
			pdf.cell(cell_width, cell_height, value, align="C", border=1)
		pdf.ln(cell_height) # next row of table


def new_page(pdf: FPDF) -> None:
	"""
	Adds a new page to the pdf file
	"""
	pdf.set_y(-15)
	pdf.set_font("Arial", "I", 8)
	pdf.cell(0, 10, f"Page {pdf.page_no()}", 0, 0, "R")
	pdf.add_page()


def create_pdf_report() -> None:
	"""
	Creates a pdf file with a summary of the chat and the statistics of each sender
	"""
	pdf = FPDF()
	title, subtitle, text = pdf.set_font("Arial", "B", 16), pdf.set_font("Arial", "B", 12), pdf.set_font("Arial", "", 8)

	reports = get_reports()  # get general sender stats for the chat
	pdf.set_auto_page_break(auto=True, margin = 4)
	pdf.add_page()
	title; pdf.cell(40, 10, "WhatsApp Chat Statistics", align="C")
	pdf.ln(10)
	text; pdf.multi_cell(0, 0, reports[len(db.senders)], align="L")

	for i, s in enumerate(db.senders):
		new_page(pdf)
		title; pdf.cell(40, 10, f"{s} WhatsApp Chat Statistics", align="C")
		pdf.ln(10)
		n = s.lower().replace(" ", "")
		pdf.image(f"data/output/plots/{n}.png")
		pdf.ln(10)
		text, pdf.multi_cell(0, 0, reports[i], align="L")


	pdf.output("data/output/pdfs/pdf_report.pdf", "F") # create pdf file