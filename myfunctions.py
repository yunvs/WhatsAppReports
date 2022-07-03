import re, os, sys, zipfile
import pandas as pd


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
	with open(path, "r", encoding="utf-16") as f: # read the content of the file
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
	# DataFrame with stats about non-message enties in chat of sender
	stats = dict()
	sender = sender_df.columns[0]
	# Extract and drop non-message enties
	image_df = sender_df[sender_df[sender] == "‎image omitted"]
	messages_df = sender_df.drop(image_df.index)
	audio_df = sender_df[sender_df[sender] == "‎audio omitted"]
	messages_df = messages_df.drop(audio_df.index)
	sticker_df = sender_df[sender_df[sender] == "‎sticker omitted"]
	messages_df = messages_df.drop(sticker_df.index)
	video_df = sender_df[sender_df[sender] == "‎video omitted"]
	messages_df = messages_df.drop(video_df.index)
	contact_df = sender_df[sender_df[sender] == "‎Contact card omitted"]
	messages_df = messages_df.drop(contact_df.index)
	# location_df = sender_df[sender_df[sender].startswith("\"‎Location: https://maps.google.com/")]
	# messages_df = messages_df.drop(location_df.index)
	# document_df = sender_df[sender_df[sender].endswith("‎document omitted")]
	# messages_df = messages_df.drop(document_df.index)
	# deleted_df = sender_df[sender_df[sender].endswith("‎You deleted this message.", "‎This message was deleted.")]
	# messages_df = messages_df.drop(deleted_df.index)
	
	# enter the extracted counts into the stats
	stats["image"] = image_df.shape[0]
	stats["audio"] = audio_df.shape[0]
	stats["sticker"] = sticker_df.shape[0]
	stats["video"] = video_df.shape[0]
	stats["contact"] = contact_df.shape[0]
	# stats["location"] = location_df.shape[0]
	# stats["document"] = document_df.shape[0]
	# stats["deleted"] = deleted_df.shape[0]

	return messages_df, stats # return the cleaned dataframe and the stats dict