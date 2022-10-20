from utils.helper import *

def get_path(path_to_file: str = "") -> str:
	"""
	Asks the user for the path to the file and checks if it is correct.
	"""
	if path_to_file == "":
		path_to_file = input(
			BOLD("\nPlease enter the path to the chat file")
			+ "\nOnly .txt or .zip files are supported"
			+ "\nEnter 'sample' if you dont have a file at hand"
			+ "\nEnter the path here: ")
	
	if path_to_file == "sample":
		path_to_file = "data/sample_chat.txt"

	v.ts = [timer()]
	print("\n" + BOLD("Analyzing file"), f"@ '{GREEN(path_to_file)}'\n")
	
	return check_file_format(path_to_file)

def check_file_format(path_to_file: str) -> str:
	"""
	Checks if the format of the file is correct and returns correct path.
	"""
	if path_to_file.endswith(".txt"):
		return path_to_file
	elif path_to_file.endswith(".zip"):
		from zipfile import ZipFile
		with ZipFile(path_to_file, "r") as zip_ref:
			zip_ref.extractall("data")
		return "data/_chat.txt"
	else:
		return off("Only .txt or .zip files are supported")