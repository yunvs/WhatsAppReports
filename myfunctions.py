from ctypes import Union
from textstyle import *  # used for printing colored and bold text
import database as db # used to access local database
import pandas as pd # used for dataframe 
import re
import emojis
# from collections import Counter
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def off(error_message: str) -> None:
	"""
	Prints error message and safely exits the program
	"""
	exit(BOLD(RED("ERROR: " + error_message)))


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
		return True # the beginning of a new message
	return False # continuation of the previous message


def convert_line(input_line: str) -> list[str]:
	"""
	Converts a WA chat history line into a list with these entries:
	datetime, sender, message, emojis_unique, emoji_count, url_count
	"""
	# match pattern and devide into groups: 1:date, 2:time, 3:sender, 4:message
	x = re.search("^.? ?\[([\d./]*), ([\d:]*)\] ([\w ]*): (\u200E?.*)$", input_line)
	result = [" ".join([x.group(1),x.group(2)])] # combine date and time
	result.append(x.group(3).title()) # capitalize first letters of sender
	message = re.sub("https?://\S+", "xURL", x.group(4)) # replace URLs with "xURL"
	result.append(message) # add message
	result.append(emojis.get(message)) # get set of unique emoji in message
	result.append(emojis.count(message)) # count amount of emoji in message
	result.append(len(re.findall("xURL", message))) # count URLs
	return result


def convert_to_list(path_to_file: str) -> list[list[str]]:
	"""
	Converts a .txt-file of messages into a list of lists: Each list element contains 
	these elements: [datetime, sender, message, emojis, emoji_count, url_count]
	"""
	chat_listed, last_message = list(), str()
	try: # try to open the file
		with open(path_to_file, "r", encoding="utf-8") as file:
			for line in file: # read line by line
				if new_message(line): # the line is the beginning of a new message
					if last_message != "": # buffer is not empty
						chat_listed.append(convert_line(last_message)) # add previous message to list
					last_message = line.strip().strip("\n").strip() # add new message to buffer
				else: # the line is a continuation of the previous message
					last_message += " " + line.strip().strip("\n").strip() # add line to previous message
			if chat_listed[-1] != convert_line(last_message): # the last message is not added to the list
				chat_listed.append(convert_line(last_message)) # add last message to list
	except FileNotFoundError: # the file does not exist
		off("File not found")
	except (UnicodeDecodeError, UnicodeError): # the file is not in UTF-8
		off(f"File not in UTF-8 format\nTry again or upload the {GREEN('original .zip file')}")
	return chat_listed


def convert_to_df(path: str) -> pd.DataFrame:
	"""
	Converts a list of lists into a dataframe with the following columns:
	[datetime, sender, message, emojis, emoji_count, url_count] and returns it
	"""
	chat_listed = convert_to_list(path)
	columns = ["datetime","sender","message","emojis","emoji_count","url_count"]
	df = pd.DataFrame(chat_listed, columns=columns)
	df["datetime"] = pd.to_datetime(df["datetime"])
	return df


def cleanse_df(df: pd.DataFrame, sender: str) -> pd.DataFrame:
	"""
	Cleans the dataframe of non-message enties and replaces URLs and enters 
	collected data into the stats dataframe
	"""
	count = 0 # counter for media messages cleaned
	for key, value in db.stats_matches.items():
		if key == "media_total":
			db.stats_df.at[sender,key] = count # add counted media data to stats_df
			continue
		if value[0] == "=": # non-message is exact match with value
			key_df = df[df == value[2]]
		else: # non-message contains value
			key_df = df[df.str.contains(value[2])]
		if value[1] == "x": # remove hole non-message entry
			df = df.drop(key_df.index) # remove non-message from clean_df
			db.chat = db.chat.drop(key_df.index) # remove non-message from chat_df
		if key in db.stats_df.columns: # add counted data to stats_df if it exists
			db.stats_df.at[sender,key] = key_df.shape[0]
			count += key_df.shape[0]
	return df.rename(sender) # return the cleaned dataframe


