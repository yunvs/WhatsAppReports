import re, os, sys, zipfile
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from textstyle import *


def get_content(path: str):
	"""
	Gets file from given path, checks for desired fileformat and extracts the
	content of the file.
	"""
	if not os.path.isfile(path):
		sys.exit(BOLD(RED("ERROR: File not found")))
	_name, extension = os.path.splitext(path)
	if extension != ".zip" and extension != ".txt": # check for fileformat
		sys.exit(BOLD(RED("ERROR: Only .txt or .zip files are supported")))
	elif extension == ".zip": # extract the content of zip file
		with zipfile.ZipFile(path, "r") as zip_ref:
			zip_ref.extractall("data")
		path = "data/_chat.txt"
	
	# try opening path with uft-16 encoding if error try with uft-8 encoding
	try:
		with open(path, "r", encoding="utf-16") as f: # read the content of the file
			contents = f.readlines()
	except UnicodeError:
		with open(path, "r", encoding="utf-8") as f:
			contents = f.readlines()
	return contents


PATTERN = r"^\u200E? ?\[([\d./]*), ([\d:]*)\] ([\w ]*): (\u200E?.*)$"
def convert_chat(wa_listed: list):
	"""
	Convert the chat history to a pandas DataFrame (with columns: date, time, 
	sender, message) and into a dictionary with the messages per sender.
	"""
	chat = list() # list of all messages
	sender_messages = dict() # dictionary with key: sender, value: list of messages
	matched = False 

	for line in wa_listed:
		if re.match(PATTERN, line): # check if a new message starts in line
			matched = True
			res = re.search(PATTERN, line) # get groups of line
			# groups are: 1:date, 2:time, 3:sender, 4:message
			sender = res.group(3).split()[0].capitalize() # get sender
			chat.append([res.group(1), res.group(2), sender, res.group(4)])
			if sender not in sender_messages:
				sender_messages[sender] = [res.group(4)]
			else:
				sender_messages[sender].append(res.group(4))
		else:
			if not matched:
				sys.exit(BOLD(RED("ERROR: Sorry, the chat is not in the correct format")))
			current_line = " " + line.strip("\n")
			chat[-1][3] += current_line
			sender_messages[chat[-1][2]][-1] += current_line
	chat_df = pd.DataFrame (chat, columns = ["date", "time", "sender", "message"])
	chat_df["date"] = pd.to_datetime(chat_df["date"],infer_datetime_format=True)
	return chat_df, sender_messages


def get_stats(sender_df: pd.DataFrame):
	"""
	Gets different statistics about the chat and returns them as a tuple
	Output: (msg_total, msg_avg_len, msg_max_len, msg_min_len)
	"""
	sender = sender_df.columns[0]
	msg_total = sender_df.shape[0]
	msg_avg_len = round(sender_df[sender].str.len().mean(), 2)
	msg_max_len = sender_df[sender].str.len().max()
	msg_min_len = sender_df[sender].str.len().min()

	return (msg_total, msg_avg_len, msg_max_len, msg_min_len)

# number of messages, number of words, number of characters, number of unique words


def cleanse_df(sender_df: pd.DataFrame):
	"""
	Cleans the dataframe of non-message enties and returns a new dataframe as 
	well as an dict with keys: category and token: the amound of that category
	"""
	stats = dict() # dict with stats about non-message enties in chat of sender
	s_clean = sender_df.copy()
	sender = s_clean.columns[0] # current sender

	entities = {"ximg":"‎image omitted", "xaud":"‎audio omitted", 
		"xstick":"‎sticker omitted", "xvid":"‎video omitted", 
		"xgif":"‎GIF omitted", "med":"", "xmiss":"‎Missed ", 
		"xcont":"‎Contact card omitted", "xloc":"‎Location: ", 
		"xdoc":"‎document omitted", "link":"http://|https://",
		"xdel":"‎You deleted |‎This message was deleted."}

	# Extract and remove non-message enties
	for key, value in entities.items():
		if key != "med":
			if key not in ("xmiss", "xloc", "xdoc", "xdel", "link"):
				key_df = s_clean[s_clean[sender] == value]
			else:
				key_df = s_clean[s_clean[sender].str.contains(value)]
		if key[:1] == "x":
			s_clean = s_clean.drop(key_df.index)
		globals()[f"{key}_df"] = key_df


	# remove all remaining non-message enties (Whatsapp system messages)
	s_clean = s_clean.drop(s_clean[s_clean[sender].str.contains("‎")].index)


	# Testing purposes only
	# sender_df.to_csv(f"data/testing/myfunctions/sender_df_{sender}.csv",index=True) # save the dataframe to a csv file
	# s_clean.to_csv(f"data/testing/myfunctions/s_clean_{sender}.csv",index=True) # save the dataframe to a csv file

	# enter the extracted counts into the stats
	for key in entities.keys():
		if key != "med":
			stats[key] = globals()[f"{key}_df"].shape[0] # get the amount of non-message enties
		else:
			stats[key] = sum(stats.values()) 
	
	return s_clean, stats # return the cleaned dataframe and the stats dict