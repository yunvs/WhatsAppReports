from myfuncs import *
# from dataclasses import replace
# from unidecode import unidecode

# import emojificate


# import requests
# import re
# emoji_data = requests.get('https://unicode.org/emoji/charts/full-emoji-list.html').text
# def emoji_to_png(emoji, version=0):
#     html_search_string = r"<img alt='{}' class='imga' src='data:image/png;base64,([^']+)'>" #'
#     matchlist = re.findall(html_search_string.format(emoji), emoji_data)
#     return matchlist[version]



# from turtle import color
# from timeit import default_timer as timer
# from ast import Str
# from hashlib import new
# from pickletools import int4
# from matplotlib import cm
# import database as db«
# import numpy as np

# # ----------------------------------------------------------------
path = "data/testing/exports/database"
db.senders = list(pd.read_csv(f"{path}/senders_df.csv", index_col=0)["0"])
db.sc = len(db.senders)
db.stats_df = pd.read_csv(f"{path}/stats_df.csv", index_col=0)
# chat_og = pd.read_csv(f"{path}/chat_og_df.csv", index_col=0)
# db.chat = pd.read_csv(f"{path}/chat_df.csv", index_col=0)
# msg = stats_df.iloc[0:-1, 0]
# chat_psc = pd.read_csv(f"{path}/chat_per_s_clean_df_demo.csv", index_col=0)
# time("import data from main")
for i in range(db.sc):
	db.common_words.append(pd.read_csv(f"{path}/common_words_s{i}.csv", index_col=0))
	db.common_emojis.append(pd.read_csv(f"{path}/common_emojis_s{i}.csv", index_col=0))
# # ----------------------------------------------------------------



pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

path = "data/output/images/page1/"

pdf.image(path+"msg_pie.png", x=114.5, y=35, w=84.5)
pdf.image(path+"media_bars.png", x=0, y=120, w=210)
pdf.image(path+"ts.png", x=0, y=180, w=210)

pdf.add_page()

path = "data/output/images/senderpages/s1"

pdf.image(path+"_wc.png", x=113, y=33, w=88)
pdf.image(path+"_ts.png", x=0, y=125, w=210)
pdf.image(path+"_heatmap.png", x=0, y=180, w=210)

pdf.output("data/testing/testing.pdf", "F")

# def print_commons(df: pd.DataFrame, cell_height: int = 6) -> None:
# 	"""
# 	Prints a DataFrame to a table in a pdf file
# 	"""
# 	# get the longest string in each column
# 	max_len = df.T.reset_index().T.reset_index(drop=True).astype(str).applymap(len).max().multiply(2)

# 	pdf.set_font("Arial", "B", 8)
# 	for i, col in enumerate(df.columns):	# Loop over to print column names
# 		pdf.cell(max_len.iloc[i], cell_height, col, align="C", border=1)
# 	pdf.ln(cell_height) # next row of table

# 	pdf.set_font("Arial", "", 8)
# 	for row in df.itertuples():	# Loop over to print each data in the table
# 		pdf.cell(max_len.iloc[i], cell_height, str(df.iloc[row, 0]) , align="C", border=1)
# 		pdf.cell(15, cell_height, str(df.iloc[row, 1]) , align="C", border=1)
# 		pdf.ln(cell_height) # next row of table


# # def print_emojis_to_pdf(df: pd.DataFrame, cell_width: int = 25, cell_height: int = 6) -> None:
# # 	"""
# # 	Prints a DataFrame to a table in a pdf file
# # 	"""
# # 	pdf.set_font("Arial", "B", 8)
# # 	for col in df.columns:	# Loop over to print column names
# # 		pdf.cell(cell_width, cell_height, col, align="C", border=1)
# # 	pdf.ln(cell_height) # next row of table

