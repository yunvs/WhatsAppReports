# this file contains functions which change the output style and colour of strings

def NORM(*args) -> str:
	"""
	Resets all the style and color settings
	"""
	s = str()
	for i, arg in enumerate(args):
		s += str(arg)
		if len(args) > i+1:
			s += " "
	return "\033[0m" + s


def BOLD(*args) -> str:
	"""
	Returns given arguments bold and with spaces between them
	"""
	s = str()
	for i, arg in enumerate(args):
		s += str(arg)
		if len(args) != i+1:
			s += " "
	return "\033[1m" + s + "\033[22m"


def DIM(*args) -> str:
	"""
	Returns given arguments dimmed and with spaces between them
	"""
	s = str()
	for i, arg in enumerate(args):
		s += str(arg)
		if len(args) > i+1:
			s += " "
	return "\033[2m" + s + "\033[22m"


def ITAL(*args) -> str:
	"""
	Returns given arguments italic and with spaces between them
	"""
	s = str()
	for i, arg in enumerate(args):
		s += str(arg)
		if len(args) > i+1:
			s += " "
	return "\033[3m" + s + "\033[23m"


def UNDL(*args) -> str:
	"""
	Returns given arguments underlined and with spaces between them
	"""
	s = str()
	for i, arg in enumerate(args):
		s += str(arg)
		if len(args) > i+1:
			s += " "
	return "\033[4m" + s + "\033[24m"


def STRIKE(*args) -> str:
	"""
	Returns given arguments striked and with spaces between them
	"""
	s = str()
	for i, arg in enumerate(args):
		s += str(arg)
		if len(args) > i+1:
			s += " "
	return "\033[9m" + s + "\033[29m"


def RED(*args) -> str:
	"""
	Returns given arguments in red and with spaces between them
	"""
	s = str()
	for i, arg in enumerate(args):
		s += str(arg)
		if len(args) > i+1:
			s += " "
	return "\033[31m" + s + "\033[39m"


def GREEN(*args) -> str:
	"""
	Returns given arguments in green and with spaces between them
	"""
	s = str()
	for i, arg in enumerate(args):
		s += str(arg)
		if len(args) > i+1:
			s += " "
	return "\033[32m" + s + "\033[39m"


def YELLOW(*args) -> str:
	"""
	Returns given arguments in yellow and with spaces between them
	"""
	s = str()
	for i, arg in enumerate(args):
		s += str(arg)
		if len(args) > i+1:
			s += " "
	return "\033[33m" + s + "\033[39m"


def BLUE(*args) -> str:
	"""
	Returns given arguments in blue and with spaces between them
	"""
	s = str()
	for i, arg in enumerate(args):
		s += str(arg)
		if len(args) > i+1:
			s += " "
	return "\033[34m" + s + "\033[39m"