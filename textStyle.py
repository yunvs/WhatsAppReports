# this file contains functions which change the output style and colour of strings

def NORM(text):
	"""
	Resets all the style and color settings
	"""
	return "\033[0m" + text

def BOLD(text):
	"""
	Returns text bold
	"""
	return "\033[1m" + text + "\033[22m"


def DIM(text):
	"""
	Returns text dimmed
	"""
	return "\033[2m" + text + "\033[22m"


def ITAL(text):
	"""
	Returns text italic
	"""
	return "\033[3m" + text + "\033[23m"


def UNDL(text):
	"""
	Returns text underlined
	"""
	return "\033[4m" + text + "\033[24m"


def BLINK(text):
	"""
	Returns text blinking
	"""
	return "\033[5m" + text + "\033[25m"


def STRIKE(text):
	"""
	Returns text striked
	"""
	return "\033[9m" + text + "\033[29m"


def RED(text):
	"""
	Returns text in red
	"""
	return "\033[31m" + text + "\033[39m"


def GREEN(text):
	"""
	Returns text in green
	"""
	return "\033[32m" + text + "\033[39m"


def YELLOW(text):
	"""
	Returns text in yellow
	"""
	return "\033[33m" + text + "\033[39m"


def BLUE(text):
	"""
	Returns text in blue
	"""
	return "\033[34m" + text + "\033[39m"
	