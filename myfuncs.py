from timeit import default_timer as timer

from unidecode import unidecode # for timing
ts = [timer()]

import database as db  # for access to local database
from outputstyle import * # for pretty printing
import numpy as np, pandas as pd # to create dataframes
import re # for regex 
import emojis # to find emoji in messages
from wordcloud import WordCloud # to create wordclouds
from matplotlib import pyplot as plt, dates as mdates, cm # to plot figures
from textblob_de import TextBlobDE as TextBlob # for sentiment analysis

from fpdf import FPDF # to create pdfs


# Unused imports
import matplotlib
# import os
# from plotly import express as px 
# from germansentiment import SentimentModel
# model = SentimentModel()

def time(task: str="untitled") -> None:
	"""
	Adds a new entry to the time dataframe.
	"""
	ts.append(timer())
	if task == "end":
		export(datab=True)
		db.tt = pd.concat([db.tt, pd.DataFrame([["- -", "- -"], 
		["# main.py #", ts[-1] - ts[0]], ["without imports", ts[-1] - ts[1]]])])
		print(f"\nmain.py took {BOLD(ts[-1] - ts[0])} sec. to complete "
				+ f"(without the imports {BOLD(ts[-1] - ts[1])} sec.)\n\n")
		db.tt.to_csv("data/testing/time.csv", mode="a", header=False)
		return exit()
	db.tt.loc[len(db.tt)] = [task, ts[-1] - ts[-2]]
	print(f"{BLUE(task)} took {BOLD(round(ts[-1] - ts[-2], 6))} sec.")


db.tt = pd.DataFrame(columns=[0, 1])
time("importing neccessary modules")

def off(*args, file_end: bool=False) -> None:
	"""
	Prints error message and safely exits the program.
	"""
	return exit(BOLD(RED("⛔️ Error: ")) + " ".join(args) + " ⛔️" 
					if len(args) > 0 else "") if not file_end else time("end")


def export(loc: str=None, data=None, name: str=None, datab: bool=False) -> None:
	"""
	Exports dataframes and text to the data/testing/exports folder. 
	"""
	if not datab:
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


