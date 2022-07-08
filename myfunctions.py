from textstyle import *  # used for printing colored and bold text
import database as db # used to access local database
import pandas as pd # used for dataframe 
import re
import emojis
# from collections import Counter
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def off(text: str()) -> None:
	"""
	Prints error message and safely exits the program
	"""
	exit(BOLD(RED("ERROR: " + text)))


def fileformat(path: str) -> str:
	"""
	Checks if the fileformat is correct and returns correct path
	"""
	if path.endswith(".txt"):
		return path
	elif path.endswith(".zip"):
		from zipfile import ZipFile
		with ZipFile(path, "r") as zip_ref:
			zip_ref.extractall("data")
		return "data/_chat.txt"
	else:
		off("Only .txt or .zip files are supported")


def new_message(line: str) -> bool:
	"""
	Checks if the input is the beginning of a new message (date in front) or not
	"""
	if re.match("^.? ?\[([\d./]*), ([\d:]*)\] ([\w ]*)", line):
		return True # the beginning of a new message
	return False # continuation of the previous message


def convert_line(line: str) -> list[str]:
	"""
	Converts a WA chat history line into a list with these entries:
	datetime, sender, message, emojis, emoji_count, url_count
	"""
	# match pattern and devide into groups: 1:date, 2:time, 3:sender, 4:message
	x = re.search("^.? ?\[([\d./]*), ([\d:]*)\] ([\w ]*): (\u200E?.*)$", line)
	result = [" ".join([x.group(1),x.group(2)])] # combine date and time
	result.append(x.group(3).title()) # capitalize first letters of sender
	message = re.sub("https?://\S+", "xURL", x.group(4)) # replace URLs with "xURL"
	result.append(emojis.decode(message)) # decode emojis
	result.append(list(emojis.get(message))) # get list of unique emoji in message
	result.append(emojis.count(message)) # count amount of emoji in message
	result.append(len([*re.finditer("xURL", message)])) # count URLs
	return result


def convert_to_list(path: str) -> list[list[str]]:
	"""
	Converts a .txt-file of messages into a list of lists: Each list element contains 
	these elements: [datetime, sender, message, emojis, emoji_count, url_count]
	"""
	data, buffer, line = list(), str(), str()
	try: # try to open the file
		with open(path, "r", encoding="utf-8") as file:
			for line in file: # read line by line
				if new_message(line): # if the line is the beginning of a new message
					if buffer != "": # if buffer is not empty
						data.append(convert_line(buffer)) # add previous message to list
					buffer = line.strip().strip("\n").strip() # add new message to buffer
				else: # if the line is a continuation of the previous message
					buffer += " " + line.strip().strip("\n").strip() # add line to previous message
			last = convert_line(buffer) # add last message to list
			if data[-1] != last: # if the last message is not the last line in the file
				data.append(last) # add last message to list
	except FileNotFoundError: # if the file does not exist
		off("File not found")
	except (UnicodeDecodeError, UnicodeError): # if the file is not in UTF-8
		off(f"File not in UTF-8 format\nTry uploading the {GREEN('original .zip file')}")
	return data



def convert_to_df(chat_list: list[list[str]]) -> pd.DataFrame:
	"""
	Converts a list of lists into a dataframe with the following columns:
	[datetime, sender, message, emojis, emoji_count, url_count] and returns it
	"""
	cols = ["datetime","sender","message","emojis","emoji_count","url_count"]
	df = pd.DataFrame(chat_list, columns=cols)
	df["datetime"] = pd.to_datetime(df["datetime"])
	return df


def cleanse_df(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Cleans the dataframe of non-message enties and replaces URLs and enters 
	collected data into the stats dataframe
	"""
	s = df.name # current sender
	count = 0 # counter for media messages cleaned
	for key, value in db.stats_matches.items():
		if key != "media_total":
			if value[0] == "=": # non-message is exact match with value
				key_df = df[df == value[2]]
			else: # non-message contains value
				key_df = df[df.str.contains(value[2])]
			if value[1] == "x": # remove hole non-message entry
				df = df.drop(key_df.index) # remove non-message from clean_df
			if key in db.stats_df.columns: # add counted data to stats_df if it exists
				db.stats_df.at[s,key] = key_df.shape[0]
				count += key_df.shape[0]
		else:
			db.stats_df.at[s,key] = count # add counted media data to stats_df 

	### Testing purposes only ###
	# sender_df.to_csv(f"data/testing/myfunctions/og_df_{s}.csv",index=True)
	# df.to_csv(f"data/testing/myfunctions/clean_df_{s}.csv",index=True)

	return df # return the cleaned dataframe


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
	return sender_df


def pl(n: int, s) -> str:
	"""
	Returns the correct plural form of a word depending on the number
	"""
	if isinstance(s, int):
		s = db.stats_df_columns[s]
	if n > 1:
		return str(n) + " " + s + "s"
	else:
		if n == 1:
			return "one " + s
		else:
			return "not a single " + s


def l(*args) -> str:
	"""
	Returns a string of strings/numbers which are divided with commas and spaces
	"""
	s = str()
	for i, arg in enumerate(args):
		s += str(arg)
		if len(args) > i+1:
			s += ", "
	return s


def print_report(i: int) -> None:
	"""
	Prints a report about the sender and the statistics collected
	"""
	def y(x): return db.stats_df.iat[i,x]
	s = db.senders[i]
	string = f"""
	{GREEN("WA-Report for",BOLD(s))}:
	{s} sent {BOLD(pl(y(0),"message"))} and {BOLD(y(5),"media")} in this chat.
	A average message is {BOLD(pl(y(1),"character"))} long and contains {BOLD(pl(y(2),"word"))}.
	The {BOLD("longest message")} they sent contained {BOLD(pl(y(3),"characters"))} and {BOLD(pl(y(4),"word"))}.
	{s} sent {BOLD(l(pl(y(10),10),pl(y(6),6),pl(y(7),7),pl(y(9),9)))} and {BOLD(pl(y(8),8))}.
	They shared {BOLD(l(pl(y(11),11),pl(y(12),12),pl(y(13),13)))} and {BOLD(pl(y(16),16))}.
	{s} changed their mind {BOLD(pl(y(14),"time"))} and {STRIKE("deleted a message")}."""
	if y(15) > 0:
		string += f"""\n\tYou missed {BOLD(pl(y(15),"(video)call"))} by {s}."""
	print(string)