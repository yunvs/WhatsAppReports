from utils.helper import *

import numpy as np
from matplotlib import pyplot as plt, dates, cm  # to plot figures
from wordcloud import WordCloud  # to create WordClouds

def plot_data() -> None:
	"""
	Creates a textual output for some data and plots the graphics for the report.
	"""
	msg_pie()
	grouped_media_bars()
	message_time_series()
	activity_heatmaps()
	sent_pies()
	
	time("visualizing data for the final pdf report")
	return


def c_m(countable = v.sender, cm_name: str = "Greens_r"):
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
	ax.pie(v.stats.iloc[0:-1, 0], startangle=90, colors=c_m(v.sender), autopct="%1.2f%%", wedgeprops={"ec": "w"}, textprops={"c": "w"})
	ax.legend(labels=v.sender, shadow=True, loc="lower right", fontsize="small")
	ax.set_title("Messages sent")
	ax.axis("equal")

	fig.tight_layout()
	plt.savefig("data/output/images/page1/msg_pie.png", transparent=True)
	plt.close()
	return


def grouped_media_bars(w: float = .9) -> None:
	"""
	Creates a bar chart of the amount of media messages sent by each sender.
	"""
	nums = [11, 7, 8, 10, 9, 17, 12, 13, 14]
	labels = [list(c.STATS_DICT.values())[x].capitalize() for x in nums]
	x = np.arange(len(nums))  # the label locations
	max_val = v.stats.iloc[:v.sc, nums].max().max()

	fig, ax = plt.subplots(figsize=(9, 2.5))
	cmap = c_m(v.sender)
	for i, s in enumerate(v.sender):
		rect = ax.bar((x-w/2) + i*w/v.sc, v.stats.iloc[i, nums], w/v.sc, label=s, align="edge", color=cmap[i])
		ax.bar_label(rect, padding=1) if any(
			[v.sc < 4 and max_val < 1000, v.sc < 6 and max_val < 100, max_val < 10]) else None

	ax.set_title("Media sent by type and sender", loc="left")
	ax.set_ylabel("amount")
	ax.set_xticks(x)
	ax.set_yticks(np.arange(0, max_val, 50), minor=True)
	ax.set_ylim([0, max_val+35])
	ax.grid(True, "both", "y", lw=.8)
	ax.set_xticklabels(labels)

	fig.tight_layout()
	plt.savefig("data/output/images/page1/media_bars.png", transparent=True)
	plt.close()
	return

def message_time_series() -> None:
	"""
	Creates a time series plot of the messages sent over time by each sender
	individually and together.
	"""
	for i, range in enumerate(v.msg_ranges):
		fig, ax = plt.subplots(figsize=(9, 2.5))

		ax.plot(range.index, range.values, color="#10590B")
		# Major ticks every half year, minor ticks every month
		ax.xaxis.set_major_locator(dates.MonthLocator((1, 5, 9), 15))
		ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
		ax.grid(True, "both", "y")
		ax.set_ylabel("amount")
		ax.set_title("Messages sent over time", loc="left")
		ax.xaxis.set_major_formatter(dates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

		fig.tight_layout()
		page = "page1/" if i == v.sc else f"senderpages/s{str(i)}_"
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

	for n in range(v.sc+1):
		df = v.msg_per_s[n] if n != v.sc else v.chat_og

		fig, ax = plt.subplots(figsize=(9, 2.5))
		vals = df.groupby(["weekday", "hour"]).size().unstack().fillna(0).astype(int)
		im = ax.imshow(vals, cmap="Greens")

		# Show all ticks and label them with the respective list entries
		ax.set_xticks(np.arange(len(hours)), labels=hours)
		ax.set_yticks(np.arange(len(days)), labels=[x[:3] for x in days])

		val_max = vals.max().max()

		if val_max < 100:
			for i in range(len(days)):
				for j in range(len(hours)):
					try:
						x = vals.iat[i, j] if vals.iat[i, j] != 0 else ""
						ax.text(j, i, x, ha="center", va="center",
								color="black" if vals.iat[i, j] < val_max/2.5 else "w")
					except IndexError:
						ax.text(j, i, "", ha="center", va="center", color="w")

		cbar = fig.colorbar(im)
		cbar.ax.set_ylabel("messages", rotation=-90, va="bottom")

		fig.tight_layout()
		ax.set_title("Messages sent by day and hour", loc="left")

		page = "page1/" if n == v.sc else f"senderpages/s{str(n)}_"
		fig.savefig(f"data/output/images/{page}heatmap.png", transparent=True)
		plt.close()
	return


def sent_pies() -> None:
	"""
	Creates a pie chart of the sentiment of the messages sent by each sender
	individually and together.
	"""
	for n in range(v.sc+1):
		fig, ax = plt.subplots(figsize=(3.14, 3.14))
		ax.pie(v.stats.iloc[n, [20, 21]], startangle=90, colors=["#9BE7C4", "#FBB3AE"], autopct="%1.1f%%", wedgeprops={"ec": "w"}, textprops={"c": "w"})
		ax.legend(labels=["☺️", "☹"], shadow=True, loc="lower right", fontsize="small")
		ax.axis("equal")
		ax.set_title("Sentiment of rated messages")

		fig.tight_layout()
		page = "page1/" if n == v.sc else f"senderpages/s{str(n)}_"
		fig.savefig(f"data/output/images/{page}sent_pie.png", transparent=True)
		plt.close()
	return


def word_cloud(words: str, i: int) -> None:
	"""
	Creates a word cloud of the given words and saves it to the plots folder.
	"""
	wc = WordCloud(None, 1000, 500, prefer_horizontal=.6, colormap="summer", mode="RGBA", background_color=None, stopwords=c.STOP_WORDS, min_word_length=2, )
	wc.generate(words)
	
	wc.to_file(f"data/output/images/senderpages/s{str(i)}_wc.png")
	return