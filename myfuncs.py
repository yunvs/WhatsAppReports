from timeit import default_timer as timer

from unidecode import unidecode # for timing
ts = [timer()]

import database as db  # for access to local database
from outputstyle import * # for pretty printing
import numpy as np, pandas as pd # to create DataFrames
import re # for regex
import emojis # to find emoji in messages
from wordcloud import WordCloud # to create wordclouds
from matplotlib import pyplot as plt, dates, cm # to plot figures
from textblob_de import TextBlobDE as TextBlob # for sentiment analysis

from fpdf import FPDF # to create pdfs


# Unused imports
# import matplotlib
# import os
# from plotly import express as px 
# from germansentiment import SentimentModel
# model = SentimentModel()

def time(task: str="untitled") -> None:
	"""
	Adds a new entry to the time DataFrame.
	"""
	ts.append(timer())
	if task == "end":
		export(exp_db=True)
		db.tt = pd.concat([db.tt, pd.DataFrame([["- -", "- -"], 
		["# main.py #", round(ts[-1] - ts[0], 6)], ["without imports", round(ts[-1] - ts[1], 6)]])])
		print(f"\nmain.py took {BOLD(round(ts[-1] - ts[0], 6))} sec to complete"
		+ f" (without the imports {BOLD(round(ts[-1] - ts[1], 6))} sec)\n\n")
		db.tt.to_csv("data/testing/time.csv", mode="a", header=False)
		return exit()
	db.tt.loc[len(db.tt)] = [task, round(ts[-1] - ts[-2], 6)]
	print(f"{BLUE(task)} took {BOLD(round(ts[-1] - ts[-2], 6))} sec")
	return


db.tt = pd.DataFrame(columns=[0, 1])
time("importing neccessary modules")


def export(loc: str=None, data=None, name: str=None, exp_db: bool=False) -> None:
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
			return export(loc, data, name) 
	else:
		export("database", db.chat_og, "chat_og_df.csv")
		export("database", db.chat, "chat_df.csv") 
		export("database", db.senders, "senders_df.csv")
		export("database", db.stats_df, "stats_df.csv") 
		export("database", db.time_stats_df, "time_stats_df.csv")
		export("database", db.msg_ranges, "msg_ranges_df.csv")
		export("database", db.reports, "reports_df.csv")
		export("database", db.chat_per_s_clean, f"chat_per_s_clean_df.csv")
		for i in range(db.sc+1):
			try:
				export("database", db.chat_per_s[i], f"chat_per_s{i}.csv")
				export("database", db.common_words[i], f"common_words_s{i}.csv")
				export("database", db.common_emojis[i], f"common_emojis_s{i}.csv")
				# export("database", db.msg_bundles[i], f"msg_bundles_s{i}.csv")
			except IndexError:
				pass
		time("exporting the database contents")
	return


def off(*args, file_end: bool=False) -> None:
	"""
	Prints error message and safely exits the program.
	"""
	return exit(BOLD(RED("⛔️ Error: ")) + " ".join(args) + " ⛔️" if len(args) > 0 else "") if not file_end else time("end")


def convert_file_to_df(path: str) -> None:
	"""
	Checks and converts a file of messages into a pandas DataFrame with the columns date, datetime, sender, message and sentiment.
	"""
	new_path = check_file_format(path) # check if the file is in the correct format
	chat_list = convert_file_to_list(new_path) # convert the file to a list
	db.chat = convert_list_to_df(chat_list) # convert the list to a DataFrame
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
				if re.match("^.? ?\[([\d./]*), ([\d:]*)\] .*", line):  # line begins with a new message
					chat.append(convert_ln(last_msg)) if last_msg != "" else None  # add buffer to list
					last_msg = line.strip().strip("\n").strip()  # add new message to buffer
				else:  # line is the continuation of the last message
					last_msg += " " + line.strip().strip("\n").strip()  # add line to buffer
			chat.append(convert_ln(last_msg)) if chat[-1] != convert_ln(last_msg) else None # add buffer to list if it is not added yet
	except FileNotFoundError:  # file does not exist
		return off("File not found\nCheck the path to the file")
	except (UnicodeDecodeError, UnicodeError):  # file is not in UTF-8
		return off("File not in UTF-8 format\nTry uploading the original file")
	return chat


