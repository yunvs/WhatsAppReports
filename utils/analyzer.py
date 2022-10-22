import re
import emojis
from unidecode import unidecode

from utils.helper import *


def analyze_chat() -> None:
	"""
	Analyzes the chat and creates the stats DataFrame.
	"""
	prepare_database()

	analysis_per_sender()  # data analysis

	calc_remaining_stats()  # get the summary statistics for all senders
	time("Calculating remaining statistics")
	return


def prepare_database() -> None:
	"""
	Prepares the database by filling data in variables placeholder.
	"""
	v.chat["weekday"] = v.chat["date"].apply(lambda x: x.weekday())  # add weekday
	v.chat["hour"] = v.chat["datetime"].apply(lambda x: x.hour)  # add hour
	v.chat_og = v.chat.copy()  # Create copy of chat to use it later

	v.sender = list(v.chat["sender"].unique())  # Creates list of senders
	v.sc = len(v.sender)  # Number of senders

	v.stats = pd.DataFrame(None, [*v.sender, "sum"], c.STATS_DICT.keys())
	v.tstats = pd.DataFrame(None, [*v.sender, "sum"], c.TSTATS_COLS)
	return


def analysis_per_sender() -> None:
	"""
	Performs the analysis of the chat per sender.
	"""
	# data separation, cleansing and data analysis per sender
	for i, s in enumerate(v.sender):
		df = v.chat.loc[v.chat["sender"] == s]  # DataFrame with messages from sender
		v.msg_per_s.append(df)

		clean_df = cleanse_df(df["message"], s)  # get stats for each sender
		count_occurrences(clean_df, i)  # count occurrences of words and emojis

		calc_stats(clean_df.rename(s))  # calculate the stats for each sender
		time(f"Analyzing chat for sender {str(i+1)} / {str(v.sc)}")
	
	v.msg_per_s.append(v.chat_og)  # add original chat to msg_per_s
	count_occurrences(None, v.sc)  # count occurrences of words and emojis
	return


def cleanse_df(df: pd.DataFrame, sender: str) -> pd.DataFrame:
	"""
	Cleans the DataFrame of non-message entities and replaces URLs and enters
	collected data into the stats DataFrame.
	"""
	count = 0  # counter for media messages cleaned
	for key, val in c.STATS_PATTERN.items():
		if key != "media":  # media messages are counted separately
			key_df = (df[df == val[1]] if val[0] == "exact" else df[df.str.contains(val[1])])
			df = df.drop(key_df.index)  # remove non-messages
			v.chat = v.chat.drop(key_df.index)  # remove non-messages
			if key in v.stats.columns:  # add counted data to stats_df.if it exists
				v.stats.at[sender, key] = key_df.shape[0]
				count += key_df.shape[0]
		else:
			v.stats.at[sender, key] = count
	return df


def count_occurrences(df: pd.DataFrame, i: int) -> None:
	"""
	Calculates different statistics about the chat and enters collected data.
	"""
	# combines all words in a single string
	all_msg = " ".join(df).lower() if i != v.sc else v.all_msgs 

	# count occurrences of emojis
	emj_dct = dict()
	emj_lst = emojis.get(all_msg)  # get list of emojis
	if emj_lst:
		for item in emj_lst:
			emj_dct[emojis.decode(item)] = all_msg.count(item)  # count emojis
		emoji_freq = pd.Series(emj_dct).sort_values(ascending=False).reset_index()
		emoji_freq.columns = ["Emoji", "Frequency"]
		v.common_emojis.append(emoji_freq)
	v.stats.iat[i, 19] = len(emj_dct)

	if i != v.sc:  # if not the last sender (sum)
		v.stats.at[v.sender[i], "emoji"] = sum(emj_dct.values())
		v.stats.at[v.sender[i], "link"] = len(re.findall("xurlx", all_msg))
		v.all_msgs += all_msg  # add all messages to all_msg

	# count occurrences of words
	all_msg = re.sub(r"(xurlx)|(\W)|(\d)", " ", unidecode(all_msg))
	if all_msg:
		word_freq = pd.Series(all_msg.split()).value_counts().reset_index()
		word_freq.columns = ["Word", "Frequency"]
		v.common_words.append(word_freq)

	v.all_msgs_clean.append(all_msg.upper())
	return


def calc_stats(s_df: pd.DataFrame) -> None:
	"""
	Calculates different statistics about the chat and enters collected data
	into the stats DataFrame.
	"""
	s = s_df.name  # get column name (sender)
	v.stats.at[s, "msg_count"] = s_df.shape[0]


	df_words = s_df.str.split().str.len()  # get number of words in each message
	v.stats.at[s, "words_avg"] = round(df_words.mean(), 1)
	v.stats.at[s, "words_max"] = df_words.max()
	v.word_counts.append(df_words)

	df_chars = s_df.str.replace(r"\W", "", regex=True).str.len()  # get number of characters in each message
	v.stats.at[s, "chars_avg"] = round(df_chars.mean(), 1)
	v.stats.at[s, "chars_max"] = df_chars.max()
	v.char_count.append(df_chars)

	v.stats.at[s, "sent_avg"] = round(
		v.chat.loc[v.chat["sender"] == s, "sentiment"].mean(skipna=True), 2
	)
	v.stats.at[s, "sent_pos"] = (
		v.chat.loc[v.chat["sender"] == s, "sentiment"].gt(0).sum()
	)
	v.stats.at[s, "sent_neg"] = (
		v.chat.loc[v.chat["sender"] == s, "sentiment"].lt(0).sum()
	)
	return


def calc_remaining_stats() -> None:
	"""
	Calculates summary statistics about the chat and enters collected data
	into the stats DataFrame.
	"""
	for i in range(v.sc + 1):
		msg_r = create_msg_range(i)
		v.msg_ranges.append(msg_r)

		v.tstats.iat[i, 0] = str(msg_r.index[0]).split()[0]
		v.tstats.iat[i, 1] = str(msg_r.index[-1]).split()[0]

		v.tstats.iat[i, 2] = str(msg_r[msg_r == msg_r.max()].index[0]).split()[0]
		v.tstats.iat[i, 3] = msg_r.max()

		v.tstats.iat[i, 4] = msg_r[msg_r != 0].shape[0]
		v.tstats.iat[i, 5] = msg_r[msg_r == 0].shape[0]

		v.tstats.iat[i, 6] = int((msg_r.index[-1] - msg_r.index[0]).days)
		# longest time span without messaging
		v.tstats.iat[i, 7] = (
			msg_r[msg_r == 0].groupby((msg_r != 0).cumsum()).transform("count").max()
		)

	for stat in c.STATS_DICT.keys():
		if any(x in stat for x in ["calls", "unique"]):
			v.stats.at["sum", stat] = 0
		elif "max" in stat:
			v.stats.at["sum", stat] = v.stats[stat].max()
		elif "avg" in stat:
			v.stats.at["sum", stat] = round(v.stats[stat].mean(), 3)
		else:
			v.stats.at["sum", stat] = v.stats[stat].sum()
	return


def create_msg_range(i: int) -> None:
	"""
	Creates a Series with the number of messages sent per day.
	"""
	msg_date = v.msg_per_s[i]["date"].value_counts().sort_index()
	chat_date_range = pd.date_range(msg_date.index[0], msg_date.index[-1])
	msg_range = pd.Series(index=chat_date_range, dtype=int)
	for date in chat_date_range.strftime("%Y-%m-%d"):
		msg_range[date] = msg_date[date] if date in msg_date.index else 0
	return msg_range
