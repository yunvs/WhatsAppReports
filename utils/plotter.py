import numpy as np
from matplotlib import cm, dates
from matplotlib import pyplot as plt  # to plot figures
from wordcloud import WordCloud  # to create WordClouds
from nltk.corpus import stopwords

from utils.helper import *


def plot_data() -> None:
	"""
	Creates a textual output for some data and plots the graphics for the report.
	"""
	for i in range(v.sc):
		page = f"data/output/images/senderpages/s{str(i)}_"
		message_time_series(i, page)
		activity_heatmaps(i, page)
		sent_pies(i, page)

		word_cloud(v.all_msgs_clean[i], page)

		time(f"Visualizing data for sender {str(i+1)} / {str(v.sc)}")

	page = "data/output/images/generalpage/"
	msg_pie()
	grouped_media_bars()
	message_time_series(v.sc, page)
	activity_heatmaps(v.sc, page)
	sent_pies(v.sc, page)
	violinplot(page)
	boxplot(page)

	word_cloud(" ".join(v.all_msgs_clean), page)

	time("Visualizing remaining data")
	return


def c_m(countable=v.sender, cm_name: str = "Greens_r"):
	"""
	Returns a colormap for the amount needed of the given countable.
	"""
	if type(countable) != int:
		countable = len(countable)
	return cm.get_cmap(cm_name)(np.linspace(0.2, 0.8, countable + 1))


def msg_pie() -> None:
	"""
	Creates a pie chart of the amount of messages sent by each sender.
	"""
	fig, ax = plt.subplots(figsize=(3.14, 3.14))
	ax.pie(
		v.stats.iloc[0:-1, 0],
		startangle=90,
		colors=c_m(v.sender),
		autopct="%1.2f%%",
		wedgeprops={"ec": "w"},
		textprops={"c": "w"},
	)
	ax.legend(labels=v.sender, shadow=True, loc="lower right", fontsize="small")
	ax.set_title("Messages sent")
	ax.axis("equal")

	fig.tight_layout()
	plt.savefig("data/output/images/generalpage/msg_pie.png", transparent=True)
	plt.close()
	return


def grouped_media_bars(w: float = 0.9) -> None:
	"""
	Creates a bar chart of the amount of media messages sent by each sender.
	"""
	nums = [11, 7, 8, 10, 9, 17, 12, 13, 14]
	labels = [list(c.STATS_DICT.values())[x].capitalize() for x in nums]
	x = np.arange(len(nums))  # the label locations
	max_val = v.stats.iloc[: v.sc, nums].max().max()

	fig, ax = plt.subplots(figsize=(7.2, 2))
	cmap = c_m(v.sender)
	for i, s in enumerate(v.sender):
		rect = ax.bar(
			(x - w / 2) + i * w / v.sc,
			v.stats.iloc[i, nums],
			w / v.sc,
			label=s,
			align="edge",
			color=cmap[i],
		)
		ax.bar_label(rect, padding=1) if any(
			[v.sc < 4 and max_val < 1000, v.sc < 6 and max_val < 100, max_val < 10]
		) else None

	ax.set_title("Media sent by type and sender", loc="left")
	ax.set_ylabel("amount")
	ax.set_xticks(x)
	ax.set_yticks(np.arange(0, max_val, 50), minor=True)
	ax.set_ylim([0, max_val + 35])
	ax.grid(True, "both", "y", lw=0.8)
	ax.set_xticklabels(labels)

	fig.tight_layout()
	plt.savefig("data/output/images/generalpage/media_bars.png", transparent=True)
	plt.close()
	return


def message_time_series(s_no: int, page: str) -> None:
	"""
	Creates a time series plot of the messages sent over time.
	"""
	msg_range = v.msg_ranges[s_no]
	fig, ax = plt.subplots(figsize=(7.2, 2))

	ax.plot(msg_range.index, msg_range.values, color="#10590B")
	# Major ticks every half year, minor ticks every month
	ax.xaxis.set_major_locator(dates.MonthLocator((1, 5, 9), 15))
	ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
	ax.grid(True, "both", "y")
	ax.set_ylabel("amount")
	ax.set_title("Messages sent over time", loc="left")
	ax.xaxis.set_major_formatter(
		dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
	)

	fig.tight_layout()
	fig.savefig(page + "ts.png", transparent=True)
	plt.close()
	return