def convert_ln(input: str) -> list[str]:
	"""
	Converts a line of the WhatsApp chat history into a list and returns it.
	"""
	x = re.search("^.? ?\[([\d./]*), ([\d:]*)\] ([\w ]*): (\u200E?.*)$", input) # match pattern and devide into groups: 1:date, 2:datetime, 3:sender, 4:message
	result = [x.group(1), " ".join([x.group(1), x.group(2)])]  # add date, datetime
	result.append(x.group(3).title())  # add name of sender
	message = re.sub("https?://\S+", "xURLx", x.group(4))  # replace URLs
	result.append(message)  # add message
	if len(message) > 2 and message.upper().isupper():
		result.append(TextBlob(message.replace("xURLx", "")).sentiment.polarity)  # add sentiment
	else:
		result.append(pd.NA)
	return result


def convert_list_to_df(chat_list: list) -> pd.DataFrame:
	"""
	Converts the list of messages into a pandas DataFrame and returns it.
	"""
	df = pd.DataFrame(chat_list, columns=db.df_cols) # convert the list to a DataFrame
	df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True, format="%d.%m.%Y")  # format date
	df["datetime"] = pd.to_datetime(df["datetime"], infer_datetime_format=True)  # format datetime
	return df


def prepare_database() -> None:
	"""
	Prepares the database by filling data in #tobefilled placeholders.
	"""
	db.chat["weekday"] = db.chat["date"].apply(lambda x: x.weekday()) # add weekday
	db.chat["hour"] = db.chat["datetime"].apply(lambda x: x.hour) # add hour
	db.chat_og = db.chat.copy() # Create copy of chat to use it later

	db.senders = list(db.chat["sender"].unique()) # Creates list of senders
	db.sc = len(db.senders) # Number of senders
	
	db.stats_df = pd.DataFrame(index=db.senders, columns=db.stats_dict.keys())
	db.time_stats_df = pd.DataFrame(index=db.senders, columns=db.time_stats_cols)
	return


def seperate_data() -> None:
	# data seperation, cleansing and data analysis per sender
	for i, s in enumerate(db.senders):
		df = db.chat.loc[db.chat["sender"] == s]  # DataFrame with messages from sender
		db.chat_per_s.append(df)
		clean_df = cleanse_df(df["message"], s)  # get the stats for each sender
		count_occurances(clean_df, i) # count the occurances of words and emojis
		calc_stats(clean_df) # calculate the stats for each sender

	db.chat_per_s.append(db.chat_og)
	return


def count_occurances(df: pd.DataFrame, i: int) -> None:
	"""
	Calculates different statistics about the chat and enters collected data.
	"""
	messages = " ".join(df).lower()

	# count emojis
	emoji_dict = dict()
	emojis_listed = emojis.get(messages) # get list of emojis
	for item in emojis_listed:
		emoji_dict[emojis.decode(item)] = messages.count(item) # count the emojis
	emoji_freq = pd.Series(emoji_dict).sort_values(ascending=False).reset_index()
	emoji_freq.columns = ["Emoji", "Frequency"]
	db.common_emojis.append(emoji_freq)
	db.stats_df.at[db.senders[i], "emoji"] = sum(emoji_dict.values())
	db.stats_df.at[db.senders[i], "emoji_unique"] = len(emoji_dict)
	db.stats_df.at[db.senders[i], "link"] = len(re.findall("xurlx", messages))

	# count words
	messages = re.sub(r"(xurlx)|(\W)|(\d)", " ", unidecode(messages))
	word_freq = pd.Series(messages.split()).value_counts().reset_index()
	word_freq.columns = ["Word", "Frequency"]
	db.common_words.append(word_freq)

	time(f"counting word and emoji occurances for sender{str(i+1)}")
	
	create_wordcloud(messages.upper(), i)
	time(f"creating wordcloud for sender{str(i+1)}")
	return


def cleanse_df(DataFrame: pd.DataFrame, sender: str) -> pd.DataFrame:
	"""
	Cleans the DataFrame of non-message enties and replaces URLs and enters 
	collected data into the stats DataFrame.
	"""
	count = 0  # counter for media messages cleaned
	df = DataFrame.copy().rename(sender)
	for key, val in db.cstats_match.items():
		if key == "media_count": # media messages are counted separately
			db.stats_df.at[sender, key] = count
		else:
			key_df = df[df == val[1]] if val[0] == "exact" else df[df.str.contains(val[1])]
			df = df.drop(key_df.index)  # remove non-messages from clean_df
			db.chat = db.chat.drop(key_df.index) # remove non-messages from chat_df
			if key in db.stats_df.columns:  # add counted data to stats_df.if it exists
				db.stats_df.at[sender, key] = key_df.shape[0]
				count += key_df.shape[0]
	
	db.chat_per_s_clean.append(df)  #TODO do i really need chat_per_s_clean?

	time(f"cleaning df for sender{db.senders.index(sender)+1}")
	return df


