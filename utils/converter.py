from utils.helper import *

import re  # for regex
from textblob_de import TextBlobDE as TextBlob  # for sentiment analysis


def convert_file(path: str) -> None:
	"""
	Checks and converts a file of messages into a pandas DataFrame with the columns date, datetime, sender, message and sentiment.
	"""
	chat_list = convert_file_to_list(path)
	v.chat = convert_list_to_df(chat_list)

	time("converting the original file to a pandas DataFrame")
	return


def convert_file_to_list(path_to_file: str) -> list[list[str]]:
	"""
	Converts a .txt-file of messages into a list of messages and returns it.
	"""
	chat, last_msg = list(), str()
	try:  # try to open the file
		with open(path_to_file, "r", encoding="utf-8") as file:
			for line in file:  # read line by line
				# line begins with a new message
				if re.match("^.? ?\[([\d./]*), ([\d:]*)\] .*", line):
					# add buffer to list
					chat.append(convert_ln(last_msg)) if last_msg != "" else None
					last_msg = line.strip().strip("\n").strip()  # add new message to buffer
				else:  # line is the continuation of the last message
					last_msg += " " + line.strip().strip("\n").strip()  # add line to buffer
			# add buffer to list if it is not added yet
			chat.append(convert_ln(last_msg)) if chat[-1] != convert_ln(last_msg) else None
	except FileNotFoundError:  # file does not exist
		return off("File not found\nCheck the path to the file")
	except (UnicodeDecodeError, UnicodeError):  # file is not in UTF-8
		return off("File not in UTF-8 format\nTry uploading the original file")
	return chat


def convert_ln(input: str) -> list[str]:
	"""
	Converts a line of the WhatsApp chat history into a list and returns it.
	"""
	# match pattern and divide into groups: 1:date, 2:datetime, 3:sender, 4:message
	x = re.search("^.? ?\[([\d./]*), ([\d:]*)\] ([\w ]*): (\u200E?.*)$", input)
	result = [x.group(1), " ".join([x.group(1), x.group(2)])]  # add date, datetime
	result.append(x.group(3).title())  # add name of sender
	message = re.sub("https?://\S+", "xURLx", x.group(4))  # replace URLs
	result.append(message)  # add message
	if len(message) > 2 and message.upper().isupper():  # add sentient
		result.append(TextBlob(message.replace("xURLx", "")).sentiment.polarity)
	else:
		result.append(pd.NA)
	return result


def convert_list_to_df(chat_list: list[list[str]]) -> pd.DataFrame:
	"""
	Converts the list of messages into a pandas DataFrame and returns it.
	"""
	df = pd.DataFrame(chat_list, columns=["date", "datetime", "sender", "message", "sentiment"])  # convert into DataFrame
	df["date"] = pd.to_datetime(
		df["date"], infer_datetime_format=True, format="%d.%m.%Y")  # format date
	df["datetime"] = pd.to_datetime(
		df["datetime"], infer_datetime_format=True)  # format datetime
	return df