# # 	pdf.set_font("Arial", "", 8)
# # 	for row in df.itertuples():	# Loop over to print each data in the table
# # 		xpos, ypos = float(pdf.get_x()) + cell_width/2, float(pdf.get_y()) + cell_height/2
# # 		emoji_to_png(getattr(row, 0))
# # 		pdf.image(, xpos, ypos, 5, 5, "PNG")
# # 		pdf.cell(cell_width, cell_height, str(getattr(row, 1)), align="C", border=1)
# # 		pdf.ln(cell_height) # next row of table


# def count_occurances(messages) -> None:
# 	"""
# 	Counts the emojis in the chat
# 	"""
# 	emojis_listed = emojis.get(messages)
# 	emoji_freq = dict()
# 	for item in emojis_listed:
# 		emoji_freq[item] = messages.count(item) # count the emojis
# 	db.common_emojis.append(pd.Series(emoji_freq).sort_values(ascending=False))
# 	return

# x = """Hshdbcu djchsdbu d d vd d d ndsa 😍 dfdf 😍😍 fja fjv au🤪 😣 😶‍🌫️ 🥳 🥳 😤 😤 🙂 df fvjadf uj😭v av ja vja va🤪 😣 😶‍🌫️ 🥳 🥳 😤 😤 🙂jvbjasbv 😭 😍 😍 😍  ajdn vm🤪 😣 😶‍🌫️ 🥳 🥳 😤 😤 🙂dvncjv djjdn """
# # print(count_occurances(x))



	


# for i in range(db.sc+1):
# 	sentiment_pies(i)


# s = ":Hello_Hello:"

# #remove the tailing colons and replace underscores with spaces
# s = s.replace(":", "").replace("_", " ")



# # pdf = FPDF()
# # # pdf.add_font("ACE", "", "data/ACE.ttc", uni=True) # Error:  TrueType Fonts Collections not supported
# # for i in range(db.sc):
# # 	pdf.add_page()
# # 	pdf.set_font("Arial", "", 10)
# # 	pdf.cell(200, 10, f"Emoji stats for {db.senders[i]}", align="C")
# # 	pdf.ln(10)
# # 	print_emojis_to_pdf(db.common_emojis[i].head(10))



# # pdf.output("data/testing/testing.pdf", "F")




# # def get_msg_bundles() -> None:
# # 	db.msg_bundles = list() #TODO remove 
# # 	chat_psc = db.chat_per_s_clean
# # 	for i in range(chat_psc.shape[0]):
# # 		sender_list = list()
# # 		last = str()
# # 		for j in  range(chat_psc.shape[1]):
# # 			if not pd.isnull(chat_psc.iloc[i, j]):
# # 				last += str(chat_psc.iloc[i, j]).replace("xURL", "")
# # 				if j == chat_psc.shape[1] - 1 or pd.isna(chat_psc.iloc[i, j+1]):
# # 					sender_list.append(last)
# # 					last = str()
# # 				else:
# # 					last += " "
# # 		db.msg_bundles.append(sender_list)
# # 	return


# # def calc_polarity1(ls: list) -> float:
# # 	pol = 0
# # 	ls = [s for s in ls if s != "" or " "]

# # 	for i in range(len(ls)):
# # 		prediction = model.predict_sentiment([ls[i]])
# # 		pol += 1 if prediction == ["positive"] else -1 if prediction == ["negative"] else 0
# # 		# print(BLUE(f"{i}/{len(ls)}: '{ls[i][:30]}' = {prediction[0]}"))
# # 		# print(BOLD(f" -> {pol/(i+1)}"))
# # 	return pol / len(ls)


# # def calc_polarity2(ls: list) -> float: # funtktioniert nicht :/
# # 	pol = 0
# # 	# sentence_sentiment = model.predict_sentiment(ls)

# # 	ls = [s for s in ls if s != "" or " "]

# # 	predics = model.predict_sentiment(ls)
# # 	pol = sum([1 if p == "positive" else -1 if p == "negative" else 0 for p in predics])
	
