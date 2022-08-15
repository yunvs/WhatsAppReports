from timeit import default_timer as timer
ts = [timer()]

from outputstyle import *
import database as db  # used to access local database
import numpy as np, pandas as pd
import re
import emojis
from wordcloud import WordCloud
from matplotlib import pyplot as plt, cm
from plotly import express as px
from fpdf import FPDF

# from germansentiment import SentimentModel
# model = SentimentModel()

def time(task: str="untitled") -> None:
	"""
	Adds a new entry to the time dataframe.
	"""
	ts.append(timer())
	if task == "end":
		print(BOLD(BLUE("main.py"), "took", ts[-1] - ts[0], f"seconds to complete (minus imports {ts[-1] - ts[1]} seconds)"))
		print(BLUE(pd.concat([db.tt, pd.DataFrame([["- -", "- -"], ["## main.py ##", ts[-1] - ts[0]], ["- imports", ts[-1] - ts[1]]])])))
		return
	db.tt.loc[len(db.tt)] = [task, ts[-1] - ts[-2]]
	print(BLUE(task) + " compleded in " + BOLD(ts[-1] - ts[-2], "sec."))


db.tt = pd.DataFrame(columns=[0, 1])
time("imports")

def off(*args, file_end: bool=False) -> None:
	"""
	Prints error message and safely exits the program.
	"""
	return exit(BOLD(RED("⛔️ Error: ")) + " ".join(args) + " ⛔️" if len(args) > 0 else "") if not file_end else time("end")


def export(location: str=None, data=None, name: str=None, database: bool=False) -> None:
	"""
	Exports dataframes and text to the data/testing/exports folder.
	"""
	if not database:
		path = f"data/testing/exports/{location}/"
		try:
			if name.endswith(".csv"):
				return data.to_csv(path + name, index=True)
			elif name.endswith(".txt"):
				with open(path + name, "w") as textfile:
					textfile.write(str(data))
		except FileNotFoundError:
			import os
			os.makedirs(path, exist_ok=True)
			return export(location, data, name)
	else:
		export("database", db.chat, "chat_df.csv")
		export("database", db.stats_df, "stats_df.csv")
		export("database", pd.DataFrame(db.senders), "senders_df.csv")
		export("database", db.chat_og, "chat_og.csv")
		time("database exports")


def fileformat(path_to_file: str) -> str:
	"""
	Checks if the fileformat is correct and returns correct path.
	"""
	if path_to_file.endswith(".txt"):
		return path_to_file
	elif path_to_file.endswith(".zip"):
		from zipfile import ZipFile
		with ZipFile(path_to_file, "r") as zip_ref:
			zip_ref.extractall("data")
		return "data/_chat.txt"
	else:
		return off("Only .txt or .zip files are supported")


def new_msg(input: str) -> bool:
	"""
	Returns true if the input is the beginning of a new message (date in front).
	"""
	return True if re.match("^.? ?\[([\d./]*), ([\d:]*)\] .*", input) else False


def convert_ln(input: str) -> list[str]:
	"""
	Converts a WA chat history line into a list with these entries:
	date, time, sender, message, polarity, emojis_unique, emoji_count, url_count.
	"""
	# match pattern and devide into groups: 1:date, 2:time, 3:sender, 4:message
	x = re.search("^.? ?\[([\d./]*), ([\d:]*)\] ([\w ]*): (\u200E?.*)$", input)
	result = [x.group(1), " ".join([x.group(1), x.group(2)])]  # add date and time
	result.append(x.group(3).title())  # capitalize first letters of sender
	message = re.sub("https?://\S+", "xURL", x.group(4))  # replace URLs
	result.append(message)  # add message
	result.append("polarity")
	result.append(emojis.get(message))  # get set of unique emoji in message
	result.append(emojis.count(message))  # count amount of emoji in message
	result.append(len(re.findall("xURL", message)))  # count URLs
	return result


def convert_to_list(path_to_file: str) -> list[list[str]]:
	"""
	Converts a .txt-file of messages into a list of lists: Each list element contains these elements: [date, time, sender, message, polarity, emojis, emoji_count, url_count].
	"""
	chat_ls, last_msg = list(), str()
	try:  # try to open the file
		with open(path_to_file, "r", encoding="utf-8") as file:
			for line in file:  # read line by line
				if new_msg(line):  # the line is the beginning of a new message
					# add previous message to list if buffer is not empty
					chat_ls.append(convert_ln(last_msg)) if last_msg != "" else None
					last_msg = line.strip().strip("\n").strip()  # add new message to buffer
				else:  # the line is a continuation of the previous message
					# add line to previous message
					last_msg += " " + line.strip().strip("\n").strip()
			# add last message to list if it is not added yet
			chat_ls.append(convert_ln(last_msg)) if chat_ls[-1] != convert_ln(last_msg) else None
	except FileNotFoundError:  # the file does not exist
		return off("File not found")
	except (UnicodeDecodeError, UnicodeError):  # the file is not in UTF-8
		return off("File not in UTF-8 format\nTry again or upload the",GREEN("original .zip file"))
	
	time(".txt file -> list")
	return chat_ls


