import emojis
import re
import spacy
from unidecode import unidecode
from collections import Counter

from utils.helper import *

nlp = spacy.load("de_core_news_sm")


def analyze_chat() -> None:
	"""
	Analyzes the chat and creates the stats DataFrame.
	"""
	prepare_database()

	analysis_per_sender()  # data analysis per sender

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

	indexes = [*v.sender, "sum"]  # Create list of indexes for stats DataFrame
	v.stats = pd.DataFrame(None, indexes, c.STATS_DICT.keys())
	v.time_stats = pd.DataFrame(None, indexes, c.TIME_STATS_COLS)
	v.nlp_stats = pd.DataFrame(None, indexes, c.NLP_STATS_COLS)
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
		count_emojis(clean_df, i)  # count occurrences of words and emojis
		nlp_analysis(i)  # perform nlp analysis

		calc_stats(clean_df.rename(s))  # calculate the stats for each sender
		time(f"Analyzing chat for sender {str(i+1)} / {str(v.sc)}")
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


def count_emojis(df: pd.DataFrame, i: int) -> None:
	"""
	Calculates different statistics about the chat and enters collected data.
	"""
	# combines all words in a single string
	msgs = " ".join(df).lower() if i != v.sc else v.all_msgs

	# count occurrences of emojis
	emj_dct = dict()
	emj_lst = emojis.get(msgs)  # get list of emojis
	if emj_lst:
		for item in emj_lst:
			emj_dct[emojis.decode(item)] = msgs.count(item)  # count emojis
		emoji_freq = pd.Series(emj_dct).sort_values(ascending=False).reset_index()
		emoji_freq.columns = ["Emoji", "Frequency"]
		v.common_emojis.append(emoji_freq)
	v.stats.iat[i, 19] = len(emj_dct)

	if i != v.sc:  # if not the last sender (sum)
		v.stats.at[v.sender[i], "emoji"] = sum(emj_dct.values())
		v.stats.at[v.sender[i], "link"] = len(re.findall("xurlx", msgs))

	v.all_msgs += msgs if i != v.sc else ""  # all messages in one string

	msgs = re.sub(r"(xurlx)|(\W)|(\d)", " ", unidecode(msgs))

	v.all_msgs_clean.append(msgs.lower())
	return


def nlp_analysis(s_no: int) -> None:
	"""
	Performs nlp analysis for the sender s_no.
	"""
	doc = nlp(v.all_msgs_clean[s_no])  # spacy nlp object

	words, lemmas, stop_words, words_clean = list(), list(), list(), list()
	pos_tag_dict = dict()

	for token in doc:
		# extract words, lemmas and stop words
		if token.is_alpha:  # token is an alpha character
			words.append(token.text)
			if token.is_stop:
				stop_words.append(token.text)
			else:
				if token.lemma_ != "--":
					lemmas.append(token.lemma_.lower())
				words_clean.append(token.text)
		# count occurrences of pos tags
		if token.pos_ in pos_tag_dict:
			pos_tag_dict[token.pos_] += 1
		else:
			pos_tag_dict[token.pos_] = 1

	v.pos_tags.append(pos_tag_dict)

	for i, ls in enumerate([words, lemmas, stop_words, words_clean]):
		# counts and unique counts of words, lemmas, stop words and clean words
		v.nlp_stats.iat[s_no, i] = len(ls)
		v.nlp_stats.iat[s_no, i + 4] = len(set(ls))

	# average word length
	v.nlp_stats.iat[s_no, 8] = round(sum(len(w) for w in words) / len(words), 2)

	ents = dict()
	# counts and lists the different named entities types
	for ent in doc.ents:
		explanation = spacy.explain(ent.label_)
		if explanation not in ents:
			ents[explanation] = [1, set(ent.text)]
		else:
			ents[explanation][0] += 1
			ents[explanation][1].add(ent.text)

	v.named_entities.append(ents)
	v.named_entities_counts.append(len(doc.ents))

	# word, lemma, stopword and clean word frequencies
	v.frequencies.append([
		pd.DataFrame(Counter(words).most_common(), columns=["Word", "Frequency"]),
		pd.DataFrame(Counter(lemmas).most_common(), columns=["Lemma", "Frequency"]),
		pd.DataFrame(Counter(stop_words).most_common(), columns=["Stopword", "Frequency"]),
		pd.DataFrame(Counter(words_clean).most_common(), columns=["Word", "Frequency"]),
	])
	return


