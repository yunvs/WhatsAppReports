from timeit import default_timer as timer  # for timing
ts = [timer()]

import pandas as pd  # to create DataFrames
import numpy as np
from unidecode import unidecode
from fpdf import FPDF  # to create pdfs
from textblob_de import TextBlobDE as TextBlob  # for sentiment analysis
from matplotlib import pyplot as plt, dates, cm  # to plot figures
from wordcloud import WordCloud  # to create wordclouds
import emojis  # to find emoji in messages
import re  # for regex

from outputstyle import *  # for pretty printing
import database as db  # for access to local database


def time(task: str = "untitled") -> None:
	"""
	Adds a new entry to the time DataFrame.
	"""
	ts.append(timer())
	if task == "end":
		exp(exp_db=True)
		db.tt = pd.concat([db.tt, pd.DataFrame([["- -", "- -"], ["# main.py #", round(ts[-1] - ts[0], 6)], ["without imports", round(ts[-1] - ts[1], 6)]])])
		print(f"\nmain.py took {BOLD(round(ts[-1] - ts[0], 6))} sec to complete"
			  + f" (without the imports {BOLD(round(ts[-1] - ts[1], 6))} sec)\n\n")
		db.tt.to_csv("data/testing/time.csv", mode="a", header=False)
		return exit()
	db.tt.loc[len(db.tt)] = [task, round(ts[-1] - ts[-2], 6)]
	print(f"{BLUE(task)} took {BOLD(round(ts[-1] - ts[-2], 6))} sec")
	return


db.tt = pd.DataFrame(columns=[0, 1])
time("importing neccessary modules")


def exp(loc: str = None, data=None, name: str = None, exp_db: bool = False) -> None:
	"""
	Exports DataFrames and text to the data/testing/exports folder.
	"""
	if not exp_db:
		path = f"data/testing/exports/{loc}/"
		if type(data) != pd.DataFrame:
			data = pd.DataFrame(data)
		try:
			return data.to_csv(path + name, index=True)
		except FileNotFoundError:
			import os
			os.makedirs(path, exist_ok=True)
			return exp(loc, data, name)
	else:
		dbase = "database"
		exp(dbase, db.chat_og, "chat_og_df.csv")
		exp(dbase, db.chat, "chat_df.csv")
		exp(dbase, db.senders, "senders_df.csv")
		exp(dbase, db.stats, "stats_df.csv")
		exp(dbase, db.tstats, "time_stats_df.csv")
		exp(dbase, db.msg_ranges, "msg_ranges_df.csv")
		exp(dbase, db.txt_reports, "reports_df.csv")
		for i in range(db.sc+1):
			try:
				exp(dbase, db.msg_per_s[i], f"msg_per_s{i}.csv")
				exp(dbase, db.common_words[i], f"common_words_s{i}.csv")
				exp(dbase, db.common_emojis[i], f"common_emojis_s{i}.csv")
			except IndexError:
				pass
		time("exporting the database contents")
	return


def off(*args, file_end: bool = False) -> None:
	"""
	Prints error message and safely exits the program.
	"""
	return exit(BOLD(RED("⛔️ Error: ")) + " ".join(args) + " ⛔️" if len(args) > 0 else "") if not file_end else time("end")


def convert_file_to_df(path: str) -> None:
	"""
	Checks and converts a file of messages into a pandas DataFrame with the columns date, datetime, sender, message and sentiment.
	"""
	new_path = check_file_format(path)
	chat_list = convert_file_to_list(new_path)
	db.chat = convert_list_to_df(chat_list)
	prepare_database()

	time("converting the orinial file to a pandas DataFrame")
	return


def check_file_format(path_to_file: str) -> str:
	"""
	Checks if the format of the file is correct and returns correct path.
	"""
	if path_to_file.endswith(".txt"):
		return path_to_file
	elif path_to_file.endswith(".zip"):
		from zipfile import ZipFile
		with ZipFile(path_to_file, "r") as zip_ref:
			zip_ref.extractall("data/input")
		return "data/input/_chat.txt"
	else:
		return off("Only .txt or .zip files are supported")