# def calc_polarity(df: pd.DataFrame, s: int) -> float:
# 	pol = 0

# 	for i in range(len(df)):
# 		sentence_sentiment = model.model.predict_sentiment(df.iloc[i, 4])
# 		if sentence_sentiment == "positive":
# 			pol += 1
# 		elif sentence_sentiment == "negative":
# 			pol -= 1
# 		else:
# 			pol = pol
		
# 	time(f"calc polarity for sender {s}")
# 	return pol / len(df)


def convert_to_df(path: str) -> pd.DataFrame:
	"""
	Converts a list of lists into a dataframe with the following columns:
	[date, time, sender, message, polarity, emojis, emoji_count, url_count] and returns it.
	"""
	chat_listed = convert_to_list(path)
	df = pd.DataFrame(chat_listed, columns=db.df_cols)
	df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)
	db.chat = df
	db.chat_og = db.chat.copy() # Creates copy for later using
	db.senders = list(db.chat["sender"].unique())

	export("myfuncs/convert_to_df", df, "df_converted.csv")
	time("list -> df")
	return


def cleanse_df(dataframe: pd.DataFrame, sender: str) -> pd.DataFrame:
	"""
	Cleans the dataframe of non-message enties and replaces URLs and enters 
	collected data into the stats dataframe.
	"""
	count = 0  # counter for media messages cleaned
	df = dataframe.copy().rename(sender)
	for key, val in db.cstats_match.items():
		if key == "media_count": # media messages are counted separately
			db.stats_df.at[sender, key] = count
		else:
			key_df = df[df == val[1]] if val[0] == "exact" else df[df.str.contains(val[1])]
			df = df.drop(key_df.index)  # remove non-messages from clean_df
			db.chat = db.chat.drop(key_df.index) # remove non-messages from chat_df
			if key in db.stats_df.columns:  # add counted data to stats_df.if it exists
				db.stats_df.at[sender, key] = key_df.shape[0]
				count += key_df.shape[0]
	
	# export("myfuncs/cleanse_df", df, f"df_clean_{sender}.csv")
	time(f"cleaning df for {db.senders.index(sender)+1}")

	# db.stats_df.at[sender, "polarity_avg"] = calc_polarity(df, db.senders.index(sender)+1)
	return df  # return the cleaned dataframe


def calc_stats(sender_df: pd.DataFrame) -> pd.DataFrame:
	"""
	Calculates different statistics about the chat and enters collected data 
	into the stats dataframe.
	"""
	s = sender_df.name # get column name (sender)
	db.stats_df.at[s,"msg_count"] = sender_df.shape[0]
	db.stats_df.at[s,"chars_avg"] = round(sender_df.str.replace(" ", "").str.len().mean(), 1)
	db.stats_df.at[s,"words_avg"] = round(sender_df.str.split().str.len().mean(), 1)
	db.stats_df.at[s,"chars_max"] = sender_df.str.replace(" ", "").str.len().max()
	db.stats_df.at[s,"words_max"] = len(sender_df[sender_df.str.len().idxmax()].split())
	db.stats_df.at[s,"link"] = db.chat.loc[db.chat["sender"] == s, "url_count"].sum()
	db.stats_df.at[s,"emoji"] = db.chat.loc[db.chat["sender"] == s, "emoji_count"].sum()
	emoji_set = set().union(*list(db.chat.loc[db.chat["sender"] == s, "emojis"]))
	db.stats_df.at[s,"emoji_unique"] = (len(emoji_set), emoji_set)
	# db.stats_df.at[s,"polarity_avg"] = round(db.chat.loc[db.chat["sender"] == s, "polarity"].mean(), 1)
	
	# export("myfuncs/calc_stats", db.stats_df, f"stats_df_{s}.csv")
	time(f"calc stats for sender {db.senders.index(s)+1}")
	return sender_df