def fileformat(path_to_file: str) -> str:
	"""
	Checks if the fileformat is correct and returns correct path.
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


def new_msg(input: str) -> bool:
	"""
	Returns true if the input is the beginning of a new message (date in front).
	"""
	# return True if re.match("^.? ?\[([\d./]*), ([\d:]*)\] .*", input) else False
	return re.match("^.? ?\[([\d./]*), ([\d:]*)\] .*", input)


def convert_ln(input: str) -> list[str]:
	"""
	Converts a WA chat history line into a list with these entries:
	date, datetime, sender, message, polarity, emojis_unique, emoji_count, url_count.
	"""
	# match pattern and devide into groups: 1:date, 2:datetime, 3:sender, 4:message
	x = re.search("^.? ?\[([\d./]*), ([\d:]*)\] ([\w ]*): (\u200E?.*)$", input)
	result = [x.group(1), " ".join([x.group(1), x.group(2)])]  # add date, datetime
	result.append(x.group(3).title())  # capitalize first letters of sender
	message = re.sub("https?://\S+", "xURLx", x.group(4))  # replace URLs
	result.append(message)  # add message
	if len(message) > 2 and message.upper().isupper():
		result.append(TextBlob(message.replace("xURLx", "")).sentiment.polarity)  # add polarity
	else:
		result.append(pd.NA)
	return result


def convert_to_list(path_to_file: str) -> list[list[str]]:
	"""
	Converts a .txt-file of messages into a list of lists: Each list element 
	contains these elements: [date, datetime, sender, message, polarity, emojis, 
	emoji_count, url_count].
	"""
	chat, last_msg = list(), str()
	try:  # try to open the file
		with open(path_to_file, "r", encoding="utf-8") as file:
			for line in file:  # read line by line
				if new_msg(line):  # the line is the beginning of a new message
					# add previous message to list if buffer is not empty
					chat.append(convert_ln(last_msg)) if last_msg != "" else None
					last_msg = line.strip().strip("\n").strip()  # add new message to buffer
				else:  # the line is a continuation of the previous message
					# add line to previous message
					last_msg += " " + line.strip().strip("\n").strip()
			# add last message to list if it is not added yet
			chat.append(convert_ln(last_msg)) if chat[-1] != convert_ln(last_msg) else None
	except FileNotFoundError:  # the file does not exist
		return off("File not found\nCheck the path to the file")
	except (UnicodeDecodeError, UnicodeError):  # the file is not in UTF-8
		return off("File not in UTF-8 format\nTry uploading the original file")
	
	time("converting the .zip/.txt file to a python list")
	return chat


def convert_to_df(path: str) -> pd.DataFrame:
	"""
	Converts a list of lists into a dataframe with the following columns:
	[date, time, sender, message, polarity, emojis, emoji_count, url_count] and returns it.
	"""
	# chat_listed = convert_to_list(path)
	df = pd.DataFrame(convert_to_list(path), columns=db.df_cols)
	df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True, format="%d.%m.%Y")
	df["datetime"] = pd.to_datetime(df["datetime"], infer_datetime_format=True)
	db.chat = df

	# export("myfuncs/convert_to_df", df, "df_converted.csv") #TODO remove line
	time("converting the python list to a pandas dataframe")
	return


def prepare_db() -> None:
	"""
	Prepares the database by filling data in #tobefilled placeholders.
	"""
	db.chat["weekday"] = db.chat["date"].apply(lambda x: x.weekday())
	db.chat["hour"] = db.chat["datetime"].apply(lambda x: x.hour)
	db.chat_og = db.chat.copy() # Creates copy for later using

	db.senders = list(db.chat["sender"].unique()) # Creates list of senders
	db.sc = len(db.senders) # Number of senders
	
	db.stats_df = pd.DataFrame(index=db.senders, columns=db.stats_dict.keys())
	db.time_stats_df = pd.DataFrame(index=db.senders, columns=db.time_stats_cols)
	
	time("preparing the database")
	return


def seperate_data() -> None:
	# data seperation, cleansing and data analysis per sender
	for i, s in enumerate(db.senders):
		# bar.text = f"Cleaning and analyzing messages from {s}" #TODO bar
		df = db.chat.loc[db.chat["sender"] == s]  # dataframe with messages from sender
		db.chat_per_s.append(df)
		clean_df = cleanse_df(df["message"], s)  # get the stats for each sender
		count_occurances(clean_df, i)
		calc_stats(clean_df) # calculate the stats for each sender
		# globals()[f"s{i}_df_clean"] = clean_df #TODO remove line
		# globals()[f"s{i}_word_freq"] = word_freq #TODO remove line

	db.chat_per_s.append(db.chat_og)
	return


def cleanse_df(dataframe: pd.DataFrame, sender: str) -> pd.DataFrame:
	"""
	Cleans the dataframe of non-message enties and replaces URLs and enters 
	collected data into the stats dataframe.
	"""
	count = 0  # counter for media messages cleaned
	df = dataframe.copy().rename(sender)
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
	
	# export("myfuncs/cleanse_df", df, f"df_clean_{sender}.csv") #TODO remove line
	db.chat_per_s_clean.append(df)
	time(f"cleaning df for sender{db.senders.index(sender)+1}")

	# db.stats_df.at[sender, "polarity_avg"] = calc_polarity(df, db.senders.index(sender)+1) #TODO remove line
	return df  # return the cleaned dataframe


def calc_stats(sender_df: pd.DataFrame) -> None:
	"""
	Calculates different statistics about the chat and enters collected data 
	into the stats dataframe.
	"""
	s = sender_df.name # get column name (sender)
	db.stats_df.at[s,"msg_count"] = sender_df.shape[0]
	db.stats_df.at[s,"chars_avg"] = round(sender_df.str.replace(" ", "").str.len().mean(), 2)
	db.stats_df.at[s,"words_avg"] = round(sender_df.str.split().str.len().mean(), 2)
	db.stats_df.at[s,"chars_max"] = sender_df.str.replace(" ", "").str.len().max()
	db.stats_df.at[s,"words_max"] = len(sender_df[sender_df.str.len().idxmax()].split())
	db.stats_df.at[s,"polarity_avg"] = round(db.chat.loc[db.chat["sender"] == s, "polarity"].mean(skipna=True), 2)
	db.stats_df.at[s,"polarity_pos"] = db.chat.loc[db.chat["sender"] == s, "polarity"].gt(0).sum()
	db.stats_df.at[s,"polarity_neg"] = db.chat.loc[db.chat["sender"] == s, "polarity"].lt(0).sum()
	db.stats_df.at[s,"polarity_neu"] = db.chat.loc[db.chat["sender"] == s, "polarity"].eq(0).sum() #TODO remove if not needed
	db.stats_df.at[s,"polarity_nan"] = db.chat.loc[db.chat["sender"] == s, "polarity"].isna().sum() #TODO remove if not needed
	
	time(f"calculating statistics for sender{db.senders.index(s)+1}")
	return


def calc_sum_stats() -> None:
	"""
	Calculates summary statistics about the chat and enters collected data
	into the stats dataframe.
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
	
	# export("myfuncs/get_sum_stats", db.stats_df, "stats_df.csv") #TODO remove line
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


