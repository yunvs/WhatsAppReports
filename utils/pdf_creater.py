from utils.helper import *
from utils.outputer import ss

from fpdf import FPDF  # to create pdfs

pdf = FPDF()

def new_section(size: int = -1, style: str = "", color: tuple[int, int, int] = (0, 0, 0), space: int = 0, xy: tuple[int, int] = (-1, -1)) -> None:
	"""
	Creates a new section by setting the font size, style and color for the 
	next text to be added to the pdf and setting the given position.
	"""
	v.last_text_size = size if size != -1 else v.last_text_size # save last size
	pdf.set_font("Arial", style, size if size != -1 else v.last_text_size) 
	pdf.set_text_color(*color) 
	if space != 0: 
		pdf.ln(space)
	if xy != (-1, -1):
		pdf.set_xy(*xy)
	return


def add_title_footer(n: int = -1) -> None:
	"""
	Inserts the title of the page and the footer with the page number.
	"""
	pdf.set_margins(20, 20, 20) if pdf.page_no() == 0 else None

	pdf.add_page()
	page = pdf.page_no()

	# Create title of current page
	new_section(18, "B")
	pdf.cell(0, 10, "WhatsApp Chat Statistics", align="C")
	new_section(12, space=5)
	xy = (pdf.get_x(), pdf.get_y())
	pdf.cell(0, 12, "for " + str(ss() if n == -1 else v.sender[n]), align="C")

	# Create footer of current page
	new_section(10, "I", xy=(20, 270))
	desc = str("General" if page == 1 else "Sender specific") + " statistics"
	s_str = ss(1) if n == -1 else v.sender[n]
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
			pdf.cell(w*4-8, h+2, "Media types and amount sent", 0, 1, "C")
			new_section(11)
		value = str(v.stats.iat[v.sc if s_no == -1 else s_no, x])
		item = list(c.STATS_DICT.values())[x] + "s" if value != 1 else ""
		pdf.cell(w, h, item.capitalize(), 1, 0, "C")
		pdf.cell(w-4, h, value, 1, 0, "C")
		if i % 2 != 0:
			pdf.ln(h)
	return


def commons_table(df: pd.DataFrame, x: int, y: int, w: int = 60, h: int = 6, emojis: bool = False) -> None:
	"""
	Prints a DataFrame of common words/emojis to a table in a pdf file
	"""
	# Create table header
	new_section(10, "B", xy=(x, y))
	pdf.cell(w, h, f"TOP {len(df)} {df.columns[0]}s", align="C", border=1)
	pdf.cell(20, h, df.columns[1], align="C", border=1)

	# Create table body
	new_section(xy=(x, pdf.get_y() + h))
	for i in range(len(df)):
		if emojis: # Emojis: inserted as link to the google search
			emoji = df.iat[i, 0].strip(":").replace("_", "+")
			url = f"https://www.google.com/search?q={emoji}+emoji&tbm=isch"
			new_section(style="U", color=(0, 0, 200)) # 
			pdf.cell(w, h, emoji.replace("+", " ")[:int(w*.8)], align="C", border=1, link=url)
			new_section(color=(0, 0, 0))
		else: # Words are inserted as link to the google search
			pdf.cell(w, h, df.iat[i, 0][:int(w*.8)], align="C", border=1)
		pdf.cell(20, h, str(df.iat[i, 1]), align="C", border=1)
		new_section(xy=(x, pdf.get_y() + h))
	return

def ts_info(x: float, y: float, s_no: int = -1) -> None:
	"""
	Prints Date of first and last message and date of most active day
	"""
	new_section(10, xy=(x, y))
	pdf.cell(165, 0, v.time_reports[s_no][0], align="L") # First message
	new_section(xy=(x, y))
	pdf.cell(165, 0, v.time_reports[s_no][1], align="C") # Most active day
	new_section(xy=(x, y))
	pdf.cell(165, 0, v.time_reports[s_no][2], align="R") # Last message
	return


def make_pdf_report() -> None:
	"""
	Creates a pdf file with a summary of the chat and the statistics
	"""
	path = "data/output/images/page1/"

	add_title_footer() # Add first page of report

	# Insert the amount of texts, media and emojis sent by all senders
	new_section(11, space=20)
	pdf.cell(90, 0, "This conversation contains")
	new_section(14, "B", space=3)
	pdf.multi_cell(110, 5, v.txt_reports[v.sc][0])

	# Insert avg, longest length and some other stats for all senders
	new_section(11, space=10)
	pdf.multi_cell(100, 4, v.txt_reports[v.sc][1])

	# Insert the general timewise statistics
	new_section(space=10)
	pdf.multi_cell(100, 4, "\n".join(v.time_reports[v.sc][3:]))

	pdf.image(path+"msg_pie.png", x=120, y=35, w=79) # messages pie chart
	pdf.image(path+"media_bars.png", x=15, y=105, w=180) # media bar chart

	pdf.image(path+"ts.png", x=15, y=155, w=180) # activity time series plot
	ts_info(25, 205) # Print information underneth time series plot

	pdf.image(path+"heatmap.png", x=15, y=215, w=190) # activity heatmap plot

	for i, s in enumerate(v.sender): # loops over all senders
		path = f"data/output/images/senderpages/s{str(i)}_"

		add_title_footer(i) # Adds first sender page for sender s

		# Insert the amount of texts, media and emojis sent by the sender 
		new_section(11, space=20)
		pdf.cell(90, 0, f"Messages {s} sent contain")
		new_section(14, "B", space=3)
		pdf.multi_cell(110, 5, v.txt_reports[i][0])

		# Insert the amount of media sent and some other stats about the sender
		insert_media_table(i)
		new_section(11, space=15)
		pdf.multi_cell(110, 4, v.txt_reports[i][1])

		# Insert the 20 most common words and emojis of the sender
		commons_table(v.common_words[i].head(20), x=20, y=130)
		commons_table(v.common_emojis[i].head(20), x=110, y=130, emojis=True)

		# Insert the total number of distinct words and emojis sent by the sender
		new_section(11, "B", xy=(20, 260))
		pdf.cell(90, 5, v.txt_reports[i][2], align="L")

		pdf.image(path+"sent_pie.png", x=115, y=40, w=84) # Sentiment plot


		add_title_footer(i) # Add second sender page for time stats

		pdf.image(path+"ts.png", x=15, y=40, w=180) # Activity time series plot
		ts_info(25, 90, i) # Insert information underneth time series plot

		# Insert the timewise statistics of the sender
		new_section(11, space=10)
		pdf.multi_cell(0, 4, "\n".join(v.time_reports[i][3:]))

		pdf.image(path+"heatmap.png", x=15, y=120, w=190) # Heatmap plot
		pdf.image(path+"wc.png", x=20, y=180, w=170) # Wordcloud 
	
	pdf.output("data/output/pdfs/WA-Report.pdf", "F")
	time("finishing final PDF Report")
	return
