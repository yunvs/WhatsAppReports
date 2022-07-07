import database as db # used to access general lists
import pandas as pd # used for dataframe 
import re
from textstyle import *  # used for printing colored and bold text
# import db # used to access the stats dataframe
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
	Converts a WA chat history line into a list with three entries:
	datetime, sender, message
	"""
	x = re.search("^.? ?\[([\d./]*), ([\d:]*)\] ([\w ]*): (\u200E?.*)$", line)
	# match pattern and devide into groups: 1:date, 2:time, 3:sender, 4:message
	return [" ".join([x.group(1),x.group(2)]), x.group(3).title(), x.group(4)]


def convert_to_list(path: str) -> list[list]:
	"""
	Converts a .txt-file of messages into a list of lists
	Each list element contains these elements: [date, time, sender, message]
	"""
	data, buffer, line = list(), list(), str()
	try: # try to open the file
		with open(path, "r", encoding='utf-8') as file:
			for line in file: # read line by line
				if new_message(line): # if the line is the beginning of a new message
					if buffer: # if buffer is not empty
						data.append(buffer) # add previous message to list
					buffer = convert_line(line) # add new message to buffer
				else: # if the line is a continuation of the previous message
					buffer[-1] += line.rstrip() # add line to previous message
			if data[-1] != buffer: # if the last message is not the last line in the file
				data.append(buffer) # add last message to list
	except FileNotFoundError: # if the file does not exist
		off("File not found")
	except (UnicodeDecodeError, UnicodeError): # if the file is not in UTF-8
		off(f"File not in UTF-8 format\nTry uploading the {GREEN('original .zip file')}")
	return data


def convert_to_df(chat_list: list[list]) -> pd.DataFrame:
	"""
	Converts a list of lists into a dataframe with the following columns:
	[datetime, sender, message] and returns it
	"""
	chat_df = pd.DataFrame(chat_list, columns=["datetime","sender","message"])
	chat_df["datetime"] = pd.to_datetime(chat_df["datetime"])
	return chat_df


def cleanse_df(sender_df: pd.DataFrame) -> pd.DataFrame:
	"""
	Cleans the dataframe of non-message enties and replaces URLs and enters 
	collected data into the stats dataframe
	"""
	clean_df = sender_df.copy(deep=True)
	s = clean_df.name # current sender
	count = 0 # counter for media messages cleaned
	for key, value in db.stats_matches.items():
		if key != "media_total":
			if value[0] == "=": # non-message is exact match with value
				df = clean_df[clean_df == value[2]]
			else: # non-message contains value
				df = clean_df[clean_df.str.contains(value[2])]
			if value[1] == "x": # remove hole non-message entry
				clean_df = clean_df.drop(df.index) # remove non-message from clean_df
			elif value[1] == "rep": # remove replace non-message segment with value[3]
				clean_df = clean_df.str.replace(value[2], value[3], regex=True)
			if key in db.stats_df.columns: # add counted data to stats_df if it exists
				db.stats_df.at[s,key] = df.shape[0]
				count += df.shape[0]
			if key == "rest" and df.shape[0] > 0:
				df.to_csv(f"data/testing/myfunctions/rest_df_{s}.csv",index=True) # save the dataframe to a csv file
		else:
			db.stats_df.at[s,key] = count # add counted media data to stats_df 

	### Testing purposes only ###
	sender_df.to_csv(f"data/testing/myfunctions/og_df_{s}.csv",index=True)
	clean_df.to_csv(f"data/testing/myfunctions/clean_df_{s}.csv",index=True)

	return clean_df # return the cleaned dataframe


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