def activity_heatmaps(s_no: int, page: str) -> None:
	"""
	Creates a heatmap of the activity in the chat.
	"""
	df = v.msg_per_s[s_no] if s_no != v.sc else v.chat_og

	fig, ax = plt.subplots(figsize=(7.2, 2))
	vals = df.groupby(["weekday", "hour"]).size().unstack().fillna(0).astype(int)
	im = ax.imshow(vals, cmap="Greens")

	# Show all ticks and label them with the respective list entries
	ax.set_xticks(np.arange(len(c.HOURS)), labels=c.HOURS)
	ax.set_yticks(np.arange(len(c.DAYS)), labels=[x[:3] for x in c.DAYS])

	val_max = vals.max().max()

	if val_max < 100:
		for i in range(len(c.DAYS)):
			for j in range(len(c.HOURS)):
				try:
					x = vals.iat[i, j] if vals.iat[i, j] != 0 else ""
					ax.text(
						j,
						i,
						x,
						ha="center",
						va="center",
						color="black" if vals.iat[i, j] < val_max / 2.5 else "w",
					)
				except IndexError:
					continue

	cbar = fig.colorbar(im)
	cbar.ax.set_ylabel("messages", rotation=-90, va="bottom")

	ax.set_title("Messages sent by day and hour", loc="left")

	fig.tight_layout()
	fig.savefig(page + "heatmap.png", transparent=True)
	plt.close()
	return


def sent_pies(s_no: int, page: str) -> None:
	"""
	Creates a pie chart of the sentiment of the messages sent.
	"""
	fig, ax = plt.subplots(figsize=(3.14, 3.14))
	ax.pie(
		v.stats.iloc[s_no, [20, 21]],
		startangle=90,
		colors=["#C2E1FF", "#F9D6D5"],
		autopct="%1.1f%%",
		wedgeprops={"ec": "w"},
		textprops={"c": "w"},
	)
	ax.legend(labels=["☺️", "☹"], shadow=True, loc="lower right", fontsize="small")
	ax.axis("equal")
	ax.set_title("Sentiment of rated messages")

	fig.tight_layout()
	fig.savefig(page + "sent_pie.png", transparent=True)
	plt.close()
	return


def violinplot(page: str) -> None:
	"""
	Creates a box plot of the message length and word count.
	"""
	for (df, title) in [(v.char_counts, "char"), (v.word_counts, "word")]:
		fig, ax = plt.subplots(figsize=(4, 4))
		ax.violinplot(df, showmeans=True, showmedians=True)
		ax.set_xticks([y + 1 for y in range(len(df))], labels=v.sender)

		ax.set_title(f"Violinplot: {title} count per message")
		ax.set_ylabel("Observed values")
		ax.yaxis.grid(True)
		fig.tight_layout()
		fig.savefig(page + title + "_violinplot.png", transparent=True)
		plt.close()
	return


def boxplot(page: str) -> None:
	"""
	Creates a box plot of the message length and word count.
	"""
	for (df, title) in [(v.char_counts, "char"), (v.word_counts, "word")]:
		fig, ax = plt.subplots(figsize=(4, 4))
		ax.boxplot(df, True, "", True, patch_artist=True, labels=v.sender)
		ax.set_title(f"Boxplot: {title} count per message")
		ax.set_ylabel("Observed values")
		ax.yaxis.grid(True)
		fig.tight_layout()
		fig.savefig(page + title + "_boxplot.png", transparent=True)
		plt.close()
	return


def word_cloud(words: str, page: str) -> None:
	"""
	Creates a word cloud of the given words and saves it to the plots folder.
	"""
	wc = WordCloud( None, 1000, 500, prefer_horizontal=0.6, colormap="summer", mode="RGBA", background_color=None, stopwords=set(stopwords.words("german")), min_word_length=2,)
	if words != "":
		wc.generate(words)
		wc.to_file(page + "wc.png")
	return