def calc_stats(sender_df: pd.DataFrame) -> None:
	"""
	Calculates different statistics about the chat and enters collected data 
	into the stats DataFrame.
	"""
	s = sender_df.name # get column name (sender)
	db.stats_df.at[s,"msg_count"] = sender_df.shape[0]
	db.stats_df.at[s,"chars_avg"] = round(sender_df.str.replace(" ", "").str.len().mean(), 2)
	db.stats_df.at[s,"words_avg"] = round(sender_df.str.split().str.len().mean(), 2)
	db.stats_df.at[s,"chars_max"] = sender_df.str.replace(" ", "").str.len().max()
	db.stats_df.at[s,"words_max"] = len(sender_df[sender_df.str.len().idxmax()].split())
	db.stats_df.at[s,"sent_avg"] = round(db.chat.loc[db.chat["sender"] == s, "sentiment"].mean(skipna=True), 2)
	db.stats_df.at[s,"sent_pos"] = db.chat.loc[db.chat["sender"] == s, "sentiment"].gt(0).sum()
	db.stats_df.at[s,"sent_neg"] = db.chat.loc[db.chat["sender"] == s, "sentiment"].lt(0).sum()
	db.stats_df.at[s,"sent_neu"] = db.chat.loc[db.chat["sender"] == s, "sentiment"].eq(0).sum() #TODO remove if not needed
	db.stats_df.at[s,"sent_nan"] = db.chat.loc[db.chat["sender"] == s, "sentiment"].isna().sum() #TODO remove if not needed
	
	time(f"calculating statistics for sender{db.senders.index(s)+1}")
	return


def calc_sum_stats() -> None:
	"""
	Calculates summary statistics about the chat and enters collected data
	into the stats DataFrame.
	"""
	for stat in db.stats_dict.keys():
		if any(x in stat for x in ["calls", "unique"]):
			continue
		elif "max" in stat:
			db.stats_df.at["sum", stat] = db.stats_df[stat].max()
		elif "avg" in stat:
			db.stats_df.at["sum", stat] = round(db.stats_df[stat].mean(), 3)
		else:
			db.stats_df.at["sum", stat] = db.stats_df[stat].sum()
	

	return time("calculating summary statistics for all senders")


def create_msg_range(i: int) -> None:
	msg_date = db.chat_per_s[i]["date"].value_counts().sort_index()
	chat_date_range = pd.date_range(msg_date.index[0], msg_date.index[-1])
	msg_range = pd.Series(index=chat_date_range, dtype=int)
	for date in chat_date_range.strftime("%Y-%m-%d"):
		msg_range[date] = msg_date[date] if date in msg_date.index else 0
	return msg_range


def calc_time_stats() -> None:
	"""
	Extracts the first and last message date from the message per date series.
	"""
	for i in range(db.sc+1):
		row = db.senders[i] if i < db.sc else "sum"
		msg_range = create_msg_range(i)
		db.msg_ranges.append(msg_range)

		db.time_stats_df.at[row, "first_msg"] = msg_range.index[0]
		db.time_stats_df.at[row, "last_msg"] = msg_range.index[-1]

		db.time_stats_df.at[row, "max_day"] = msg_range[msg_range == msg_range.max()].index[0]
		db.time_stats_df.at[row, "max_msg"] = msg_range.max()

		db.time_stats_df.at[row, "zero_days"] = msg_range[msg_range == 0].shape[0]
		db.time_stats_df.at[row, "not_zero_days"] = msg_range[msg_range != 0].shape[0]

		# get the amount of days between the first and last message
		db.time_stats_df.at[row, "msg_days"] = (db.time_stats_df.at[row, "last_msg"] - db.time_stats_df.at[row, "first_msg"]).days

	time("calculating time statistics for all senders")
	return


# ----------------------------------------------------------------
#                          word statistics
# ----------------------------------------------------------------


