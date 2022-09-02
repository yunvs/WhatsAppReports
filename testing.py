from myfuncs import *

# from timeit import default_timer as timer
# from ast import Str
# from hashlib import new
# from pickletools import int4
# from matplotlib import cm
# import database as db
# import numpy as np

# # ----------------------------------------------------------------
stats_df = pd.read_csv("data/testing/exports/database/stats_df.csv", index_col=0)
senders = list(pd.read_csv("data/testing/exports/database/senders_df.csv", index_col=0)["0"])
chat_og = pd.read_csv("data/testing/exports/database/chat_og.csv", index_col=0)
msg = stats_df.iloc[0:-1, 0]
# # ----------------------------------------------------------------



def make_pdf_report1() -> None:
	"""
	Creates a pdf file with a summary of the chat and the statistics
	"""
	# add_title_footer()
	pdf.add_page()
	path = "data/output/images/page1/"
	
	# new_section(11, space=20)
	# pdf.cell(90, 1, "This conversation contains")
	# new_section(14, "B", space=3)
	# pdf.multi_cell(110, 5, db.reports[db.sc][0])

	# new_section(space=4)
	# print_stats()

	# new_section(11, space=14)
	# pdf.multi_cell(110, 4, db.reports[db.sc][1])

	pdf.image(path+"msg_pie.png", x=80, y=20-30, w=150)
	pdf.image(path+"ts.png", x=0, y=120-30, w=210)


	for i, s in enumerate(senders):
		pdf.add_page()
		path = "data/output/images/senderpages/s" + str(i)

		# new_section(11, space=20)
		# pdf.cell(90, 1, f"{s} messages contain")
		# new_section(14, "B", space=3)
		# pdf.multi_cell(110, 5, db.reports[i][0])

		# new_section(space=4)
		# print_stats(i)

		# new_section(11, space=14)
		# pdf.multi_cell(110, 4, db.reports[i][1])

		
		pdf.image(path+"_ts.png", x=0, y=120-30, w=210)


		# add_title_footer(i)
		pdf.image(path+"_wc.png", x=113, y=33-30, w=88)

	pdf.output("data/testing/testing.pdf", "F")


senders = ["1", "2"]


def stacked_bars_media() -> None:
	"""
	Plots the stcked bar chRT bout data and senders
	"""

	# data
	nums = [11, 7, 8, 10, 9, 12, 13, 14, 17]
	labels = [list(db.stats_dict.values())[x] for x in nums]
	for i, s in enumerate(senders):


		# plotting
		width = .35
		fig, ax = plt.subplots()
		ax.bar(labels, stats_df.iat[i, nums], width, label=s)






pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=11)
make_pdf_report1()
time("@make_pdf_report1")






















# sizes: list[int] = list() # last text sizes

# def get_coord(x_offset: int=0, y_offset: int=0) -> tuple[int, int]:
# 	"""
# 	Returns the x, y cordinates on the current page
# 	"""
# 	return (pdf.get_x() + x_offset), (pdf.get_y() + y_offset)

# def new_section(size: int=0, style: str="", space: int=0, np: int=0) -> None:
# 	"""
# 	Creates a new section in the pdf file and sets the font size and style.
# 	np: -1 = only footer, 0 = no new page (default), 1 = new page, 2 = new page and new section
# 	"""
# 	if pdf.page_no() == 0: # create first page
# 		pdf.set_margins(15, 20, 15)
# 		pdf.add_page()
# 	if np in (-1, 1, 2): # create footer for current page
# 		pdf.set_xy(0, 270)
# 		new_section(8, "I")
# 		pdf.cell(0, 5, f"Page {pdf.page_no()}", align="C")
# 	pdf.add_page() if np in (1, 2) else None # create new page
# 	if np in (0, 2): # create new section	on current or new page
# 		pdf.ln(space)
# 		xys.append({"x": pdf.get_x(), "y": pdf.get_y()})
# 		sizes.append(size) if size != 0 else None
# 		pdf.set_font("Arial", style, size if size != 0 else sizes[-1])
# 	return None





