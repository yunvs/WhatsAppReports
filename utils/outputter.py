from fpdf import FPDF  # to create PDF

from utils.helper import *


pdf = FPDF()


def ss(style: int = 0) -> str:
	"""
	Returns a string representation of the senders.
	style= 0: auto (default), 1: the n senders, 2: Sender 1 and Sender 2
	"""
	short, long = f"the {str(v.sc)} senders", pprint(*v.sender)
	if style != 0:
		return short if style == 1 else long
	else:
		return long if v.sc < 3 else short


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
	return v.stats.iat[sender, stat], list(c.STATS_DICT.values())[stat]


def create_reports() -> None:
	"""
	Creates reports about the messages.
	"""
	create_txt_reports()
	create_time_reports()
	create_nlp_reports()
	return


i = int()


def create_txt_reports() -> None:
	"""
	Creates a report about the sender at the given index which includes general
	statistics about their messages and a summary report.
	"""

	def y(*ids):
		return pprint(*[calc_num(*get_stat_pair(a, i)) for a in ids])

	for i in range(v.sc + 1):  # for each sender create a sender report
		s = v.sender[i] if i != v.sc else ss()
		ls = [y(0, 6, 18)]
		ls.append(
			"\n".join(
				[
					f"Avg. message length: {y(2)} ({y(1)})",
					f"Longest message: {y(4)} ({y(3)})",
					f"{s} deleted {y(15)}.",
				]
			)
		)
		if v.stats.iat[i, 16] != 0:
			ls[-1] += f"\n{y(16)} by {s} were missed."
		ls.append(
			f"{s} used {v.nlp_stats.iat[i, 5]} distinct words"
			+ " and {len(v.common_emojis[i])} distinct emojis."
		)
		v.txt_reports.append(ls)
	return


def create_time_reports() -> None:
	"""
	Creates a report about the sender at the given index which includes
		time statistics about their messages and a summary report.
	"""

	def y(id: int) -> str:
		return v.time_stats.iat[i, id]  # get value of time statistic

	for i, s in enumerate(v.sender):  # for each sender create a sender report
		v.time_reports.append([
			f"First message: {y(0)}",
			f"Most messages: {y(2)} ({int(y(3))} msg.)",
			f"Last message: {y(1)}",
			f"{s} sent at lest one message on {y(4)} days and no messages on {y(5)} days.",
			f"The longest period without any messages from {s} was {int(y(7))} days.",
			f"On average was the time between two messages from {s} {y(8)} days.",
			f"On average {s} sent {y(9)} messages per day.",
		])

	i = v.sc
	v.time_reports.append([
		f"First message: {y(0)}",
		f"Most messages: {y(2)} ({y(3)} msg.)",
		f"Last message: {y(1)}",
		f"At lest one message sent on {y(4)} days.",
		f"Not a single message sent on {y(5)} days.",
		f"Longest period without any messages: {y(7)} days.",
	])
	return


def create_nlp_reports() -> None:
	"""
	Creates a report about the sender at the given index which includes
		NLP statistics about their messages and summary report.
	"""

	def y(id: int) -> str:
		return v.nlp_stats.iat[i, id]

	for i in range(v.sc + 1):
		v.nlp_reports.append([[
			f"Amount of words: {y(0)}; distinct ones: {y(4)}",
			f"Amount of lemmas: {y(1)}; distinct ones: {y(5)}",
			f"Amount of stopwords: {y(2)}; distinct ones: {y(6)}",
			f"Amount of non-stopword words: {y(3)}; distinct ones: {y(7)}",
			f"Average word length: {y(8)} chars",
			f"Amount of recognized named entities: {v.named_entities_counts[i]}",
		]])
	return


def new_section(size: int = -1, style: str = "", color: tuple[int, int, int] = (0, 0, 0), space: int = 0, xy: tuple[int, int] = (-1, -1),) -> None:
	"""
	Creates a new section by setting the font size, style and color for the
	next text to be added to the pdf and setting the given position.
	"""
	v.last_txt_size = size if size != -1 else v.last_txt_size  # save last size
	pdf.set_font("Arial", style, size if size != -1 else v.last_txt_size)
	pdf.set_text_color(*color)
	if space != 0:
		pdf.ln(space)
	if xy != (-1, -1):
		pdf.set_xy(*xy)
	return


