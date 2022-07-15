# this file contains functions which change the style and colour of the output

def print_with_spaces(*args) -> str:
	"""
	Returns given arguments with spaces inbetween them
	"""
	s = str()
	for i, arg in enumerate(args):
		s += str(arg) + " " if len(args) > i+1 else str(arg)
	return s


def NORM(*args) -> str:
	"""
	Resets all the style and color settings
	"""
	return "\033[0m" + print_with_spaces(*args)


def BOLD(*args) -> str:
	"""
	Returns given arguments seperated by spaces and bold 
	"""
	return "\033[1m" + print_with_spaces(*args) + "\033[22m"


def DIM(*args) -> str:
	"""
	Returns given arguments seperated by spaces and dimmed 
	"""
	return "\033[2m" + print_with_spaces(*args) + "\033[22m"


def ITAL(*args) -> str:
	"""
	Returns given arguments seperated by spaces and italic 
	"""
	return "\033[3m" + print_with_spaces(*args) + "\033[23m"


def UNDL(*args) -> str:
	"""
	Returns given arguments seperated by spaces and underlined 
	"""
	return "\033[4m" + print_with_spaces(*args) + "\033[24m"


def STRIKE(*args) -> str:
	"""
	Returns given arguments seperated by spaces and striked 
	"""
	return "\033[9m" + print_with_spaces(*args) + "\033[29m"


def RED(*args) -> str:
	"""
	Returns given arguments seperated by spaces and in red 
	"""
	return "\033[31m" + print_with_spaces(*args) + "\033[39m"


def GREEN(*args) -> str:
	"""
	Returns given arguments seperated by spaces and in green 
	"""
	return "\033[32m" + print_with_spaces(*args) + "\033[39m"


def YELLOW(*args) -> str:
	"""
	Returns given arguments seperated by spaces and in yellow 
	"""
	return "\033[33m" + print_with_spaces(*args) + "\033[39m"


def BLUE(*args) -> str:
	"""
	Returns given arguments seperated by spaces and in blue 
	"""
	return "\033[34m" + print_with_spaces(*args) + "\033[39m"