# # 	return pol / len(ls)


# # def calc_polarity3(ls: list) -> float:
# # 	ls = [s for s in ls if s != "" or " "]
# # 	preds = list()

# # 	for i in range(len(ls)):
# # 		preds.append(model.predict_sentiment([ls[i]]))

# # 	pol = sum([1 if p == ["positive"] else -1 if p == ["negative"] else 0 for p in preds])
	
# # 	return pol / len(ls)



# # def calc_polarity4(ls: list) -> float:
# # 	blob = TextBlob(" ".join(ls))
# # 	pol = 0
# # 	for sentence in blob.sentences:
# # 		pol += sentence.sentiment.polarity
# # 	return pol / len(ls)


# # def calc_polarity5(ls: list) -> float:
# # 	blob = TextBlob(" ".join(ls))
# # 	return blob.sentiment.polarity






# # def test_blob0(ls: list) -> float:
# # 	# time("start blob0")
# # 	pol = 0
# # 	# for i, sentence in enumerate(ls):
# # 	for sentence in ls:
# # 		blob = TextBlob(sentence)
# # 		# print(": ".join([sentence[:100], str(blob.sentiment.polarity)]))
# # 		pol += blob.sentiment.polarity
# # 	# time(f"Finishing blob0, pol: {pol}/{len(ls)} = {pol/len(ls)}")
# # 	return pol/len(ls)


# # def test_blob1(ls: list) -> float:
# # 	# time("start blob1")
# # 	blob = TextBlob(" ".join(ls))
# # 	# time(f"Finishing blob1, pol: {blob.sentiment.polarity*len(ls)}/{len(ls)} = {blob.sentiment.polarity}")
# # 	return blob.sentiment.polarity



# # time("startttt")
# # for x in ["chat_per_s_clean_df_demo", "chat_per_s_clean_df", ""]:
# # 	data = [[], []]
# # 	if x != "":
# # 		db.chat_per_s_clean = pd.read_csv(f"{path}{x}.csv", index_col=0) #TODO: remove
# # 		get_msg_bundles()
# # 		data = db.msg_bundles
# # 	else:
# # 		for i, s in enumerate(list(db.chat["sender"].unique())): #TODO: remove
# # 			data[i] = list(db.chat.loc[db.chat["sender"] == s]["message"])

# # 	pols = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
# # 	# time("extracting mesages bundles")

# # 	for i in range(len(data)):
# # 		print("\n")
# # 		pols[0].append(test_blob0(data[i]))
# # 		pols[1].append(test_blob1(data[i]))

# # 	print()
# # 	for n, pol in enumerate(pols):
# # 		print(f"pol{n} : {pol}") if pol != [] else None




# # # lengths = list()
# # # for i in range(len(db.msg_bundles)):
# # # 	lengths.append(len(db.msg_bundles[i]))
# # # print(lengths)







# # """
# # for x in ["chat_per_s_clean_df_demo", "chat_per_s_clean_df"]:
# # 	chat_psc = pd.read_csv(f"data/testing/exports/database/{x}.csv", index_col=0)
# # 	time("import data from main")

# # 	get_msg_bundles()
# # 	time("GET TEXT BUBBLES")
# # 	print("\n")

# # 	pols = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
# # 	for i in range(len(db.msg_bundles)):
# # 		pols[0].append(calc_polarity1(db.msg_bundles[i]))
# # 		time(f"sentiment pol1 sender{i} = {pols[0][i]}")
# # 		# pols[1].append(calc_polarity2(db.msg_bundles[i]))
# # 		# time(f"sentiment pol2 sender{i} = {pols[1][i]}")
# # 		pols[2].append(calc_polarity3(db.msg_bundles[i]))
# # 		time(f"sentiment pol3 sender{i} = {pols[2][i]}")
# # 		pols[3].append(calc_polarity4(db.msg_bundles[i]))
# # 		time(f"sentiment pol4 sender{i} = {pols[3][i]}")
# # 		pols[4].append(calc_polarity5(db.msg_bundles[i]))
# # 		time(f"sentiment pol5 sender{i} = {pols[4][i]}")
# # 		print("")


