from database import constants as c, variables as v # to access the database

import pandas as pd # to create DataFrames
import os # to access the operating system
from timeit import default_timer as timer  # for timing


def time(task: str = "untitled") -> None:
	"""
	Adds a new entry to the time DataFrame.
	"""
	v.ts.append(timer())
	print(f"{BLUE(task)} took {BOLD(round(v.ts[-1] - v.ts[-2], 6))} sec")
	return


def export(loc, data, name):
	path = f"data/testing/exports/{loc}/"
	if type(data) != pd.DataFrame:
		data = pd.DataFrame(data)
	try:
		return data.to_csv(path + name, index=True)
	except FileNotFoundError:
		os.makedirs(path, exist_ok=True)
		return export(loc, data, name)


def export_data() -> None:
	"""
	Exports DataFrames and text to the data/testing/exports folder.
	"""
	export("database", v.chat_og, "chat_og_df.csv")
	export("database", v.chat, "chat_df.csv")
	export("database", v.sender, "sender_df.csv")
	export("database", v.stats, "stats_df.csv")
	export("database", v.tstats, "time_stats_df.csv")
	export("database", v.msg_ranges, "msg_ranges_df.csv")
	export("database", v.txt_reports, "reports_df.csv")
	for i in range(v.sc+1):
		try:
			export("database", v.msg_per_s[i], f"msg_per_s{i}.csv")
			export("database", v.common_words[i], f"common_words_s{i}.csv")
			export("database", v.common_emojis[i], f"common_emojis_s{i}.csv")
		except IndexError:
			pass
	time("exporting the database contents")
	return


def off(*args, file_end: bool = False) -> None:
	"""
	Prints error message and safely exits the program.
	"""
	if not file_end:
		return exit(BOLD(RED("⛔️ Error: ")) + " ".join(args) + " ⛔️" if len(args) > 0 else "")
	else:
		print(f"\nAnalyzing took {BOLD(round(timer() - v.ts[0], 6))} seconds")
		print(f"\nYou can find the PDF report here: '{os.getcwd()}/data/output/pdfs/WA-Report.pdf'")
		# export_db()
		return exit()


def pprint(*args, spaces: bool=False) -> str:
    """
    Returns a string of strings/numbers which are divided with spaces, commas 
    and the word "and".
    """
    string = str()
    for i, arg in enumerate(args):
        if i != 0:
            string += " " if spaces else ", " if i+1 < len(args) else " and "
        string += str(arg)
    return string


def BOLD(*args) -> str:
    """
    Returns given arguments seperated by spaces and bold 
    """
    return "\033[1m" + pprint(*args, spaces=True) + "\033[22m"


def DIM(*args) -> str:
    """
    Returns given arguments seperated by spaces and dimmed 
    """
    return "\033[2m" + pprint(*args, spaces=True) + "\033[22m"


def RED(*args) -> str:
    """
    Returns given arguments seperated by spaces and in red 
    """
    return "\033[31m" + pprint(*args, spaces=True) + "\033[39m"


def GREEN(*args) -> str:
    """
    Returns given arguments seperated by spaces and in green 
    """
    return "\033[32m" + pprint(*args, spaces=True) + "\033[39m"


def BLUE(*args) -> str:
    """
    Returns given arguments seperated by spaces and in blue 
    """
    return "\033[34m" + pprint(*args, spaces=True) + "\033[39m"
