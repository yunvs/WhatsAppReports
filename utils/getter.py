from utils.helper import *

def get_path(test: bool = False) -> str:
	if not test:
		path = input(BOLD("\nEnter path to file: "))
	else:
		path = "data/input/test_chat.txt"
		path = "/Users/yunusrenz/Others/chat_mum.zip" #TODO: remove

	v.ts = [timer()]
	print(BOLD("Analyzing file"), "@", path, "\n")
	return check_file_format(path)

def check_file_format(path_to_file: str) -> str:
	"""
	Checks if the format of the file is correct and returns correct path.
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