# # 	for n, pol in enumerate(pols):
# # 			print(f"pol{n} : {pol}") if pol != [] else None
	
# # 	print("\n\n")
	
# # 	"""








# # # def heatmap(data, row_labels, col_labels, ax=None,
# # # 			cbar_kw={}, cbarlabel="", **kwargs):

# # # 	if not ax:
# # # 		ax = plt.gca()

# # # 	# Plot the heatmap
# # # 	im = ax.imshow(data, **kwargs)

# # # 	# Create colorbar
# # # 	cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
# # # 	cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

# # # 	# Show all ticks and label them with the respective list entries.
# # # 	ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
# # # 	ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

# # # 	# Let the horizontal axes labeling appear on top.
# # # 	ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

# # # 	# Turn spines off and create white grid.
# # # 	ax.spines[:].set_visible(False)

# # # 	ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
# # # 	ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
# # # 	ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
# # # 	ax.tick_params(which="minor", bottom=False, left=False)

# # # 	return im, cbar


# # # def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
# # # 					 textcolors=("black", "white"),
# # # 					 threshold=None, **textkw):

# # # 	if not isinstance(data, (list, np.ndarray)):
# # # 		data = im.get_array()

# # # 	# Normalize the threshold to the images color range.
# # # 	if threshold is not None:
# # # 		threshold = im.norm(threshold)
# # # 	else:
# # # 		threshold = im.norm(data.max())/2.

# # # 	# Set default alignment to center, but allow it to be
# # # 	# overwritten by textkw.
# # # 	kw = dict(horizontalalignment="center",
# # # 			  verticalalignment="center")
# # # 	kw.update(textkw)

# # # 	# # Get the formatter in case a string is supplied
# # # 	if isinstance(valfmt, str):
# # # 		valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

# # # 	# Loop over the data and create a `Text` for each "pixel".
# # # 	# Change the text's color depending on the data.
# # # 	texts = []
# # # 	for i in range(data.shape[0]):
# # # 		for j in range(data.shape[1]):
# # # 			kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
# # # 			text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
# # # 			texts.append(text)
# # # 	return texts


# # # def msg_pie() -> None:
# # # 	"""
# # # 	create pie chart from msg_count in stats_df
# # # 	"""
# # # 	fig, ax = plt.subplots(figsize=(3.14, 3.14))
# # # 	ax.pie(stats_df.iloc[0:-1, 0], startangle=90, colors=cmap(senders), counterclock=False, autopct="%1.2f%%", wedgeprops={"ec":"w"}, textprops={"c":"w"})
# # # 	ax.legend(labels=senders, title="sender", shadow=True, loc="upper right", fontsize="small")
# # # 	ax.set_title("Messages sent by")
# # # 	fig.tight_layout()
# # # 	plt.savefig("data/testing/exports/testing/msg_pie.png", transparent=True)
# # # 	plt.close()
# # # 	return


# # # def make_pdf_report1() -> None:
# # # 	"""
# # # 	Creates a pdf file with a summary of the chat and the statistics
# # # 	"""
# # # 	# add_title_footer()
# # # 	pdf.add_page()
# # # 	path = "data/output/images/page1/"
	
# # # 	# new_section(11, space=20)
# # # 	# pdf.cell(90, 1, "This conversation contains")
# # # 	# new_section(14, "B", space=3)
# # # 	# pdf.multi_cell(110, 5, db.reports[db.sc][0])

# # # 	# new_section(space=4)
# # # 	# print_stats()

# # # 	# new_section(11, space=14)
# # # 	# pdf.multi_cell(110, 4, db.reports[db.sc][1])

