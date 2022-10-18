from utils.helper import *


def create_texts() -> None:
	"""
	Creates the reports for the pdf report.
	"""
	create_txt_reports()
	create_time_reports()
	return


def ss(style: int = 0) -> str:
	"""
	Returns a string represtaion of the senders
	style= 0: auto (default), 1: the n senders, 2: Sender 1, Sender 2 and Sender 3
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


def create_txt_reports() -> None:
	"""
	Creates a report about the sender at the given index which includes the
	statistics about their messages or a summary report.
	"""
	i = int()

	def y(*idxs): return pprint(*[calc_num(*get_stat_pair(a, i)) for a in idxs])


	for i, s in enumerate(v.sender):  # for each sender create a sender report
		ls = [y(0, 6, 18), "\n".join([
			f"Avg. message length: {y(2)} ({y(1)})",
			f"Longest message: {y(4)} ({y(3)})",
			f"{y(15)} were deleted by {s}."])]
		if v.stats.iat[i, 16] != 0:
			ls[-1] += (f"\n{y(16)} by {s} were missed.")
		ls.append(f"In total {s} used {len(v.common_words[i])} distinct words and {len(v.common_emojis[i])} distinct emojis.")
		v.txt_reports.append(ls)

	# General report about all chat messages
	i = v.sc
	v.txt_reports.append([y(0, 6, 18), "\n".join([
		f"Avg. message length: {y(2)} ({y(1)})",
		f"Longest message: {y(4)} ({y(3)})",
		f"{ss()} deleted {y(15)}.",])])
	return


def create_time_reports() -> None:
	"""
	Creates a report about the sender at the given index which includes the
	statistics about their messages or a summary report.
	"""
	for i, s in enumerate(v.sender):  # for each sender create a sender report
		v.time_reports.append([
			f"First message: {v.tstats.iat[i, 0]}",
			f"Most messages: {v.tstats.iat[i, 2]} ({v.tstats.iat[i, 3]} msg.)",
			f"Last message: {v.tstats.iat[i, 1]}",
			f"{s} sent at lest one message on {v.tstats.iat[i, 4]} days and no messages on {v.tstats.iat[i, 5]} days.",
			f"The longest period without any messages from {s} was {int(v.tstats.iat[i, 7])} days.",
			])

	v.time_reports.append([
		f"First message: {v.tstats.iat[i, 0]}",
		f"Most messages: {v.tstats.iat[i, 2]} ({v.tstats.iat[i, 3]} msg.)",
		f"Last message: {v.tstats.iat[i, 1]}",
		f"At lest one message sent on {v.tstats.iat[i, 4]} days.",
		f"Not a single message sent on {v.tstats.iat[i, 5]} days.",
		f"Longest period without any messages: {int(v.tstats.iat[i, 7])} days.",
		])
	return