def create_wordcloud(words: str, i:int) -> None:
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


def ss(style: int=0) -> str:
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
	return db.stats_df.iat[sender, stat], list(db.stats_dict.values())[stat]


def create_txt_reports() -> None:
	"""
	Creates a report about the sender at the given index which includes the 
	statistics about their messages or a summary report and returns it.
	"""
	i = int()

	def y(*idxs): return pprint(*[calc_num(*get_stat_pair(x, i)) for x in idxs])
	def x(*idxs): return pprint(*[db.time_stats_df[i,z] for z in idxs])

	for i, s in enumerate(db.senders): # for each sender create a sender report
		db.reports.append([y(0,6,18),"\n".join([
			f"Ø message length: {y(2)} ({y(1)})",
			f"Longest message: {y(4)} ({y(3)})",
			f"Deleted messages: {y(15)}",
			f"Ø sentiment: {y(5)}",
			]),
			f"{s} deleted {y(15)}.",
			])
		if db.stats_df.iat[i, 16] != 0:
			db.reports[-1].append(f"You missed {y(16)} by {s}.")
	
	# General report about all chat messages
	i = db.sc
	db.reports.append([y(0,6,18),"\n".join([
		f"Ø message length: {y(2)} ({y(1)})",
		f"Longest message: {y(4)} ({y(3)})",
		f"Deleted messages: {y(15)}",
		f"Ø sentiment: {y(5)}",
		]),
		f"{ss()} deleted {y(15)}.",
	])
	
	time("creating a text report")
	return


# ----------------------------------------------------------------
# 				Functions to create images for the report
# ----------------------------------------------------------------


def plot_data() -> None:
	"""
	Creates the plots for the report.
	"""
	msg_pie()
	grouped_madia_bars()
	message_time_series()
	activity_heatmaps()
	sentiment_pies()
	return time("making plots for the report")


def cmap(countable=db.senders, cm_name: str="Greens_r"):
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
	ax.pie(db.stats_df.iloc[0:-1, 0], startangle=90, colors=cmap(db.senders), counterclock=False, autopct="%1.2f%%", wedgeprops={"ec":"w"}, textprops={"c":"w"})
	ax.legend(labels=db.senders, title="sender", shadow=True, loc="upper right", fontsize="small")
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
	w = .9 # the width of the bars
	x = np.arange(len(nums)) # the label locations
	max_val = db.stats_df.iloc[:db.sc, nums].max().max()

	fig, ax = plt.subplots(figsize=(8.27, 2))
	for i, s in enumerate(db.senders):
		rect = ax.bar((x-w/2) + i*w/db.sc, db.stats_df.iloc[i, nums], w/db.sc, label=s, align="edge")
		ax.bar_label(rect, padding=1) if any([db.sc < 4 and max_val < 1000, db.sc < 6 and max_val < 100, max_val < 10]) else None

	ax.set_title("Media types sent by sender", loc="left"); ax.set_ylabel("amount")
	ax.set_xticks(x); ax.set_yticks(np.arange(0, max_val, 50), minor=True)
	ax.set_ylim([0, max_val+35]); ax.grid(True, "both", "y", lw=.8)
	ax.set_xticklabels(labels)
	if db.sc < 7:
		ax.legend(bbox_to_anchor=(1,1.2), fontsize="small", ncol=db.sc)
	else:
		ax.legend(bbox_to_anchor=(1,1.3), fontsize="small", ncol=round(db.sc/2))

	plt.savefig("data/output/images/page1/media_bars.png", transparent=True)
	plt.close()


def message_time_series() -> None:
	"""
	Creates a time series plot of the messages sent over time by each sender 
	individually and together.
	"""
	for i, range in enumerate(db.msg_ranges):
		fig, ax = plt.subplots(figsize=(8.27,2))

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
		plt.close(fig)
	return


days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
hours = [str(i) for i in range(24)]