# # # 	pdf.image(path+"msg_pie.png", x=109, y=29, w=96)
# # # 	pdf.image(path+"media_bars.png", x=0, y=120, w=210)
# # # 	pdf.image(path+"ts.png", x=0, y=160, w=210)


# # # 	for i, s in enumerate(senders):
# # # 		pdf.add_page()
# # # 		path = "data/output/images/senderpages/s" + str(i)

# # # 		# new_section(11, space=20)
# # # 		# pdf.cell(90, 1, f"{s} messages contain")
# # # 		# new_section(14, "B", space=3)
# # # 		# pdf.multi_cell(110, 5, db.reports[i][0])

# # # 		# new_section(space=4)
# # # 		# print_stats(i)

# # # 		# new_section(11, space=14)
# # # 		# pdf.multi_cell(110, 4, db.reports[i][1])

		
# # # 		pdf.image(path+"_wc.png", x=113, y=33, w=88)
# # # 		pdf.image(path+"_ts.png", x=0, y=120, w=210)


# # # 		# add_title_footer(i)

# # # 	pdf.output("data/testing/testing.pdf", "F")




# # # def stacked_bars_media() -> None:
# # # 	"""
# # # 	Plots the stcked bar chRT bout data and senders
# # # 	"""
# # # 	# data
# # # 	nums = [11, 7, 8, 10, 9, 12, 13, 14, 17]
# # # 	labels = [list(db.stats_dict.values())[x] for x in nums]
# # # 	width = 1
# # # 	fig, ax = plt.subplots()
# # # 	for i, s in enumerate(senders):
# # # 		# plotting
# # # 		if i == 0:
# # # 			rect = ax.bar(labels, stats_df.iloc[i, nums], width, label=s)
# # # 		else:
# # # 			rect = ax.bar(labels, stats_df.iloc[i, nums], width, bottom=stats_df.iloc[i-1, nums], label=s)
# # # 		ax.bar_label(rect, label_type="center", padding=4)
# # # 	ax.set_xticks(labels);ax.set_xticklabels(labels, rotation=35)
# # # 	ax.set_ylabel("Amount")
# # # 	ax.set_title("Media by types and sender")
# # # 	ax.legend()
# # # 	plt.show()

# # # def grouped_bars_media() -> None:
# # # 	"""
# # # 	Plots the stcked bar chRT bout data and senders
# # # 	"""
# # # 	# data
# # # 	nums = [11, 7, 8, 10, 9, 17, 12, 13, 14]
# # # 	labels = [list(db.stats_dict.values())[x].capitalize() for x in nums]
# # # 	w = .9 # the width of the bars
# # # 	x = np.arange(len(labels)) # the label locations
# # # 	# max_val = stats_df.iloc[:, nums].max().max()
# # # 	max_val = stats_df.iloc[0:s_count, nums].max().max()

# # # 	fig, ax = plt.subplots(figsize=(10,3))

# # # 	for i, s in enumerate(senders):
# # # 		# plotting
# # # 		rect = ax.bar((x-w/2) + i*w/s_count, stats_df.iloc[i, nums], w/s_count, label=s, align="edge")
# # # 		ax.bar_label(rect, padding=1) if any([s_count < 4 and max_val < 1000, s_count < 6 and max_val < 100, max_val < 10]) else None

# # # 	# Add some text for labels, title and custom x-axis tick labels, etc.
# # # 	ax.set_ylabel("amount");ax.set_title("Media types by sender", loc="left")
# # # 	ax.set_xticks(x);ax.set_xticklabels(labels)
# # # 	ax.set_yticks(np.arange(0, max_val, 50), minor=True)
# # # 	ax.set_ylim([0, max_val+30]);ax.grid(True, "both", "y", lw=.8, ls="--")
# # # 	if s_count < 7:
# # # 		ax.legend(bbox_to_anchor=(1,1.15), fontsize="small", ncol=s_count)
# # # 	else:
# # # 		ax.legend(bbox_to_anchor=(1,1.3), fontsize="small", ncol=round(s_count/2))