def get_stats(sender_df: pd.DataFrame) -> pd.DataFrame:
	"""
	Calculates different statistics about the chat and enters collected data 
	into the stats dataframe
	"""
	s = sender_df.name # get column name (sender)
	db.stats_df.at[s,"msg_total"] = sender_df.shape[0]
	db.stats_df.at[s,"msg_chars_avg"] = round(sender_df.str.replace(" ", "").str.len().mean(), 1)
	db.stats_df.at[s,"msg_words_avg"] = round(sender_df.str.split().str.len().mean(), 1)
	db.stats_df.at[s,"msg_chars_max"] = sender_df.str.replace(" ", "").str.len().max()
	db.stats_df.at[s,"msg_words_max"] = len(sender_df[sender_df.str.len().idxmax()].split())
	db.stats_df.at[s,"link"] = db.chat.loc[db.chat["sender"] == s, "url_count"].sum()
	db.stats_df.at[s,"emoji"] = db.chat.loc[db.chat["sender"] == s, "emoji_count"].sum()
	emoji_set = set().union(*list(db.chat.loc[db.chat["sender"] == s, "emojis"]))
	db.stats_df.at[s,"emoji_unique"] = (len(emoji_set), emoji_set)
	return sender_df


def get_sum_stats() -> None:
	"""
	Calculates summary statistics about the chat and enters collected data
	into the stats dataframe
	"""
	for stat in db.stats_df_columns:
		if "max" in stat or "unique" in stat or "missed" in stat:
			continue
		elif "avg" in stat:
			db.stats_df.at["sum",stat] = round(db.stats_df[stat].mean(), 1)
		else:
			db.stats_df.at["sum",stat] = db.stats_df[stat].sum()
	return


def pl(amount: int, indexmessage) -> str: 
	"""
	Returns the correct plural form of a word depending on the amount
	"""
	if isinstance(indexmessage, int):
		indexmessage = db.stats_df_columns[indexmessage]
	if amount > 1:
		if indexmessage == "media":
			return str(amount) + " " + indexmessage
		return str(amount) + " " + indexmessage + "s"
	elif amount == 1:
		return "one " + indexmessage
	else:
		return "not a single " + indexmessage


def say(*args) -> str:
	"""
	Returns a bold printed string of strings/numbers which are divided with 
	spaces, commas and the word "and"
	"""
	output = str(args[0])
	if len(args) != 1:
		for i, arg in enumerate(args):
			if i == 0:
				continue
			elif i+1 < len(args):
				output += ", " + str(arg)
			else:
				return BOLD(output) + " and " + BOLD(args[i])
	else:
		return BOLD(output)


def get_stat_value(sender_index: int, stat_index: int) -> int:
	"""
	Returns the value of a specific statistic for a specific sender.
	"""
	return db.stats_df.iat[sender_index,stat_index]


def get_reports() -> list[str]:
	"""
	Creates a report about the sender at the given index which includes the 
	statistics about their messages or a summary report and returns it.
	"""
	output, i = list(), len(db.senders)
	def f1(stat_index): return pl(get_stat_value(i,stat_index), stat_index)
	def f2(stat_index, description:str): return pl(get_stat_value(i,stat_index), description)
	output.append(f"""
	{GREEN("This WA Chat was between",say(*db.senders))}:
	All in all {say(f2(0,"message"),f1(17),f2(5,"media"))} were sent in this chat.
	A average message is {say(f2(1,"character"))} long and contains {say(f2(2,"word"))}.
	The {say(f"{i} senders")} sent {say(f1(10),f1(6),f1(7),f1(9),f1(8))},
	  they shared {say(f1(11),f1(12),f1(13),f1(16))}
	  and deleted {say(f2(14,"message"))} in this chat.""")
	for i in range(len(db.senders)):
		s = db.senders[i] # get sender
		report = f"""
	{GREEN("WA-Report for",say(s))}:
	{s} sent {say(f2(0,"message"),f1(17),f2(5,"media"))} in this chat.
	A average message is {say(f2(1,"character"))} long and contains {say(f2(2,"word"))}.
	The {say("longest message")} they sent contained {say(f2(3,"character"),f2(4,"word"))}.
	{s} sent {say(f1(10),f1(6),f1(7),f1(9),f1(8))}.
	They shared {say(f1(11),f1(12),f1(13),f1(16))}.
	{s} changed their mind {say(f2(14,"time"),STRIKE("deleted a message"))}."""
		if get_stat_value(i, 15) > 0:	
			report += f"""\n\tYou missed {say(f2(15,"(video)call"))} by {s}."""
		output.append(report)
	return output