def add_title_footer(n: int = v.sc) -> None:
	"""
	Inserts the title of the page and the footer with the page number.
	"""
	pdf.set_margins(20, 20, 20) if pdf.page_no() == 0 else None

	pdf.add_page()  # add new page
	page = pdf.page_no()

	# Create title of current page
	new_section(18, "B")
	pdf.cell(0, 10, "WhatsApp Chat Statistics", align="C")
	new_section(12, space=5)
	xy = (pdf.get_x(), pdf.get_y())
	pdf.cell(0, 12, "for " + str(ss() if n == v.sc else v.sender[n]), align="C")

	# Create footer of current page
	new_section(10, "I", xy=(20, 270))
	desc = str("General" if n == v.sc else "Sender specific") + " statistics"
	s_str = ss(1) if n == v.sc else v.sender[n]
	pdf.cell(0, 5, f"Page {str(page)}: {desc} for {s_str}", align="C")

	new_section(11, xy=xy)
	return


def insert_media_table(s_no: int = -1, w: int = 24, h: int = 6) -> None:
	"""
	Inserts the amounts of media types sent by a sender into a table.
	"""
	new_section(12, "B", space=4)
	for i, x in enumerate([11, 12, 7, 13, 8, 14, 10, 17, 9]):
		if i == 0:
			pdf.cell(w * 4 - 8, h + 2, "Media types and amount sent", 0, 1, "C")
			new_section(11)
		value = str(v.stats.iat[v.sc if s_no == -1 else s_no, x])
		item = list(c.STATS_DICT.values())[x] + "s" if value != 1 else ""
		pdf.cell(w, h, item.capitalize(), 1, 0, "C")
		pdf.cell(w - 4, h, value, 1, 0, "C")
		if i % 2 != 0:
			pdf.ln(h)
	return


def commons_table(df: pd.DataFrame, x: int, y: int, w: int = 60, h: int = 6, emojis: bool = False) -> None:
	"""
	Prints a DataFrame of common words/emojis to a table in a pdf file
	"""
	# Create table header
	new_section(10, "B", xy=(x, y))
	pdf.cell(w, h, f"Top {len(df)} {df.columns[0]}s", align="C", border=1)
	pdf.cell(20, h, df.columns[1], align="C", border=1)

	# Create table body
	new_section(xy=(x, pdf.get_y() + h))

	for i in range(len(df)):
		if emojis:  # Emojis: inserted as link to a google image search
			emoji = df.iat[i, 0].strip(":").replace("_", "+")
			url = f"https://www.google.com/search?q={emoji}+emoji&tbm=isch"
			new_section(style="U", color=(0, 0, 200))  # blue underline
			pdf.cell(w, h, emoji.replace("+", " ")[: int(w * 0.8)], align="C", border=1, link=url)
			new_section(color=(0, 0, 0))
		else:  # Words are inserted as link to the google search
			pdf.cell(w, h, df.iat[i, 0][: int(w * 0.8)], align="C", border=1)
		pdf.cell(20, h, str(df.iat[i, 1]), align="C", border=1)
		new_section(xy=(x, pdf.get_y() + h))
	return


def ts_info(x: float, y: float, s_no: int = -1) -> None:
	"""
	Prints Date of first and last message and date of most active day
	"""
	new_section(10, xy=(x, y))
	pdf.cell(165, 0, v.time_reports[s_no][0], align="L")  # First message
	new_section(xy=(x, y))
	pdf.cell(165, 0, v.time_reports[s_no][1], align="C")  # Most active day
	new_section(xy=(x, y))
	pdf.cell(165, 0, v.time_reports[s_no][2], align="R")  # Last message
	return


def add_nlp_page(i: int = v.sc) -> None:
	"""
	Adds a page with the NLP statistics to the pdf file.
	"""

	new_section(12, "B", space=12)
	pdf.cell(0, 5, "Natural Language Processing Analysis")

	new_section(11, space=10)
	pdf.multi_cell(0, 4, "\n".join(v.nlp_reports[i][0]))  # insert nlp stats

	new_section(12, "B", space=5)
	pdf.cell(175, 10, "POS Tags and counts", align="C")
	new_section(11)
	for n, (key, val) in enumerate(v.pos_tags[i].items()):
		if n % 3 == 0:
			pdf.ln(8)
		new_section(style="B")
		pdf.cell(170 / 6, 8, key, align="C", border=1, ln=0)
		new_section()
		pdf.cell(170 / 6, 8, str(val), align="C", border=1, ln=0)

	# insert the 20 most common lemmas and stopwords of the sender
	commons_table(v.frequencies[i][1].head(20), x=20, y=135)
	commons_table(v.frequencies[i][2].head(20), x=110, y=135)
	return