# # # 	fig.tight_layout()

# # # senders = ["Samia", "Besco"]


# # # # stacked_bars_media()
# # # for i in range(2, 8):
# # # 	s_count = len(senders)
# # # 	grouped_bars_media()
# # # 	plt.savefig(f"data/testing/exports/testing/{str(i)}_senders.png", transparent=True)
# # # 	plt.close()
# # # 	senders.append(f"Lopa{i}")
# # # 	time(f"{str(i)} senders")






# # # pdf = FPDF()
# # # pdf.add_page()
# # # pdf.set_font("Arial", size=11)
# # # make_pdf_report1()
# # # time("@make_pdf_report1")






















# # # # sizes: list[int] = list() # last text sizes

# # # # def get_coord(x_offset: int=0, y_offset: int=0) -> tuple[int, int]:
# # # # 	"""
# # # # 	Returns the x, y cordinates on the current page
# # # # 	"""
# # # # 	return (pdf.get_x() + x_offset), (pdf.get_y() + y_offset)

# # # # def new_section(size: int=0, style: str="", space: int=0, np: int=0) -> None:
# # # # 	"""
# # # # 	Creates a new section in the pdf file and sets the font size and style.
# # # # 	np: -1 = only footer, 0 = no new page (default), 1 = new page, 2 = new page and new section
# # # # 	"""
# # # # 	if pdf.page_no() == 0: # create first page
# # # # 		pdf.set_margins(15, 20, 15)
# # # # 		pdf.add_page()
# # # # 	if np in (-1, 1, 2): # create footer for current page
# # # # 		pdf.set_xy(0, 270)
# # # # 		new_section(8, "I")
# # # # 		pdf.cell(0, 5, f"Page {pdf.page_no()}", align="C")
# # # # 	pdf.add_page() if np in (1, 2) else None # create new page
# # # # 	if np in (0, 2): # create new section	on current or new page
# # # # 		pdf.ln(space)
# # # # 		xys.append({"x": pdf.get_x(), "y": pdf.get_y()})
# # # # 		sizes.append(size) if size != 0 else None
# # # # 		pdf.set_font("Arial", style, size if size != 0 else sizes[-1])
# # # # 	return None





# # # # pdf = FPDF()
# # # # pdf.add_page()
# # # # pdf.set_font("Arial", size=11)

# # # # # i = db.sc
# # # # # def y(*idxs): return say(*[calc_numerus(*get_stat_pair(x, i)) for x in idxs])
# # # # """	f"The {db.sc} senders ...", f"... sent {y(11,7,8,10,9)}", 
# # # # 	f"... shared {y(12,13,14,17)}", f"... deleted {y(15)} in this chat"]) """




# # # # new_section(11, "", space=20)
# # # # pdf.multi_cell(90, 4, x)

# # # # new_section(space=20)

# # # # l1 = [	11,	12, 
# # # # 		7, 	13, 
# # # # 		8, 	14, 
# # # # 		10,	17,
# # # # 		9]
# # # # l2 = [stats_df.iat[len(senders), item] for item in l1]
# # # # w, h = 90, 6
# # # # w_item = 21
# # # # w_value = len(str(max(l2)))*5

# # # # for i, x in enumerate(l1):
# # # # 	if i == 0:
# # # # 		pdf.set_font("Arial", "B", 12)
# # # # 		pdf.cell(w, h+2, "Media types and amount sent", 0, 1, "C")
# # # # 		# pdf.cell(w, h, "media", 1, 0, "C")
# # # # 		# pdf.cell(w, h, "count", 1, 0, "C")
# # # # 		# pdf.cell(w, h, "media", 1, 0, "C")
# # # # 		# pdf.cell(w, h, "count", 1, 1, "C")
# # # # 	pdf.set_font("Arial", "", 11)
# # # # 	pdf.cell(w_item, h, list(db.stats_dict.values())[x].capitalize()+"s", 1, 0, "C")
# # # # 	pdf.cell(w_value, h, str(l2[i]), 1, 0, "C")
# # # # 	if i % 2 != 0:
# # # # 		pdf.ln(h)
# # # # 	else:
# # # # 		pdf.set_xy(pdf.get_x() + (w - (w_item + w_value) * 2), pdf.get_y())


