import os  # to access the operating system
from timeit import default_timer as timer  # for timing
import pandas as pd  # to create DataFrames

from database import constants as c, variables as v  # to access the database


def time(task: str = "untitled") -> None:
	"""
	Adds a new entry to the time DataFrame.
	"""
	v.ts.append(timer())
	print(f"{BLUE(task)} took {BOLD(round(v.ts[-1] - v.ts[-2], 6))} sec")
	return


def export(data, name) -> None:
	try:
		if type(data) != pd.DataFrame:
			try:
				data = pd.DataFrame(data)
			except ValueError:  # data cant be converted to a pandas DataFrame
				with open("database/exports/" + name + ".txt", "w") as f:
					f.write(data)
				return
		return data.to_csv("database/exports/" + name + ".csv", index=True)
	except OSError:  # create the folder if it does not exist
		os.makedirs("database/exports/", exist_ok=True)
		return export(data, name)


def export_database() -> None:
	"""
	Exports DataFrames and text to the data/testing/exports folder.
	"""
	export(v.chat, "v_chat")
	export(v.chat_og, "v_chat_og")
	export(v.stats, "v_stats")
	export(v.tstats, "v_time_stats")
	export(v.sender, "v_sender")
	export(v.msg_ranges, "v_msg_ranges")
	export(v.txt_reports, "v_txt_reports")
	export(v.time_reports, "v_time_reports")
	export(v.ts, "v_timestamps")
	export(v.msg_per_s[v.sc], "v_msg_per_sc")
	export(v.all_msgs_clean[v.sc], "v_all_msgs_clean_sc")
	export(v.all_msgs, "v_all_msgs")
	for i in range(v.sc):
		export(v.msg_per_s[i], f"v_msg_per_s{i}")
		export(v.common_words[i], f"v_common_words_s{i}")
		export(v.common_emojis[i], f"v_common_emojis_s{i}")
		export(v.word_counts[i], f"v_word_count_s{i}")
		export(v.char_count[i], f"v_char_count_s{i}")
		export(v.all_msgs_clean[i], f"v_all_msgs_clean_s{i}")

	return


def off(*args, error: bool = True) -> None:
	"""
	Prints error message and safely exits the program.
	"""
	# program is ending because of a file error
	exit(" ".join([BOLD(RED("⛔️ Error")), *args, "⛔️"])) if error else None

	# program has finished successfully
	success_msg = [
		BOLD(GREEN("\n✅ Success: Analysis finished ✅")),
		f"Analyzing took {BOLD(round(timer() - v.ts[0], 6))} seconds in total.",
		f"The PDF Report is located here: '{os.getcwd()}/data/output/Report.pdf'\n",
		]
	print("\n".join(success_msg))
	return


def pprint(*args, spaces: bool = False) -> str:
	"""
	Returns a string of strings/numbers which are divided with spaces, commas
	and the word "and".
	"""
	string = str()
	for i, arg in enumerate(args):
		if i != 0:
			string += " " if spaces else ", " if i + 1 < len(args) else " and "
		string += str(arg)
	return string


def BOLD(*args) -> str:
	"""
	Returns given arguments separated by spaces and bold
	"""
	return "\033[1m" + pprint(*args, spaces=True) + "\033[22m"


def RED(*args) -> str:
	"""
	Returns given arguments separated by spaces and in red
	"""
	return "\033[31m" + pprint(*args, spaces=True) + "\033[39m"


def GREEN(*args) -> str:
	"""
	Returns given arguments separated by spaces and in green
	"""
	return "\033[32m" + pprint(*args, spaces=True) + "\033[39m"


def BLUE(*args) -> str:
	"""
	Returns given arguments separated by spaces and in blue
	"""
	return "\033[34m" + pprint(*args, spaces=True) + "\033[39m"