def make_pdf_report() -> None:
	"""
	Creates a pdf file with a summary of the chat and the statistics
	"""
	create_reports()

	path = "data/output/images/generalpage/"
	i = v.sc

	add_title_footer(i)  # Add first page of report

	new_section(11, space=20)
	# insert the amount of texts, media and emojis sent by all senders
	pdf.cell(90, 0, "This conversation contains")
	new_section(14, "B", space=3)
	pdf.multi_cell(110, 5, v.txt_reports[i][0])

	# insert avg, longest length and some other stats for all senders
	new_section(11, space=10)
	pdf.multi_cell(100, 4, v.txt_reports[i][1])

	# insert the general time-wise statistics
	new_section(space=10)
	pdf.multi_cell(100, 4, "\n".join(v.time_reports[i][3:]))

	pdf.image(path + "msg_pie.png", x=120, y=35, w=79)  # messages pie chart
	pdf.image(path + "media_bars.png", x=15, y=105, w=180)  # media bar chart

	pdf.image(path + "ts.png", x=15, y=155, w=180)  # activity time series plot
	ts_info(25, 205)  # insert information underneath time series plot

	pdf.image(path + "heatmap.png", x=15, y=215, w=190)  # activity heatmap plot

	add_title_footer(i)  # Add second page of report

	pdf.image(path + "char_violinplot.png", x=15, y=50, w=90)  # char violinplot
	pdf.image(path + "char_boxplot.png", x=105, y=50, w=90)  # word violinplot

	pdf.image(path + "word_violinplot.png", x=15, y=160, w=90)  # char boxplot
	pdf.image(path + "word_boxplot.png", x=105, y=160, w=90)  # word boxplot

	add_title_footer(i)  # Add third page of report

	pdf.image(path + "wc.png", x=20, y=37.5, w=170)  # WordCloud

	# insert the 20 most common words and emojis of the sender
	commons_table(v.frequencies[i][0].head(20), x=20, y=130)
	commons_table(v.common_emojis[i].head(20), x=110, y=130, emojis=True)

	# insert the total number of distinct words and emojis sent by the sender
	new_section(11, "B", xy=(20, 260))
	pdf.cell(90, 5, v.txt_reports[i][2], align="L")

	add_title_footer(i)  # Add fourth page of general report
	add_nlp_page()

	for i, s in enumerate(v.sender):  # loops over all senders
		path = f"data/output/images/senderpages/s{str(i)}_"

		add_title_footer(i)  # Adds first sender page for sender s

		# insert the amount of texts, media and emojis sent by the sender
		new_section(11, space=20)
		pdf.cell(90, 0, f"Messages {s} sent contain")
		new_section(14, "B", space=3)
		pdf.multi_cell(110, 5, v.txt_reports[i][0])

		# insert the amount of media sent and some other stats about the sender
		insert_media_table(i)
		new_section(11, space=15)
		pdf.multi_cell(110, 4, v.txt_reports[i][1])

		# insert the 20 most common words and emojis of the sender
		commons_table(v.frequencies[i][0].head(20), x=20, y=130)
		commons_table(v.common_emojis[i].head(20), x=110, y=130, emojis=True)

		# insert the total number of distinct words and emojis sent by the sender
		new_section(11, "B", xy=(20, 260))
		pdf.cell(90, 5, v.txt_reports[i][2], align="L")

		pdf.image(path + "sent_pie.png", x=115, y=40, w=84)  # sentiment plot

		add_title_footer(i)  # add second sender page for time stats

		pdf.image(path + "ts.png", x=15, y=40, w=180)  # activity time series plot
		ts_info(25, 90, i)  # insert information underneath time series plot

		# insert the time-wise statistics of the sender
		new_section(11, space=10)
		pdf.multi_cell(0, 4, "\n".join(v.time_reports[i][3:]))

		pdf.image(path + "heatmap.png", x=15, y=120, w=190)  # heatmap plot
		pdf.image(path + "wc.png", x=20, y=180, w=170)  # WordCloud

		add_title_footer(i)  # add third sender page for sender s
		add_nlp_page(i)

	pdf.output("data/output/Report.pdf", "F")
	time("Finishing final PDF Report")
	return