# pdf = FPDF()
# pdf.add_page()
# pdf.set_font("Arial", size=11)

# # i = db.sc
# # def y(*idxs): return say(*[calc_numerus(*get_stat_pair(x, i)) for x in idxs])
# """	f"The {db.sc} senders ...", f"... sent {y(11,7,8,10,9)}", 
# 	f"... shared {y(12,13,14,17)}", f"... deleted {y(15)} in this chat"]) """




# new_section(11, "", space=20)
# pdf.multi_cell(90, 4, x)

# new_section(space=20)

# l1 = [	11,	12, 
# 		7, 	13, 
# 		8, 	14, 
# 		10,	17,
# 		9]
# l2 = [stats_df.iat[len(senders), item] for item in l1]
# w, h = 90, 6
# w_item = 21
# w_value = len(str(max(l2)))*5

# for i, x in enumerate(l1):
# 	if i == 0:
# 		pdf.set_font("Arial", "B", 12)
# 		pdf.cell(w, h+2, "Media types and amount sent", 0, 1, "C")
# 		# pdf.cell(w, h, "media", 1, 0, "C")
# 		# pdf.cell(w, h, "count", 1, 0, "C")
# 		# pdf.cell(w, h, "media", 1, 0, "C")
# 		# pdf.cell(w, h, "count", 1, 1, "C")
# 	pdf.set_font("Arial", "", 11)
# 	pdf.cell(w_item, h, list(db.stats_dict.values())[x].capitalize()+"s", 1, 0, "C")
# 	pdf.cell(w_value, h, str(l2[i]), 1, 0, "C")
# 	if i % 2 != 0:
# 		pdf.ln(h)
# 	else:
# 		pdf.set_xy(pdf.get_x() + (w - (w_item + w_value) * 2), pdf.get_y())


# new_section(space=20)
# pdf.multi_cell(90, 4, "Hello this is the end of the report")


# new_section(space=20)


# l1 = [	11,	12, 
# 		7, 	13, 
# 		8, 	14, 
# 		10,	17,
# 		9]
# l2 = [stats_df.iat[len(senders), item] for item in l1]
# w, h = 90, 6
# w_item, w_value = 20, len(str(max(l2)))*5

# for i, x in enumerate(l1):
# 	if i == 0:
# 		pdf.set_font("Arial", "B", 11)
# 		pdf.cell(w, h, "Media types and amount sent", 0, 1, "C")
# 		# pdf.cell(w, h, "media", 1, 0, "C")
# 		# pdf.cell(w, h, "count", 1, 0, "C")
# 		# pdf.cell(w, h, "media", 1, 0, "C")
# 		# pdf.cell(w, h, "count", 1, 1, "C")
# 	pdf.set_font("Arial", "", 11)
# 	pdf.cell(w_item, h, list(db.stats_dict.values())[x], 1, 0, "C")
# 	pdf.cell(w_value, h, str(l2[i]), 1, 0, "C")
# 	if i % 2 != 0:
# 		pdf.ln(h)
# 	else:
# 		pdf.set_xy(pdf.get_x() + (w - (w_item + w_value) * 2), pdf.get_y())




# pdf.output("data/output/pdfs/testing.pdf", "F")




# zz = chat_og["date"].value_counts().sort_index()
# date_range = pd.date_range(start=zz.index[0], end=zz.index[-1])

# msg_date = pd.Series(index=date_range, dtype=int)
# for date in date_range.strftime('%Y-%m-%d'):
# 	msg_date[date] = zz[date] if date in zz.index else 0

# fig, ax = plt.subplots(figsize=(12, 4))

# ax.plot(msg_date.index, msg_date.values, color="green")
# # # Major ticks every half year, minor ticks every month,
# ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
# ax.xaxis.set_minor_locator(mdates.MonthLocator())
# ax.grid(True)
# ax.set_ylabel('Messages sent')


# ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))


# # for label in ax.get_xticklabels(which='major'):
# # 	label.set(rotation=30, horizontalalignment='right')

# plt.show()