# # # # new_section(space=20)
# # # # pdf.multi_cell(90, 4, "Hello this is the end of the report")


# # # # new_section(space=20)


# # # # l1 = [	11,	12, 
# # # # 		7, 	13, 
# # # # 		8, 	14, 
# # # # 		10,	17,
# # # # 		9]
# # # # l2 = [stats_df.iat[len(senders), item] for item in l1]
# # # # w, h = 90, 6
# # # # w_item, w_value = 20, len(str(max(l2)))*5

# # # # for i, x in enumerate(l1):
# # # # 	if i == 0:
# # # # 		pdf.set_font("Arial", "B", 11)
# # # # 		pdf.cell(w, h, "Media types and amount sent", 0, 1, "C")
# # # # 		# pdf.cell(w, h, "media", 1, 0, "C")
# # # # 		# pdf.cell(w, h, "count", 1, 0, "C")
# # # # 		# pdf.cell(w, h, "media", 1, 0, "C")
# # # # 		# pdf.cell(w, h, "count", 1, 1, "C")
# # # # 	pdf.set_font("Arial", "", 11)
# # # # 	pdf.cell(w_item, h, list(db.stats_dict.values())[x], 1, 0, "C")
# # # # 	pdf.cell(w_value, h, str(l2[i]), 1, 0, "C")
# # # # 	if i % 2 != 0:
# # # # 		pdf.ln(h)
# # # # 	else:
# # # # 		pdf.set_xy(pdf.get_x() + (w - (w_item + w_value) * 2), pdf.get_y())




# # # # pdf.output("data/output/pdfs/testing.pdf", "F")




# # # # zz = chat_og["date"].value_counts().sort_index()
# # # # date_range = pd.date_range(start=zz.index[0], end=zz.index[-1])

# # # # msg_date = pd.Series(index=date_range, dtype=int)
# # # # for date in date_range.strftime('%Y-%m-%d'):
# # # # 	msg_date[date] = zz[date] if date in zz.index else 0

# # # # fig, ax = plt.subplots(figsize=(12, 4))

# # # # ax.plot(msg_date.index, msg_date.values, color="green")
# # # # # # Major ticks every half year, minor ticks every month,
# # # # ax.xaxis.set_major_locator(dates.MonthLocator(bymonth=(1, 7)))
# # # # ax.xaxis.set_minor_locator(dates.MonthLocator())
# # # # ax.grid(True)
# # # # ax.set_ylabel('Messages sent')


# # # # ax.xaxis.set_major_formatter(dates.ConciseDateFormatter(ax.xaxis.get_major_locator()))


# # # # # for label in ax.get_xticklabels(which='major'):
# # # # # 	label.set(rotation=30, horizontalalignment='right')

# # # # plt.show()








# # # # # Testing Area:
# # # # data = []
# # # # for i in range(len(senders)):
# # # # 	data.append([stats_df.iloc[i,0], stats_df.iloc[i,6]])
# # # # data = np.array(data)
# # # # print(data)


# # # # # # ----------------------------------------------------------------
# # # # fig, ax = plt.subplots()

# # # # # cmap = plt.colormaps["tab20c"]
# # # # # outer_colors = cmap(np.arange(3)*4)
# # # # # inner_colors = cmap([1  , 2, 5, 6, 9, 10])

# # # # # ax.pie(msg, startangle=90, counterclock=False, autopct="%1.1f%%", wedgeprops={"ec": "w"}, colors=cm_colors("Greens_r", db.senders))

