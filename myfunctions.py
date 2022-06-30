import re, os, sys, zipfile
import pandas as pd

PATTERN = r"^\u200E?\[(\d{1,2}.\d{1,2}.\d{2}), (\d{2}:\d{2}:\d{2})\] \u200E?(\b[\w ]*\b): (.*)$"


def get_content(path):
    """
    Gets file from given path, checks for desired fileformat and extracts the
    content of the file.
    """
    _name, extension = os.path.splitext(path)
    if extension != ".zip" and extension != ".txt":
        sys.exit("ERROR: Sorry, only .txt or .zip files are supported")
    elif extension == ".zip":
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall("data")
        path = "data/_chat.txt"
    with open(path, 'r', errors='ignore') as f:
        contents = f.readlines()
    return contents


def check_for_pattern(string):
    """
    Check if a string matches the pattern and is a the beginning of a new 
    message: Starts with [mm/dd/yy, hh:mm:ss]
    """
    return re.match(PATTERN, string) is not None


def get_groups(string):
    """
    Get the groups of a string.
    Groups are: 1:Date, 2:Time, 3:Sender, 4:Message
    """
    return re.search(PATTERN, string)


def chats_to_list(string):
    """
    Convert a chat history to a list of messages:
    In each message, the first element is a list of the date and time, 
    the second element is the sender, and the third element is the message.
    [[[Date, Time], Sender, Message], [[Date, Time], Sender, Message], … ]
    """
    chat_history = list() # list of all messages
    msg_count = 0 # total number of messages

    for line in string:
        if check_for_pattern(line):
            res = get_groups(line)
            chat_history.append([[res.group(1), res.group(2)], res.group(3), res.group(4)])
            msg_count += 1
        else:
            current_line = "\n" + line.strip("\n")
            chat_history[msg_count-1][2] += current_line
    return chat_history


def chats_per_sender(all_chats):
    """
    Divide the chat history into a list of lists, where each list contains all
    messages from one sender.
    """
    sender_texts = list()
    sender_dict = dict()
    for msg in all_chats:
        if msg[1] not in sender_dict:
            sender_dict[msg[1]] = len(sender_dict)
            sender_texts.append([msg[1]])
        sender_texts[sender_dict[msg[1]]].append(msg[2])
    return sender_texts
