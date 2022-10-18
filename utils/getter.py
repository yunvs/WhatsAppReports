from utils.helper import *

def get_path(test: bool = False) -> str:
	if not test:
		path = input(BOLD("\nEnter path to file: "))
	else:
		path = "data/input/test_chat.txt"
		path = "/Users/yunusrenz/Others/chat_mum.zip" #TODO: remove

	v.ts = [timer()]
	print(BOLD("Analyzing file"), "@", path, "\n")
	return path