def count_occurances(df: pd.DataFrame, i: int) -> pd.DataFrame:
	"""
	Calculates different statistics about the chat and enters collected data.
	"""
	messages = " ".join(df).lower()

	# count emojis
	emojis_listed = emojis.get(messages)
	emoji_dict = dict()
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
	s = (str(n) if n > 1 else ("one" if n == 1 else "no")) + " " + term
	return s + ("s" if n != 1 and term not in ("media", "polarity") else "")


def get_stat_pair(stat: int, sender: int) -> tuple[int, str]:
	"""
	Returns the value and term of a specific statistic.
	"""
	return db.stats_df.iat[sender, stat], list(db.stats_dict.values())[stat]


def create_txt_reports() -> list[str]:
	"""
	Creates a report about the sender at the given index which includes the 
	statistics about their messages or a summary report and returns it.
	"""
	i = int()

	def y(*idxs): return pprint(*[calc_num(*get_stat_pair(x, i)) for x in idxs])
	def x(*idxs): return pprint(*[db.time_stats_df[i,z] for z in idxs])

	for i, s in enumerate(db.senders): # for each sender create a sender report
		db.reports.append([y(0,6,18),
			f"An average message from {s} is {y(2)} ({y(1)}) long. "
			+ f"Their longest message contained {y(4)} and {y(3)}.",
			f"{s} deleted {y(15)}.",
			])
		if db.stats_df.iat[i, 16] != 0:
			db.reports[-1].append(f"You missed {y(16)} by {s}.")
	
	# General report about all chat messages
	i = db.sc
	db.reports.append([y(0,6,18),
	f"An average message between {ss()} is {y(2)} ({y(1)}) long. "
	+ f"The longest message contained {y(4)} and {y(3)}.",
	f"{ss()} deleted {y(15)}.",
	]) # add report to the list
	
	return time("txt report creation")


# ----------------------------------------------------------------
# 				Functions to create images for the report
# ----------------------------------------------------------------


def plot_data() -> None:
	msg_pie()
	grouped_madia_bars()
	message_time_series()
	return time("make plots")


def cmap(countable=db.senders, cm_name: str="Greens_r"):
	if type(countable) != int:
		countable = len(countable)
	return cm.get_cmap(cm_name)(np.linspace(.2, .8, countable+1))


def msg_pie() -> None:
	"""
	create pie chart from msg_count in stats_df
	"""
	fig, ax = plt.subplots(figsize=(3.14, 3.14))
	ax.pie(db.stats_df.iloc[0:-1, 0], startangle=90, colors=cmap(db.senders), counterclock=False, autopct="%1.2f%%", wedgeprops={"ec":"w"}, textprops={"c":"w"})
	ax.legend(labels=db.senders, title="sender", shadow=True, loc="upper right", fontsize="small")
	fig.tight_layout()
	plt.savefig("data/output/images/page1/msg_pie.png", transparent=True)
	plt.close()
	return


