import re  # for regex
from textblob_de import TextBlobDE as TextBlob  # for sentiment analysis

from utils.helper import *


def convert_lines(lines: str) -> None:
	"""
	Checks and converts a file of messages into a pandas DataFrame
	with the columns date, datetime, sender, message and sentiment.
	"""
	chat_list = convert_list(lines)
	v.chat = convert_list_to_df(chat_list)

	time("Converting chat to a pandas.DataFrame")
	return


def convert_list(lines: list[str]) -> list[list[str]]:
	"""
	Converts a list of strings into a list of sorted messages and returns it.
	"""
	chat, last_msg = list(), str()
	first_msg_reached = False
	for line in lines[1:]:  # iterate over lines
		if not first_msg_reached:
			if not re.match(r"^.? ?\[([\d./]*), ([\d:]*)\] .*:.*$", line):
				continue
			else:
				first_msg_reached = True
		# line begins with a new message
		if re.match(r"^.? ?\[([\d./]*), ([\d:]*)\] .*:.*$", line):
			# add buffer to list
			chat.append(convert_ln(last_msg)) if last_msg != "" else None
			last_msg = line.strip().strip("\n").strip()  # add new message to buffer
		else:  # line is the continuation of the last message
			last_msg += " " + line.strip().strip("\n").strip()  # add line to buffer
	# add buffer to list if it is not added yet
	chat.append(convert_ln(last_msg)) if chat[-1] != convert_ln(last_msg) else None

	return chat


def convert_ln(input: str) -> list[str]:
	"""
	Converts a line of the WhatsApp chat history into a list and returns it.
	"""
	# match pattern and divide into groups: 1:date, 2:datetime, 3:sender, 4:message
	x = re.search(r"^.? ?\[([\d./]*), ([\d:]*)\] (.+?\u202A?): (\u200E?.*)$", input)
	if not x:
		return list()
	result = [x.group(1), " ".join([x.group(1), x.group(2)])]  # add date, datetime
	result.append(x.group(3).strip("‪").strip("‬").title())  # add name of sender
	message = re.sub(r"https?://\S+", "xURLx", x.group(4))  # replace URLs
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
	df = pd.DataFrame(chat_list, columns=["date", "datetime", "sender", "message", "sentiment"])
	df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True, format="%d.%m.%Y")  # format date
	df["datetime"] = pd.to_datetime(df["datetime"], infer_datetime_format=True)  # format datetime
	return df
