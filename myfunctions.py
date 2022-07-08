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
	matched_before = False 

	for line in wa_listed:
		if re.match(PATTERN, line): # check if a new message starts in line
			res = re.search(PATTERN, line) # get groups of line
			# groups are: 1:date, 2:time, 3:sender, 4:message
			chat.append([res.group(1), res.group(2), res.group(3), res.group(4)])
			matched_before = True
			if res.group(3) not in sender_messages:
				sender_messages[res.group(3)] = [res.group(4)]
			else:
				sender_messages[res.group(3)].append(res.group(4))
		else:
			if not matched_before:
				sys.exit(BOLD(RED("ERROR: Sorry, the chat is not in the correct format")))
			current_line = " " + line.strip("\n")
			chat[-1][3] += current_line
			sender_messages[chat[-1][2]][-1] += current_line
	chat_df = pd.DataFrame (chat, columns = ["date", "time", "sender", "message"])
	chat_df["date"] = pd.to_datetime(chat_df["date"], infer_datetime_format=True)
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

	# Extract and remove non-message enties
	image_df = s_clean[s_clean[sender] == "‎image omitted"]
	s_clean = s_clean.drop(image_df.index) # remove image messages
	audio_df = s_clean[s_clean[sender] == "‎audio omitted"]
	s_clean = s_clean.drop(audio_df.index) # remove audio messages
	sticker_df = s_clean[s_clean[sender] == "‎sticker omitted"]
	s_clean = s_clean.drop(sticker_df.index) # remove sticker messages
	video_df = s_clean[s_clean[sender] == "‎video omitted"]
	s_clean = s_clean.drop(video_df.index) # remove video messages
	gif_df = s_clean[s_clean[sender] == "‎GIF omitted"]
	s_clean = s_clean.drop(gif_df.index) # remove GIF messages
	missed_df = s_clean[s_clean[sender].str.startswith("‎Missed ")]
	s_clean = s_clean.drop(missed_df.index) # remove missed messages
	contact_df = s_clean[s_clean[sender] == "‎Contact card omitted"]
	s_clean = s_clean.drop(contact_df.index) # remove contact messages
	location_df = s_clean[s_clean[sender].str.startswith("‎Location: https://maps.google.com/")]
	s_clean = s_clean.drop(location_df.index) # remove location messages
	document_df = s_clean[s_clean[sender].str.endswith("‎document omitted")]
	s_clean = s_clean.drop(document_df.index) # remove document messages
	deleted_df = s_clean[s_clean[sender].str.startswith(("‎You deleted this message.", "‎This message was deleted."))]
	s_clean = s_clean.drop(deleted_df.index) # remove "deleted" messages

	# remove all remaining non-message enties (Whatsapp system messages)
	s_clean = s_clean.drop(s_clean[s_clean[sender].str.contains("‎")].index)

	# Testing purposes only
	# sender_df.to_csv(f"data/testing/myFunctions/sender_df_{sender}.csv", index=True) # save the dataframe to a csv file
	# s_clean.to_csv(f"data/testing/myFunctions/s_clean_{sender}.csv", index=True) # save the dataframe to a csv file

	
	# enter the extracted counts into the stats
	stats["image"] = image_df.shape[0]
	stats["audio"] = audio_df.shape[0]
	stats["sticker"] = sticker_df.shape[0]
	stats["video"] = video_df.shape[0]
	stats["gif"] = gif_df.shape[0]
	stats["media"] = sum(stats.values())
	stats["document"] = document_df.shape[0]
	stats["contact"] = contact_df.shape[0]
	stats["location"] = location_df.shape[0]
	stats["missed"] = missed_df.shape[0]
	stats["deleted"] = deleted_df.shape[0]

	return s_clean, stats # return the cleaned dataframe and the stats dict