def calc_stats(s_df: pd.DataFrame) -> None:
	"""
	Calculates different statistics about the chat and enters collected data
	into the stats DataFrame.
	"""
	s = s_df.name  # get column name (sender)
	v.stats.at[s, "msg_count"] = s_df.shape[0]

	# number of words, average and max
	df_words = s_df.str.split().str.len()  # number of words in each message
	v.stats.at[s, "words_avg"] = round(df_words.mean(), 1)
	v.stats.at[s, "words_max"] = df_words.max()
	v.word_counts.append(df_words)

	# number of characters, average and max
	df_chars = s_df.str.replace(r"\W", "", regex=True).str.len()
	v.stats.at[s, "chars_avg"] = round(df_chars.mean(), 1)
	v.stats.at[s, "chars_max"] = df_chars.max()
	v.char_counts.append(df_chars)

	# sentiment calculation, positive, negative
	v.stats.at[s, "sent_avg"] = round(v.chat.loc[v.chat["sender"] == s, "sentiment"].mean(skipna=True), 2)
	v.stats.at[s, "sent_pos"] = (v.chat.loc[v.chat["sender"] == s, "sentiment"].gt(0).sum())
	v.stats.at[s, "sent_neg"] = (v.chat.loc[v.chat["sender"] == s, "sentiment"].lt(0).sum())
	return


def calc_remaining_stats() -> None:
	"""
	Calculates summary statistics about the chat and enters collected data
	into the stats DataFrame.
	"""
	v.msg_per_s.append(v.chat_og)  # add original chat to msg_per_s

	count_emojis(None, v.sc)  # count occurrences of words and emojis
	nlp_analysis(v.sc)  # perform nlp analysis

	for stat in c.STATS_DICT.keys():
		if any(x in stat for x in ["calls", "unique"]):
			v.stats.at["sum", stat] = 0
		elif "max" in stat:
			v.stats.at["sum", stat] = v.stats[stat].max()
		elif "avg" in stat:
			v.stats.at["sum", stat] = round(v.stats[stat].mean(), 3)
		else:
			v.stats.at["sum", stat] = v.stats[stat].sum()

	calc_time_stats()  # calculate time statistics
	return


def calc_time_stats() -> None:
	"""
	Calculates time statistics about the chat and enters collected data
	into the time_stats DataFrame.
	"""
	for i in range(v.sc + 1):
		msg_r = create_msg_range(i)
		v.msg_ranges.append(msg_r)

		# start and end date of chat
		v.time_stats.iat[i, 0] = str(msg_r.index[0]).split()[0]
		v.time_stats.iat[i, 1] = str(msg_r.index[-1]).split()[0]

		# maximal messages per day and date of that day
		v.time_stats.iat[i, 2] = str(msg_r[msg_r == msg_r.max()].index[0]).split()[0]
		v.time_stats.iat[i, 3] = msg_r.max()

		# amount of days with and without messages
		v.time_stats.iat[i, 4] = msg_r[msg_r != 0].shape[0]
		v.time_stats.iat[i, 5] = msg_r[msg_r == 0].shape[0]

		# message span in days
		v.time_stats.iat[i, 6] = int((msg_r.index[-1] - msg_r.index[0]).days)

		# longest span without messaging
		v.time_stats.iat[i, 7] = (msg_r[msg_r == 0].groupby((msg_r != 0).cumsum()).transform("count").max())

		# average amount of days without messaging
		v.time_stats.iat[i, 8] = round((msg_r[msg_r == 0].groupby((msg_r != 0).cumsum()).transform("count").mean()), 1)

		# average amount of messages per day
		v.time_stats.iat[i, 9] = round(msg_r.mean(), 1)
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