def activity_heatmaps() -> None:
	"""
	Creates a heatmap of the activity of the chat members individually and 
	together.
	"""
	for n in range(db.sc+1):
		df = db.chat_per_s[n] if n != db.sc else db.chat_og
		
		fig, ax = plt.subplots(figsize=(7, 2))
		vals = df.groupby(["weekday", "hour"]).size().unstack().fillna(0).astype(int)
		im = ax.imshow(vals, cmap="Greens")

		# Show all ticks and label them with the respective list entries
		ax.set_xticks(np.arange(len(hours)), labels=hours)
		ax.set_yticks(np.arange(len(days)), labels=[x[:3] for x in days])

		val_max = vals.max().max()
		
		if val_max < 100:
			for i in range(len(days)):
				for j in range(len(hours)):
					x = vals.iat[i,j] if vals.iat[i,j] != 0 else ""
					ax.text(j, i, x, ha="center", va="center", 
						color="black" if vals.iat[i,j] < val_max/2.5 else "w")

		cbar = fig.colorbar(im)
		cbar.ax.set_ylabel("messages sent", rotation=-90, va="bottom")

		# ax.set_title("Activity by day and hour", loc="left")

		page = "page1/" if n == db.sc else f"senderpages/s{str(n)}_"
		fig.savefig(f"data/output/images/{page}heatmap.png", transparent=True)
		plt.close()
	return

def sentiment_pies() -> None:
	"""
	Creates a pie chart of the sentiment of the messages sent by each sender 
	individually and together.
	"""
	for n in range(db.sc+1):
		fig, ax = plt.subplots(figsize=(3.14, 3.14))
		ax.pie(db.stats_df.iloc[n, [20, 22]], labels=["😀", "☹"], startangle=90, colors=["g","r"], autopct="%1.1f%%")
		ax.axis("equal")
		fig.tight_layout()
		page = "page1/" if n == db.sc else f"senderpages/s{str(n)}_"
		fig.savefig(f"data/output/images/{page}polpie.png", transparent=True)
		plt.close()
	return

# def bar_plotter(results, category_names):
#     labels = list(results.keys())
#     data = np.array(list(results.values()))
#     data_cum = data.cumsum(axis=1)
#     category_colors = cmap(data.shape[1])
#     fig, ax = plt.subplots(figsize=(9.2, 5))
#     ax.xaxis.set_visible(False)
#     ax.yaxis.set_visible(True if len(results) > 1 else False)
#     ax.set_xlim(0, np.sum(data, axis=1).max())
#     for i, (colname, color) in enumerate(zip(category_names, category_colors)):
#         widths = data[:, i]
#         starts = data_cum[:, i] - widths
#         rects = ax.barh(labels, widths, left=starts, label=colname, color=color)
#         text_color = "white" if color[0] * color[1] * color[2] < 0.5 else "darkgrey"
#         ax.bar_label(rects, label_type="center", color=text_color)
#     ax.legend(ncol=len(category_names), bbox_to_anchor=(0.5, 1.1), loc="upper center", fontsize="x-small")
#     return fig, ax


# def media_bar() -> None:
# 	"""
# 	create bar chart from sum row in stats_df
# 	"""
# 	bar_plotter({"a":db.stats_df.iloc[-1].iloc[list(db.plot1_dict.keys())]}, list(db.plot1_dict.values()))
# 	plt.savefig("data/output/images/page1/media_bar.png", transparent=True)
# 	plt.close()
# 	return


# def plot_barh(df: pd.DataFrame, title: str, x_label: str, y_label: str, color: str) -> None:
# 	df.plot.barh(x=x_label, y=y_label, color=color, figsize=(10,5), legend=False, title=title)
# 	plt.savefig(f"data/output/images/senderpages/barh_{df.name}.png", transparent=True)
# 	plt.close()
# 	return


# --------------------------------------------
#		Functions used to create pdf ouptut
# --------------------------------------------


pdf = FPDF()

xys: list[tuple[int, int]] = list() # last x, y coordinates
sizes: list[int] = list() # last text sizes


def get_coord(x_offset: int=0, y_offset: int=0) -> tuple[int, int]:
	"""
	Returns the x, y cordinates on the current page
	"""
	return (pdf.get_x() + x_offset), (pdf.get_y() + y_offset)


def new_section(size: int=0, style: str="", space: int=0, np: int=0) -> None:
	"""
	Creates a new section in the pdf file and sets the font size and style.
	np: 0 = no new page (default), 1 = new page, 2 = new page and new section
	"""
	pdf.add_page() if np in (1, 2) else None # create new page
	if np in (0, 2): # create new section	on current or new page
		pdf.ln(space)
		xys.append({0: pdf.get_x(), 1: pdf.get_y()})
		sizes.append(size) if size != 0 else None
		pdf.set_font("Arial", style, size if size != 0 else sizes[-1])
	return None