# # Testing Area:
# data = []
# for i in range(len(senders)):
# 	data.append([stats_df.iloc[i,0], stats_df.iloc[i,6]])
# data = np.array(data)
# print(data)


# # # ----------------------------------------------------------------
# fig, ax = plt.subplots()

# # cmap = plt.colormaps["tab20c"]
# # outer_colors = cmap(np.arange(3)*4)
# # inner_colors = cmap([1  , 2, 5, 6, 9, 10])

# # ax.pie(msg, startangle=90, counterclock=False, autopct="%1.1f%%", wedgeprops={"ec": "w"}, colors=cm_colors("Greens_r", db.senders))

# colors = cmap("Greens_r", db.senders)
# aplha_colors = colors[:, 3] = 0.8

# ax.pie(data.sum(axis=1), radius=1, colors=colors, wedgeprops=dict(width=0.3, edgecolor='w'))
# ax.legend(labels=db.senders, title="Sender:", shadow=True, loc="best", markerfirst=False)

# # ax.pie(data.flatten(), radius=1-0.3, colors=aplha_colors, wedgeprops=dict(width=0.3, edgecolor='w'))

# ax.set(aspect="equal", title='Pie plot with `ax.pie`')
# plt.show()







# # fig, ax = plt.subplots()

# # vals = np.array([[60., 32.], [37., 40.], [29., 10.]])


# # cmap = cm.get_cmap('Greens')
# # outer_colors = cmap(np.arange(3)*4)
# # inner_colors = cmap([1, 2, 5, 6, 9, 10])

# # ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors,
# # 	   wedgeprops=dict(width=0.3, edgecolor='w'))

# # ax.pie(vals.flatten(), radius=1-0.3, colors=inner_colors,
# # 	   wedgeprops=dict(width=0.3, edgecolor='w'))

# # ax.set(aspect="equal", title='Pie plot with `ax.pie`')
# # plt.show()

# # stat = "messages_max"
# # if "max" in stat or "unique" in stat or "calls" in stat:
# # 	print("Yesss")
# # else:
# # 	print("Nooo")



# # last_sizes = [-100]
# # size = 10

# # last_sizes.append(size) if size != 0 else None
# # size = last_sizes[-1] if size == 0 else size


# # print(f"last_sizes: {last_sizes}, size: {size}")

# # def new_section(space: int=0, size: int=db.last_size[-1], style: str="") -> None:
# # 	db.last_size.append(size)
# # 	print(f"space: {space}, size: {size}, style: {style}")

# # new_section(20)
# # new_section(20, 10, "B")
# # new_section(20)



# # print(GREEN("testing started"))
# # t = [timer()]


# # def cm_colors(cm_name: str, countable):
# # 	if type(countable) != int:
# # 		countable = len(countable)
# # 	return cm.get_cmap(cm_name)(np.linspace(.2, .8, countable+1))


# # # Piechart Message per senders
# # # plt.pie(stats_df.iloc[0:-1, 0], startangle=90, counterclock=False, autopct="%1.1f%%", wedgeprops={"ec": "w"}, colors=cm_colors("Greens_r", senders))
# # # plt.legend(labels=senders, title="Sender:", shadow=True, loc="center left", bbox_to_anchor=(1, .5))
# # # plt.show()

# i=0
# # Piechart with bar types of messages

# # pie chart parameters

# plt.pie(data, autopct="%1.1f%%", startangle=0, counterclock=False,
#         	labels=["Media","Messages"], explode=[.1, 0], colors=cmap("YIGn", 2))

# # bar chart parameters
# age_ratios = stats_df.iloc[i, 7:14]
# age_labels = ["Images", "Videos", "GIFs", "Sticker", "Audios", "Contacts", "Locations", "Files"]
# print(age_ratios)


# plt.show()




# # # ----------------------------------------------------------------
# # t.append(timer())
# # print(GREEN(f"\n testing took {t[-1] - t[-2]} seconds"))
# # # ----------------------------------------------------------------

print(BLUE("\nDONE"))
off(file_end=True)