def calc_sum_stats() -> None:
	"""
	Calculates summary statistics about the chat and enters collected data
	into the stats dataframe.
	"""
	for stat in db.stats_dict.keys():
		if "max" in stat or "unique" in stat or "calls" in stat:
			continue
		elif "avg" in stat:
			db.stats_df.at["sum", stat] = round(db.stats_df[stat].mean(), 1)
		else:
			db.stats_df.at["sum", stat] = db.stats_df[stat].sum()
	
	# export("myfuncs/get_sum_stats", db.stats_df, "stats_df.csv")
	return time("calc summary stats")


# ----------------------------------------------------------------
#                          word statistics
# ----------------------------------------------------------------


def word_cloud(words: str, name: str) -> None:
	"""
	Creates a word cloud of the given words and saves it to the plots folder.
	"""
	wc = WordCloud(width=500, height=250, background_color="white", colormap="Greens", stopwords=db.stopset)
	wc.generate(words.upper())
	n = name.lower().replace(" ", "")

	return wc.to_file(f"data/output/images/senderpages/{n}_wc.png")


def calc_word_stats(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Calculates different statistics about the chat and enters collected data.
	"""
	# get all words in the chat
	words_str = " ".join(df.str.replace("\W", " ", regex=True).str.replace("xURL", " "))
	word_cloud(words_str, df.name)
	word_freq = pd.Series(words_str.lower().split()).value_counts().rename(df.name+ " common words")

	# export("myfuncs/calc_word_stats", word_freq, f"common_words{df.name}.csv")
	return word_freq


# --------------------------------------------
# Functions used to print the ouptut in a specific format
# --------------------------------------------


def say(*args, spaces: bool=False) -> str:
	"""
	Returns a string of strings/numbers which are divided with spaces, commas 
	and the word "and".
	"""
	listing = str()
	for i, arg in enumerate(args):
		if i != 0:
			listing += " " if spaces else ", " if i+1 < len(args) else " and "
		listing += str(arg)
	return listing


def calc_numerus(amount: int, term: str) -> str:
	"""
	Returns the correct plural form of a word depending on the amount passed.
	"""
	s = (str(amount) if amount > 1 else ("one" if amount == 1 else "no")) + " " + term
	return s + ("s" if amount != 1 and term not in ("media", "polarity") else "")


def get_stat_pair(stat_idx: int, sender_idx: int) -> tuple[int, str]:
	"""
	Returns the value and term of a specific statistic.
	"""
	return db.stats_df.iat[sender_idx, stat_idx], list(db.stats_dict.values())[stat_idx]


def get_txt_reports() -> list[str]:
	"""
	Creates a report about the sender at the given index which includes the 
	statistics about their messages or a summary report and returns it.
	"""
	reports_list, i = list(), int()

	def y(*idxs): return say(*[calc_numerus(*get_stat_pair(x, i)) for x in idxs])

	for i, s in enumerate(db.senders): # for each sender create a sender report
		reports_list.append("\n".join([f"{say(s)}...",
			f"... sent {y(0,6,18)} in this chat.",
			f"... average length of a message is {y(1,2)}.",
			f"... longest message was {y(3,4)} long.",
			f"... sent {y(11,7,8,10,9)}"
			F"... shared {y(12,13,14,17)}",
			f"... deleted {y(15)} in this chat"]))
		reports_list[-1] += (f"\nYou missed {y(16)} by {s}.") if db.stats_df.iat[i, 16] > 0 else ""
	
	# General report about the chat
	i = len(db.senders)
	reports_list.append([f"{y(0,6,18)}",
		f"The average message length is {y(1)}.",
		f"The {len(db.senders)} senders ...",
		f"... sent {y(11,7,8,10,9)}",
		f"... shared {y(12,13,14,17)}",
		f"... deleted {y(15)} in this chat"]) # add report to the list
	
	# export("myfuncs/get_reports", "\n\n".join(reports_list), "reports.txt")
	time("txt report creation")
	return reports_list

# ----------------------------------------------------------------
# 				Functions to create images for the report
# ----------------------------------------------------------------

def make_plots() -> None:
	plot0()
	return time("make plots")


def cmap(cm_name: str, countable):
	if type(countable) != int:
		countable = len(countable)
	return cm.get_cmap(cm_name)(np.linspace(.2, .8, countable+1))


def time_series():
	z = db.chat_og["Date"].value_counts()
	z1 = z.to_dict() #converts to dictionary
	db.chat_og["Msg_count"] = db.chat_og["Date"].map(z1)
	### Timeseries plot 
	fig = px.line(x=db.chat_og["Date"], y=db.chat_og["Msg_count"])
	fig.update_layout(title="Analysis of number of messages using TimeSeries plot.", xaxis_title="Month", yaxis_title="No. of Messages")
	fig.update_xaxes(nticks=20)
	fig.show()
	return


def plot0() -> None:
	# create pie chart from msg_count in stats_df
	plt.pie(db.stats_df.iloc[0:-1, 0], startangle=90, colors=cmap("Greens_r", db.senders), counterclock=False, autopct="%1.1f%%", wedgeprops={"ec":"w"})
	plt.legend(labels=db.senders, title="Sender:", shadow=True, loc="best")
	return plt.savefig("data/output/images/firstpage/plot0.png", transparent=True)


def plot_barh(df: pd.DataFrame, title: str, x_label: str, y_label: str, color: str) -> None:
	df.plot.barh(x=x_label, y=y_label, color=color, figsize=(10,5), legend=False, title=title)
	return plt.savefig(f"data/output/images/senderpages/barh_{df.name}.png", transparent=True)




# --------------------------------------------
#		Functions used to create pdf ouptut
# --------------------------------------------


pdf = FPDF()

xys: list[tuple[int, int]] = list() # last x, y coordinates
sizes: list[int] = list() # last text sizes


# def print_df_to_pdf(df: pd.DataFrame, cell_width: int = 25, cell_height: int = 6) -> None:
# 	"""
# 	Prints a dataframe to a table in a pdf file
# 	"""
# 	pdf.set_font("Arial", "B", 10)
# 	for col in df.columns:	# Loop over to print column names
# 		pdf.cell(cell_width, cell_height, col, align="C", border=1)
# 	pdf.ln(cell_height) # next row of table

# 	pdf.set_font("Arial", "", 8)
# 	for row in df.itertuples():	# Loop over to print each data in the table
# 		for col in df.columns:
# 			value = str(getattr(row, col))
# 			pdf.cell(cell_width, cell_height, value, align="C", border=1)
# 		pdf.ln(cell_height) # next row of table


def get_coord(x_offset: int=0, y_offset: int=0) -> tuple[int, int]:
	"""
	Returns the x, y cordinates on the current page
	"""
	return (pdf.get_x() + x_offset), (pdf.get_y() + y_offset)


def new_section(size: int=0, style: str="", space: int=0, np: int=0) -> None:
	"""
	Creates a new section in the pdf file and sets the font size and style.
	np: -1 = only footer, 0 = no new page (default), 1 = new page, 2 = new page and new section
	"""
	if pdf.page_no() == 0: # create first page
		pdf.set_margins(15, 20, 15)
		pdf.add_page()
	if np in (-1, 1, 2): # create footer for current page
		pdf.set_xy(0, 270)
		new_section(8, "I")
		pdf.cell(0, 5, f"Page {pdf.page_no()}", align="C")
	pdf.add_page() if np in (1, 2) else None # create new page
	if np in (0, 2): # create new section	on current or new page
		pdf.ln(space)
		xys.append({"x": pdf.get_x(), "y": pdf.get_y()})
		sizes.append(size) if size != 0 else None
		pdf.set_font("Arial", style, size if size != 0 else sizes[-1])
	return None


def make_pdf_report() -> None:
	"""
	Creates a pdf file with a summary of the chat and the statistics of each sender
	"""
	new_section(16, "B")
	pdf.cell(0, 10, "WhatsApp Chat Statistics", align="C")
	new_section(10, space=5)
	pdf.cell(0, 12, f"between {say(*db.senders)}", align="C")
	
	new_section(10, space=20)
	pdf.cell(90, 1, "This chat contained:" )
	new_section(14, "B", space=4)
	pdf.cell(120, 1, "1563330 messages, 6229 media and 34226 emojis")
	# pdf.cell(120, 1, db.reports[len(db.senders)][0])


	new_section(10, space=5)
	pdf.multi_cell(90, 4, "\n".join(db.reports[len(db.senders)][1:]))
	pdf.image("data/output/images/firstpage/plot0.png", x=80, y=20, w=150)

	for i, s in enumerate(db.senders):
		# 
		new_section(16, "B", np=2)
		pdf.cell(0, 10, "WhatsApp Chat Statistics", align="C")
		new_section(12, space=5)
		pdf.cell(0, 10, "for " + s , align="C")

		new_section(8, space=20)
		pdf.multi_cell(90, 4, db.reports[i])

		new_section(10, "B")
		pdf.set_xy(105, xys[-1]["y"] - 5)
		pdf.cell(90, 4, f"{s} WordCloud", align="C")
		n = s.lower().replace(" ", "")
		pdf.image(f"data/output/images/senderpages/{n}_wc.png", x=105, y=xys[-2]["y"], w=90)

	new_section(np=-1)
	pdf.output("data/output/pdfs/WA-Report.pdf", "F")
	return time("PDF creation")