def print_commons(df: pd.DataFrame, cell_width: int = 25, cell_height: int = 6) -> None:
	"""
	Prints a DataFrame to a table in a pdf file
	"""
	margin, _ = get_coord()
	pdf.set_font("Arial", "B", 8)
	pdf.cell(cell_width, cell_height, df.columns[0], align="C", border=1)
	pdf.cell(17, cell_height, df.columns[1], align="C", border=1)
	pdf.set_xy(margin, pdf.get_y() + cell_height)

	pdf.set_font("Arial", "", 8)
	for i in range(len(df)):
		pdf.cell(cell_width, cell_height, df.iat[i,0].strip(":").replace("_", " ")[:20], align="C", border=1)
		pdf.cell(17, cell_height, str(df.iat[i,1]), align="C", border=1)
		pdf.set_xy(margin, pdf.get_y() + cell_height)




def add_title_footer(n: int=-1) -> None:
	"""
	Prints the title of the page
	"""
	pdf.set_margins(15, 20, 15) if pdf.page_no() == 0 else None
	pdf.add_page()

	# Create title of current page
	new_section(18, "B")
	pdf.cell(0, 10, "WhatsApp Chat Statistics", align="C")
	new_section(12, space=5)
	pdf.cell(0, 12, "for "+ str(ss() if n == -1 else db.senders[n]), align="C")

	# Create footer of current page
	pdf.set_xy(0, 270)
	new_section(10, "I")
	pdf.cell(0, 5, f"Page {pdf.page_no()}", align="C")
	pdf.set_xy(*xys[-2].values())
	return


def print_stats(s_no: int=-1, w: int=24, h: int=6) -> None:
	"""
	Prints the statistics of a sender to the pdf file
	"""
	for i, x in enumerate([11, 12, 7, 13, 8, 14, 10, 17, 9]):
		if i == 0:
			pdf.set_font("Arial", "", 12)
			pdf.cell(w*4, h+2, "Media types and amount sent", 0, 1, "C")
			pdf.set_font("Arial", "", 11)
		value = str(db.stats_df.iat[db.sc if s_no == -1 else s_no, x])
		item = list(db.stats_dict.values())[x] + "s" if value != 1 else ""
		pdf.cell(w, h, item.capitalize(), 1, 0, "C")
		pdf.cell(w, h, value, 1, 0, "C")
		if i % 2 != 0:
			pdf.ln(h)
	return None


def make_pdf_report() -> None:
	"""
	Creates a pdf file with a summary of the chat and the statistics
	"""
	add_title_footer()
	path = "data/output/images/page1/"
	
	new_section(11, space=20)
	pdf.cell(90, 0, "This conversation contains")
	new_section(14, "B", space=3)
	pdf.multi_cell(110, 5, db.reports[db.sc][0])

	new_section(11, space=4)
	pdf.multi_cell(100, 4, db.reports[db.sc][1])

	new_section(space=4)

	pdf.image(path+"msg_pie.png", x=114.5, y=35, w=84.5)
	pdf.image(path+"media_bars.png", x=0, y=120, w=210)
	pdf.image(path+"ts.png", x=0, y=180, w=210)


	for i, s in enumerate(db.senders):
		add_title_footer(i)
		path = "data/output/images/senderpages/s" + str(i)

		new_section(11, space=20)
		pdf.cell(90, 0, f"Messages from {s} contain")
		new_section(14, "B", space=3)
		pdf.multi_cell(110, 5, db.reports[i][0])

		new_section(space=4)
		print_stats(i)

		new_section(11, space=10)
		pdf.multi_cell(110, 4, db.reports[i][1])

		
		# add_title_footer(i)
		pdf.image(path+"_wc.png", x=113, y=33, w=88)
		pdf.image(path+"_ts.png", x=0, y=125, w=210)
		pdf.image(path+"_heatmap.png", x=0, y=180, w=210)

		add_title_footer(i)

		pdf.set_xy(20, 40)

		print_commons(db.common_words[i].head(10), cell_width=25, cell_height=5)

		pdf.set_xy(70, 40)

		print_commons(db.common_emojis[i].head(10), cell_width=25, cell_height=5)


	pdf.output("data/output/pdfs/WA-Report.pdf", "F",)
	return time("finishing final PDF Report")