def convert_file_to_list(path_to_file: str) -> list[list[str]]:
	"""
	Converts a .txt-file of messages into a list of messeages and returns it.
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
	# match pattern and devide into groups: 1:date, 2:datetime, 3:sender, 4:message
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
	df = pd.DataFrame(chat_list, columns=db.df_cols)  # convert into DataFrame
	df["date"] = pd.to_datetime(
		df["date"], infer_datetime_format=True, format="%d.%m.%Y")  # format date
	df["datetime"] = pd.to_datetime(
		df["datetime"], infer_datetime_format=True)  # format datetime
	return df


def prepare_database() -> None:
	"""
	Prepares the database by filling data in #tobefilled placeholders.
	"""
	db.chat["weekday"] = db.chat["date"].apply(lambda x: x.weekday())  # add weekday
	db.chat["hour"] = db.chat["datetime"].apply(lambda x: x.hour)  # add hour
	db.chat_og = db.chat.copy()  # Create copy of chat to use it later

	db.senders = list(db.chat["sender"].unique())  # Creates list of senders
	db.sc = len(db.senders)  # Number of senders

	db.stats = pd.DataFrame(None, db.senders, db.stats_dict.keys())
	db.tstats = pd.DataFrame(None, db.senders, db.tstats_cols)
	return


def analysis_per_sender() -> None:
	# data seperation, cleansing and data analysis per sender
	for i, s in enumerate(db.senders):
		df = db.chat.loc[db.chat["sender"] == s]  # DataFrame with messages from sender
		db.msg_per_s.append(df)

		clean_df = cleanse_df(df["message"], s) # get stats for each sender
		count_occurances(clean_df, i)  # count occurances of words and emojis
		time(f"sender no. {i}: counting occurances of media, words and emojis")

		calc_stats(clean_df.rename(s))  # calculate the stats for each sender
		time(f"sender no. {i}: calculating contactwise statistics")
	db.msg_per_s.append(db.chat_og)
	return


def count_occurances(df: pd.DataFrame, i: int) -> None:
	"""
	Calculates different statistics about the chat and enters collected data.
	"""
	all_msg = " ".join(df).lower()  # combine all messages into one string

	# count occurances of emojis
	emj_dct = dict()
	emj_lst = emojis.get(all_msg)  # get list of emojis
	for item in emj_lst:
		emj_dct[emojis.decode(item)] = all_msg.count(item)  # count emojis
	emoji_freq = pd.Series(emj_dct).sort_values(ascending=False).reset_index()
	emoji_freq.columns = ["Emoji", "Frequency"]
	db.common_emojis.append(emoji_freq)
	db.stats.at[db.senders[i], "emoji"] = sum(emj_dct.values())
	db.stats.at[db.senders[i], "emoji_unique"] = len(emj_dct)
	db.stats.at[db.senders[i], "link"] = len(re.findall("xurlx", all_msg))

	# count occurances of words
	all_msg = re.sub(r"(xurlx)|(\W)|(\d)", " ", unidecode(all_msg))
	word_freq = pd.Series(all_msg.split()).value_counts().reset_index()
	word_freq.columns = ["Word", "Frequency"]
	db.common_words.append(word_freq)

	create_wordcloud(all_msg.upper(), i)
	return


def cleanse_df(df: pd.DataFrame, sender: str) -> pd.DataFrame:
	"""
	Cleans the DataFrame of non-message enties and replaces URLs and enters
	collected data into the stats DataFrame.
	"""
	count = 0  # counter for media messages cleaned
	for key, val in db.cstats_match.items():
		if key == "media_count":  # media messages are counted separately
			db.stats.at[sender, key] = count
		else:
			key_df = df[df == val[1]] if val[0] == "exact" else df[df.str.contains(val[1])]
			df = df.drop(key_df.index) # remove non-messages
			db.chat = db.chat.drop(key_df.index) # remove non-messages
			if key in db.stats.columns:  # add counted data to stats_df.if it exists
				db.stats.at[sender, key] = key_df.shape[0]
				count += key_df.shape[0]
	return df


def calc_stats(s_df: pd.DataFrame) -> None:
	"""
	Calculates different statistics about the chat and enters collected data
	into the stats DataFrame.
	"""
	s = s_df.name  # get column name (sender)
	db.stats.at[s, "msg_count"] = s_df.shape[0]
	db.stats.at[s, "chars_avg"] = round(s_df.str.replace(" ", "").str.len().mean(), 2)
	db.stats.at[s, "words_avg"] = round(s_df.str.split().str.len().mean(), 2)
	db.stats.at[s, "chars_max"] = s_df.str.replace(" ", "").str.len().max()
	db.stats.at[s, "words_max"] = len(s_df[s_df.str.len().idxmax()].split())
	db.stats.at[s, "sent_avg"] = round(db.chat.loc[db.chat["sender"] == s, "sentiment"].mean(skipna=True), 2)
	db.stats.at[s, "sent_pos"] = db.chat.loc[db.chat["sender"] == s, "sentiment"].gt(0).sum()
	db.stats.at[s, "sent_neg"] = db.chat.loc[db.chat["sender"] == s, "sentiment"].lt(0).sum()

	return


def calc_remaining_stats() -> None:
	"""
	Calculates summary statistics about the chat and enters collected data
	into the stats DataFrame.
	"""
	for i in range(db.sc+1):
		row = db.senders[i] if i < db.sc else "sum"
		msg_r = create_msg_range(i)
		db.msg_ranges.append(msg_r)

		db.tstats.at[row, "first_msg"] = str(msg_r.index[0]).split()[0]
		db.tstats.at[row, "last_msg"] = str(msg_r.index[-1]).split()[0]
		db.tstats.at[row, "msg_span_days"] = (msg_r.index[-1] - msg_r.index[0]).days

		db.tstats.at[row, "max_day"] = str(msg_r[msg_r == msg_r.max()].index[0]).split()[0]
		db.tstats.at[row, "max_msg"] = msg_r.max()

		db.tstats.at[row, "msg_days"] = msg_r[msg_r != 0].shape[0]
		db.tstats.at[row, "zero_days"] = msg_r[msg_r == 0].shape[0]

	
	for stat in db.stats_dict.keys():
		if any(x in stat for x in ["calls", "unique"]):
			continue
		elif "max" in stat:
			db.stats.at["sum", stat] = db.stats[stat].max()
		elif "avg" in stat:
			db.stats.at["sum", stat] = round(db.stats[stat].mean(), 3)
		else:
			db.stats.at["sum", stat] = db.stats[stat].sum()

	time("calculating remaining statistics for all senders")
	return


def create_msg_range(i: int) -> None:
	msg_date = db.msg_per_s[i]["date"].value_counts().sort_index()
	chat_date_range = pd.date_range(msg_date.index[0], msg_date.index[-1])
	msg_range = pd.Series(index=chat_date_range, dtype=int)
	for date in chat_date_range.strftime("%Y-%m-%d"):
		msg_range[date] = msg_date[date] if date in msg_date.index else 0
	return msg_range


# ----------------------------------------------------------------
#                          word statistics
# ----------------------------------------------------------------


def create_wordcloud(words: str, i: int) -> None:
	"""
	Creates a word cloud of the given words and saves it to the plots folder.
	"""
	x, y = np.ogrid[:1000, :1000]
	mask = (x - 500) ** 2 + (y - 500) ** 2 > 400 ** 2
	mask = 255 * mask.astype(int)

	wc = WordCloud(None, 200, 200, prefer_horizontal=.7,
				   colormap="summer", mode="RGBA", mask=mask, background_color=None,
				   stopwords=db.stop_words, min_word_length=2,).generate(words)
	wc.to_file(f"data/output/images/senderpages/s{str(i)}_wc.png")
	return


# --------------------------------------------
# Functions used to print the ouptut in a specific format
# --------------------------------------------


def ss(style: int = 0) -> str:
	"""
	Returns a string represtaion of the senders
	style= 0: auto (default), 1: the n senders, 2: s_no1, s_no2 and s_no3 etc.
	"""
	short, long = f"the {str(db.sc)} senders", pprint(*db.senders)
	if style != 0:
		return short if style == 1 else long
	else:
		return long if db.sc < 3 else short


def calc_num(n: int, term: str) -> str:
	"""
	Returns the correct plural form of a word depending on the amount passed.
	"""
	s = (str(n) if not n < 0 else ("one" if n == 1 else "no")) + " " + term
	return s + ("s" if n != 1 and term not in ("media", "sentiment") else "")


def get_stat_pair(stat: int, sender: int) -> tuple[int, str]:
	"""
	Returns the value and term of a specific statistic.
	"""
	return db.stats.iat[sender, stat], list(db.stats_dict.values())[stat]


def create_txt_reports() -> None:
	"""
	Creates a report about the sender at the given index which includes the
	statistics about their messages or a summary report.
	"""
	i = int()

	def y(*idxs): return pprint(*[calc_num(*get_stat_pair(a, i)) for a in idxs])

	def x(*idxs): return pprint(*[db.stats.iat[i, a] for a in idxs])

	for i, s in enumerate(db.senders):  # for each sender create a sender report
		ls = [y(0, 6, 18), "\n".join([
			f"Avg. message length: {y(2)} ({y(1)})",
			f"Longest message: {y(4)} ({y(3)})",
			f"{x(15)} deleted messages",
			f"{s} deleted {y(15)}.",
			])]
		if db.stats.iat[i, 16] != 0:
			ls.append(f"You missed {y(16)} by {s}.") #TODO check this
		db.txt_reports.append(ls)

	# General report about all chat messages
	i = db.sc
	db.txt_reports.append([y(0, 6, 18), "\n".join([
		f"Avg. message length: {y(2)} ({y(1)})",
		f"Longest message: {y(4)} ({y(3)})",
		f"{x(15)} deleted messages",
		f"{ss()} deleted {y(15)}."])])
	return


def create_time_reports() -> None:
	"""
	Creates a report about the sender at the given index which includes the
	statistics about their messages or a summary report.
	"""
	for i in range(db.sc+1):  # for each sender create a sender report 
		db.time_reports.append("\n".join([
			f"First message: {db.tstats.iat[i, 0]}",
			f"Last message: {db.tstats.iat[i, 1]}",
			f"Most messages sent on {db.tstats.iat[i, 2]} ({db.tstats.iat[i, 3]})",
			f"Messages sent on {db.tstats.iat[i, 4]} days",
			f"No messages sent on {db.tstats.iat[i, 5]} days"]))
	return


# ----------------------------------------------------------------
# 				Functions to create images for the report
# ----------------------------------------------------------------


def visualise_data() -> None:
	"""
	Creates a texual output for some data and plots the grafics for the report.
	"""
	create_txt_reports()
	create_time_reports()

	msg_pie()
	grouped_madia_bars()
	message_time_series()
	activity_heatmaps()
	sent_pies()
	
	time("visualising data for the final pdf report")
	return


def cmap(countable=db.senders, cm_name: str = "Greens_r") -> Colormap:
	"""
	Returns a colormap for the amount needed of the given countable.
	"""
	if type(countable) != int:
		countable = len(countable)
	return cm.get_cmap(cm_name)(np.linspace(.2, .8, countable+1))


def msg_pie() -> None:
	"""
	Creates a pie chart of the amount of messages sent by each sender.
	"""
	fig, ax = plt.subplots(figsize=(3.14, 3.14))
	ax.pie(db.stats.iloc[0:-1, 0], startangle=90, colors=cmap(db.senders),
		   counterclock=False, autopct="%1.2f%%", wedgeprops={"ec": "w"}, textprops={"c": "w"})
	ax.legend(labels=db.senders, shadow=True, loc="upper right", fontsize="small")
	ax.set_title("Messages sent")
	ax.axis("equal")
	fig.tight_layout()
	plt.savefig("data/output/images/page1/msg_pie.png", transparent=True)
	plt.close()
	return


def grouped_madia_bars() -> None:
	"""
	Creates a bar chart of the amount of media messages sent by each sender.
	"""
	nums = [11, 7, 8, 10, 9, 17, 12, 13, 14]
	labels = [list(db.stats_dict.values())[x].capitalize() for x in nums]
	w = .9  # the width of the bars
	x = np.arange(len(nums))  # the label locations
	max_val = db.stats.iloc[:db.sc, nums].max().max()

	fig, ax = plt.subplots(figsize=(8.27, 2))
	for i, s in enumerate(db.senders):
		rect = ax.bar((x-w/2) + i*w/db.sc,
					  db.stats.iloc[i, nums], w/db.sc, label=s, align="edge")
		ax.bar_label(rect, padding=1) if any(
			[db.sc < 4 and max_val < 1000, db.sc < 6 and max_val < 100, max_val < 10]) else None

	ax.set_title("Media types sent by sender", loc="left")
	ax.set_ylabel("amount")
	ax.set_xticks(x)
	ax.set_yticks(np.arange(0, max_val, 50), minor=True)
	ax.set_ylim([0, max_val+35])
	ax.grid(True, "both", "y", lw=.8)
	ax.set_xticklabels(labels)
	if db.sc < 7:
		ax.legend(bbox_to_anchor=(1, 1.2), fontsize="small", ncol=db.sc, shadow=True)
	else:
		ax.legend(bbox_to_anchor=(1, 1.3), fontsize="small", ncol=round(db.sc/2), shadow=True)

	plt.savefig("data/output/images/page1/media_bars.png", transparent=True)
	plt.close()
	return

def message_time_series() -> None:
	"""
	Creates a time series plot of the messages sent over time by each sender
	individually and together.
	"""
	for i, range in enumerate(db.msg_ranges):
		fig, ax = plt.subplots(figsize=(8.27, 2))

		ax.plot(range.index, range.values, color="green")
		# Major ticks every half year, minor ticks every month
		ax.xaxis.set_major_locator(dates.MonthLocator((1, 5, 9), 15))
		ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
		ax.grid(True, "both", "y")
		ax.set_ylabel("amount")
		ax.set_title("Messages sent over time", loc="left")
		ax.xaxis.set_major_formatter(dates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

		page = "page1/" if i == db.sc else f"senderpages/s{str(i)}_"
		fig.savefig(f"data/output/images/{page}ts.png", transparent=True)
		plt.close()
	return


def activity_heatmaps() -> None:
	"""
	Creates a heatmap of the activity of the chat members individually and
	together.
	"""
	days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	hours = [str(i) for i in range(24)]

	for n in range(db.sc+1):
		df = db.msg_per_s[n] if n != db.sc else db.chat_og

		fig, ax = plt.subplots(figsize=(8, 2))
		vals = df.groupby(["weekday", "hour"]).size(
		).unstack().fillna(0).astype(int)
		im = ax.imshow(vals, cmap="Greens")

		# Show all ticks and label them with the respective list entries
		ax.set_xticks(np.arange(len(hours)), labels=hours)
		ax.set_yticks(np.arange(len(days)), labels=[x[:3] for x in days])

		val_max = vals.max().max()

		if val_max < 100:
			for i in range(len(days)):
				for j in range(len(hours)):
					x = vals.iat[i, j] if vals.iat[i, j] != 0 else ""
					ax.text(j, i, x, ha="center", va="center",
							color="black" if vals.iat[i, j] < val_max/2.5 else "w")

		cbar = fig.colorbar(im)
		cbar.ax.set_ylabel("Amount", rotation=-90, va="bottom")

		ax.set_title("Activity by day and hour", loc="left")

		page = "page1/" if n == db.sc else f"senderpages/s{str(n)}_"
		fig.savefig(f"data/output/images/{page}heatmap.png", transparent=True)
		plt.close()
	return


def sent_pies() -> None:
	"""
	Creates a pie chart of the sentiment of the messages sent by each sender
	individually and together.
	"""
	for n in range(db.sc+1):
		fig, ax = plt.subplots(figsize=(3.14, 3.14))
		ax.pie(db.stats.iloc[n, [20, 22]], startangle=90, colors=["darkgreen", "darkred"], autopct="%1.1f%%", wedgeprops={"ec": "w"}, textprops={"c": "w"})
		ax.legend(labels=["☺️", "☹"], shadow=True, loc="upper right", fontsize="small")
		ax.axis("equal")
		ax.set_title("Sentiment of rated messages")
		fig.tight_layout()
		page = "page1/" if n == db.sc else f"senderpages/s{str(n)}_"
		fig.savefig(f"data/output/images/{page}sent_pie.png", transparent=True)
		plt.close()
	return


# --------------------------------------------
#		Functions used to create pdf ouptut
# --------------------------------------------


pdf = FPDF()

xys: list[tuple[int, int]] = list()  # last x, y coordinates
sizes: list[int] = list()  # last text sizes


def get_coord(x_offset: int = 0, y_offset: int = 0) -> tuple[int, int]:
	"""
	Returns the x, y cordinates on the current page
	"""
	return (pdf.get_x() + x_offset), (pdf.get_y() + y_offset)


def new_section(size: int = 0, style: str = "", space: int = 0, np: int = 0) -> None:
	"""
	Creates a new section in the pdf file and sets the font size and style.
	np: 0 = no new page (default), 1 = new page, 2 = new page and new section
	"""
	pdf.add_page() if np in (1, 2) else None  # create new page
	if np in (0, 2):  # create new section	on current or new page
		pdf.ln(space)
		xys.append({0: pdf.get_x(), 1: pdf.get_y()})
		sizes.append(size) if size != 0 else None
		pdf.set_font("Arial", style, size if size != 0 else sizes[-1])
	return None


def add_title_footer(n: int = -1) -> None:
	"""
	Prints the title of the page
	"""
	pdf.set_margins(15, 20, 15) if pdf.page_no() == 0 else None
	pdf.add_page()

	# Create title of current page
	new_section(18, "B")
	pdf.cell(0, 10, "WhatsApp Chat Statistics", align="C")
	new_section(12, space=5)
	pdf.cell(0, 12, "for " + str(ss() if n == -1 else db.senders[n]), align="C")

	# Create footer of current page
	pdf.set_xy(0, 270)
	new_section(10, "I")
	pdf.cell(0, 5, f"Page {pdf.page_no()}", align="C")
	pdf.set_xy(*xys[-2].values())
	return


def print_stats(s_no: int = -1, w: int = 24, h: int = 6) -> None:
	"""
	Prints the statistics of a sender to the pdf file
	"""
	for i, x in enumerate([11, 12, 7, 13, 8, 14, 10, 17, 9]):
		if i == 0:
			pdf.set_font("Arial", "", 12)
			pdf.cell(w*4, h+2, "Media types and amount sent", 0, 1, "C")
			pdf.set_font("Arial", "", 11)
		value = str(db.stats.iat[db.sc if s_no == -1 else s_no, x])
		item = list(db.stats_dict.values())[x] + "s" if value != 1 else ""
		pdf.cell(w, h, item.capitalize(), 1, 0, "C")
		pdf.cell(w, h, value, 1, 0, "C")
		if i % 2 != 0:
			pdf.ln(h)
	return


def print_tstats(s_no: int = -1) -> None:
	"""
	Prints the timewise statistics of a sender to the pdf file
	"""
	n = db.sc if s_no == -1 else s_no
	x1 = 35
	x2 = 20
	h = 6
	pdf.set_font("Arial", "", 12)
	i = 0
	for key, val in db.tstats_dict.items():
		pdf.cell(x1, h, val.capitalize(), 1, 0, "C")
		pdf.cell(x2, h, str(db.tstats.iloc[n, key]), 1, 0, "C")
		if i % 2 != 0:
			pdf.ln(h)
		i += 1
	return


def print_cmms(df: pd.DataFrame, cell_width: int = 25, cell_height: int = 6) -> None:
	"""
	Prints a DataFrame of common words/emojis to a table in a pdf file
	"""
	margin, _ = get_coord()
	pdf.set_font("Arial", "B", 8)
	pdf.cell(cell_width, cell_height, df.columns[0], align="C", border=1)
	pdf.cell(17, cell_height, df.columns[1], align="C", border=1)
	pdf.set_xy(margin, pdf.get_y() + cell_height)

	pdf.set_font("Arial", "", 8)
	for i in range(len(df)):
		pdf.cell(cell_width, cell_height, 
			df.iat[i, 0].strip(":").replace("_", " ")[:20], align="C", border=1)
		pdf.cell(17, cell_height, str(df.iat[i, 1]), align="C", border=1)
		pdf.set_xy(margin, pdf.get_y() + cell_height)
	return


def make_pdf_report() -> None:
	"""
	Creates a pdf file with a summary of the chat and the statistics
	"""
	add_title_footer()
	path = "data/output/images/page1/"

	new_section(11, space=20)
	pdf.cell(90, 0, "This conversation contains")
	new_section(14, "B", space=3)
	pdf.multi_cell(110, 5, db.txt_reports[db.sc][0])

	new_section(11, space=4)
	pdf.multi_cell(100, 4, db.txt_reports[db.sc][1])

	new_section(space=4)
	pdf.multi_cell(100, 4, db.time_reports[db.sc])

	# new_section(space=4)
	# print_tstats()

	pdf.image(path+"msg_pie.png", x=115, y=35, w=84)
	pdf.image(path+"media_bars.png", x=0, y=120, w=210)
	pdf.image(path+"ts.png", x=0, y=180, w=210)

	for i, s in enumerate(db.senders):
		add_title_footer(i)
		path = f"data/output/images/senderpages/s{str(i)}_"

		new_section(11, space=20)
		pdf.cell(90, 0, f"Messages sent from {s} contain")
		new_section(14, "B", space=3)
		pdf.multi_cell(110, 5, db.txt_reports[i][0])

		new_section(space=4)
		print_stats(i)

		new_section(11, space=10)
		pdf.multi_cell(110, 4, db.txt_reports[i][1])

		# pdf.image(path+"wc.png", x=113, y=33, w=88)
		pdf.image(path+"sent_pie.png", x=115, y=35, w=84)


		pdf.image(path+"wc.png", x=113, y=140, w=88)

		pdf.set_xy(20, 160)
		print_cmms(db.common_words[i].head(10), cell_width=25, cell_height=5)

		pdf.set_xy(65, 160)
		print_cmms(db.common_emojis[i].head(10), cell_width=25, cell_height=5)




		# pdf.image(path+"ts.png", x=0, y=130, w=210)
		# pdf.image(path+"heatmap.png", x=0, y=180, w=210)

		
		add_title_footer(i) # new page 

		new_section(11, space=20)
		pdf.multi_cell(100, 4, db.time_reports[i])



		# pdf.set_xy(20, 40)
		# print_cmms(db.common_words[i].head(10), cell_width=25, cell_height=5)

		# pdf.set_xy(65, 40)
		# print_cmms(db.common_emojis[i].head(10), cell_width=25, cell_height=5)

		# pdf.image(path+"wc.png", x=50, y=100, w=150)


		pdf.image(path+"ts.png", x=0, y=130, w=210)
		pdf.image(path+"heatmap.png", x=0, y=185, w=210)


	pdf.output("data/output/pdfs/WA-Report.pdf", "F",)
	time("finishing final PDF Report")
	return
