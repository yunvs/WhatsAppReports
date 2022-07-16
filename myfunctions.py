from outputstyle import *  # used for printing colored and bold text
import database as db  # used to access local database
import re
import emojis
import pandas as pd  # used for dataframe
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from textblob_de import TextBlobDE as TextBlob


def off(*args) -> None:
	"""
	Prints error message and safely exits the program
	"""
	exit(BOLD(RED("Error: ") + " ".join(args)))


def export(location: str, *args) -> None:
	path = f"data/testing/exports/{location}/"
	for i, arg in enumerate(args):
		if i % 2 == 0:
			try:
				if args[i+1].endswith(".csv"):
					arg.to_csv(path + args[i+1], index=True)
				elif args[i+1].endswith(".txt"):
					with open(path + args[i+1], "w") as file:
						file.write(str(arg))
			except FileNotFoundError:
				import os
				os.makedirs(path, exist_ok=True)
				export(location, arg, args[i+1])


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
	result.append(TextBlob(message).polarity)  # add emojis
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
	df["datetime"] = pd.to_datetime(df["datetime"])  # 
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
	return sender_df


def get_sum_stats() -> None:
	"""
	Calculates summary statistics about the chat and enters collected data
	into the stats dataframe
	"""
	for stat in db.cstats_cols:
		if type(stat) == tuple:
			stat = stat[0]
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
	Creates a word cloud of the given words and saves it to the word_clouds
	folder
	"""
	STOPWORDS.update(db.stop_words)
	wc = WordCloud(background_color="white", width=1920, height=1080).generate(words)
	plt.imshow(wc, interpolation="bilinear")
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
	words_str = " ".join(df.str.replace("\W", " ").str.replace("xURL", " "))
	word_cloud(words_str, df.name)
	word_freq = pd.Series(words_str.lower().split()).value_counts().rename(df.name)
	print(f"{df.name}'s most common words:")
	print(word_freq.head(20))

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
	if term == "media": # media is a special case
		return str(amount) + " " + term
	if amount > 1: # if more than one, add an "s"
		return str(amount) + " " + term + "s"
	return "one " if amount == 1 else "not a single " + term


def get_stat_pair(stat_index: int, sender_index: int) -> str:
	"""
	Returns the value and term of a specific statistic.
	"""
	term = db.cstats_cols[stat_index]
	term = term if type(term) != tuple else term[1]
	return db.cstats_df.iat[sender_index, stat_index], term


def get_reports() -> list[str]:
	"""
	Creates a report about the sender at the given index which includes the 
	statistics about their messages or a summary report and returns it.
	"""
	reports_list, i = list(), len(db.senders)
	def y(*indices): return say(*[calc_numerus(get_stat_pair(x, i)) for x in indices])

	# General report about the chat
	sl = [GREEN(f"\tThis WA Chat was between {say(*db.senders)}:"),
		f"Their chat contained {y(0,6,18)}.",
		f"The average legth of a message is {y(1,2)}.",
		f"The {say(f'{i} senders')} sent {y(11,7,8,10,9)},",
		f"they shared {y(12,13,14,17)}",
		f"and deleted {y(15)} in this chat."]
	reports_list.append("\n\t".join(sl)) # add report to the list

	for i in range(i): # for each sender create a sender report
		s = db.senders[i]  # get sender name
		sl = [GREEN(f"\t{say(s)}'s report:"),
			f"{s} sent {y(0,6,18)} in this chat.",
			f"The average length of a message is {y(1,2)}.",
			f"The longest message {s} sent contained {y(3,4)}."
			f"{s} sent {y(11,7,8,10,9)}", 
			f"and shared {y(12,13,14,17)}",
			f"{y(15)} were deleted by {s} in this chat."]
		if db.cstats_df.iat[i, 16] > 0:
			sl.append(f"You missed {y(16)} by them.")
		reports_list.append("\n\t".join(sl)) # add report to list
	
	export("get_reports", "\n\n".join(reports_list), "reports")
	return reports_list