# # # # colors = cmap("Greens_r", db.senders)
# # # # aplha_colors = colors[:, 3] = 0.8

# # # # ax.pie(data.sum(axis=1), radius=1, colors=colors, wedgeprops=dict(width=0.3, edgecolor='w'))
# # # # ax.legend(labels=db.senders, title="Sender:", shadow=True, loc="best", markerfirst=False)

# # # # # ax.pie(data.flatten(), radius=1-0.3, colors=aplha_colors, wedgeprops=dict(width=0.3, edgecolor='w'))

# # # # ax.set(aspect="equal", title='Pie plot with `ax.pie`')
# # # # plt.show()







# # # # # fig, ax = plt.subplots()

# # # # # vals = np.array([[60., 32.], [37., 40.], [29., 10.]])


# # # # # cmap = cm.get_cmap('Greens')
# # # # # outer_colors = cmap(np.arange(3)*4)
# # # # # inner_colors = cmap([1, 2, 5, 6, 9, 10])

# # # # # ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors,
# # # # # 	   wedgeprops=dict(width=0.3, edgecolor='w'))

# # # # # ax.pie(vals.flatten(), radius=1-0.3, colors=inner_colors,
# # # # # 	   wedgeprops=dict(width=0.3, edgecolor='w'))

# # # # # ax.set(aspect="equal", title='Pie plot with `ax.pie`')
# # # # # plt.show()

# # # # # stat = "messages_max"
# # # # # if "max" in stat or "unique" in stat or "calls" in stat:
# # # # # 	print("Yesss")
# # # # # else:
# # # # # 	print("Nooo")



# # # # # last_sizes = [-100]
# # # # # size = 10

# # # # # last_sizes.append(size) if size != 0 else None
# # # # # size = last_sizes[-1] if size == 0 else size


# # # # # print(f"last_sizes: {last_sizes}, size: {size}")

# # # # # def new_section(space: int=0, size: int=db.last_size[-1], style: str="") -> None:
# # # # # 	db.last_size.append(size)
# # # # # 	print(f"space: {space}, size: {size}, style: {style}")

# # # # # new_section(20)
# # # # # new_section(20, 10, "B")
# # # # # new_section(20)



# # # # # print(GREEN("testing started"))
# # # # # t = [timer()]


# # # # # def cm_colors(cm_name: str, countable):
# # # # # 	if type(countable) != int:
# # # # # 		countable = len(countable)
# # # # # 	return cm.get_cmap(cm_name)(np.linspace(.2, .8, countable+1))


# # # # # # Piechart Message per senders
# # # # # # plt.pie(stats_df.iloc[0:-1, 0], startangle=90, counterclock=False, autopct="%1.1f%%", wedgeprops={"ec": "w"}, colors=cm_colors("Greens_r", senders))
# # # # # # plt.legend(labels=senders, title="Sender:", shadow=True, loc="center left", bbox_to_anchor=(1, .5))
# # # # # # plt.show()

# # # # i=0
# # # # # Piechart with bar types of messages

# # # # # pie chart parameters

# # # # plt.pie(data, autopct="%1.1f%%", startangle=0, counterclock=False,
# # # #         	labels=["Media","Messages"], explode=[.1, 0], colors=cmap("YIGn", 2))

# # # # # bar chart parameters
# # # # age_ratios = stats_df.iloc[i, 7:14]
# # # # age_labels = ["Images", "Videos", "GIFs", "Sticker", "Audios", "Contacts", "Locations", "Files"]
# # # # print(age_ratios)


# # # # plt.show()




# # # # # # ----------------------------------------------------------------
# # # # # t.append(timer())
# # # # # print(GREEN(f"\n testing took {t[-1] - t[-2]} seconds"))
# # # # # # ----------------------------------------------------------------

print(BLUE("\nDONE!"))
# # off(file_end=True)