from utils.helper import *


def get_file(path_to_file: str = "") -> list[str]:
	"""
	Returns the chat file as a list of strings.
	"""
	if path_to_file == "":
		path_to_file = get_path()

	if path_to_file in ["sample", "Sample", "SAMPLE", "s", "S", "", "'sample'"]:
		path_to_file = "data/sample_chat.txt"

	v.ts = [timer()]
	print("\n" + BOLD("Analyzing file"), f"@ '{GREEN(path_to_file)}'\n")

	try:
		file1 = open(check_file_format(path_to_file), "r", encoding="utf8")
		lines = file1.readlines()
		file1.close()
	except FileNotFoundError:  # file does not exist
		return off("File not found\nCheck the path to the file")
	except (UnicodeDecodeError, UnicodeError):  # file is not in UTF-8
		return off("File not in UTF-8 format\nTry uploading the original file")

	return lines


def get_path() -> str:
	"""
	Asks user in terminal for the filepath as input.
	"""
	path_to_file = input(
		BOLD("\nPlease enter the path to the chat file")
		+ "\nOnly .txt or .zip files are supported"
		+ "\nEnter 'sample' if you do not have a file at hand"
		+ "\nEnter the path here: "
	)
	return path_to_file


def check_file_format(path_to_file: str) -> str:
	"""
	Checks if the filetype is correct and returns correct path.
	"""
	if path_to_file.endswith(".txt"):
		return path_to_file
	elif path_to_file.endswith(".zip"):
		from zipfile import ZipFile

		with ZipFile(path_to_file, "r") as zip_ref:
			zip_ref.extractall("data")
		return "data/_chat.txt"
	else:
		return off("Wrong file type\nOnly .txt or .zip files are supported")