def grouped_madia_bars() -> None:
	"""
	Plots the stcked bar chRT bout data and senders
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

	ax.set_title("Media types by sender", loc="left"); ax.set_ylabel("amount")
	ax.set_xticks(x); ax.set_yticks(np.arange(0, max_val, 50), minor=True)
	ax.set_ylim([0, max_val+30]); ax.grid(True, "both", "y", lw=.8)
	ax.set_xticklabels(labels)

	if db.sc < 7:
		ax.legend(bbox_to_anchor=(1,1.15), fontsize="small", ncol=db.sc)
	else:
		ax.legend(bbox_to_anchor=(1,1.3), fontsize="small", ncol=round(db.sc/2))

	# fig.tight_layout()
	
	plt.savefig("data/output/images/page1/media_bars.png", transparent=True)
	plt.close()


def message_time_series() -> None:
	"""
	Creates a time series plot of the messages sent per day.
	"""
	for i, range in enumerate(db.msg_ranges):
		fig, ax = plt.subplots(figsize=(8.27,2))

		ax.plot(range.index, range.values, color="green")
		# Major ticks every half year, minor ticks every month
		ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 5, 9), bymonthday=15))
		ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=15))
		ax.grid(True, "both", "y")
		ax.set_ylabel("amount")
		ax.set_title("Messages per day", loc="left")
		ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

		page = "page1/" if i == db.sc else f"senderpages/s{str(i)}_"
		fig.savefig(f"data/output/images/{page}ts.png", transparent=True)
		plt.close(fig)
	return


def bar_plotter(results, category_names):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = cmap(data.shape[1])
    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(True if len(results) > 1 else False)
    ax.set_xlim(0, np.sum(data, axis=1).max())
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, label=colname, color=color)
        text_color = "white" if color[0] * color[1] * color[2] < 0.5 else "darkgrey"
        ax.bar_label(rects, label_type="center", color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0.5, 1.1), loc="upper center", fontsize="x-small")
    return fig, ax


def media_bar() -> None:
	"""
	create bar chart from sum row in stats_df
	"""
	bar_plotter({"a":db.stats_df.iloc[-1].iloc[list(db.plot1_dict.keys())]}, list(db.plot1_dict.values()))
	plt.savefig("data/output/images/page1/media_bar.png", transparent=True)
	plt.close()
	return


def plot_barh(df: pd.DataFrame, title: str, x_label: str, y_label: str, color: str) -> None:
	df.plot.barh(x=x_label, y=y_label, color=color, figsize=(10,5), legend=False, title=title)
	plt.savefig(f"data/output/images/senderpages/barh_{df.name}.png", transparent=True)
	plt.close()
	return


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


# def print_df_to_pdf(df: pd.DataFrame, cell_width: int = 25, cell_height: int = 6) -> None:
# 	"""
# 	Prints a dataframe to a table in a pdf file
# 	"""
# 	pdf.set_font("Arial", "B", 10)
# 	for col in df.columns:	# Loop over to print column names
# 		pdf.cell(cell_width, cell_height, col, align="C", border=1)
# 	pdf.ln(cell_height) # next row of table

# 	pdf.set_font("Arial", "", 8)
# 	for row in df.itertuples():	# Loop over to print each data in the table
# 		for col in df.columns:
# 			value = str(getattr(row, col))
# 			pdf.cell(cell_width, cell_height, value, align="C", border=1)
# 		pdf.ln(cell_height) # next row of table


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

	new_section(space=4)
	print_stats()

	new_section(11, space=14)
	pdf.multi_cell(110, 4, db.reports[db.sc][1])

	pdf.image(path+"msg_pie.png", x=109, y=29, w=96)
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

		new_section(11, space=14)
		pdf.multi_cell(110, 4, db.reports[i][1])

		
		# add_title_footer(i)
		pdf.image(path+"_wc.png", x=113, y=33, w=88)
		pdf.image(path+"_ts.png", x=0, y=120, w=210)



	pdf.output("data/output/pdfs/WA-Report.pdf", "F")
	return time("PDF creation")
