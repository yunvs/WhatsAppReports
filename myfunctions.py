import re, os, sys, zipfile
import pandas as pd


def get_content(path):
    """
    Gets file from given path, checks for desired fileformat and extracts the
    content of the file.
    """
    _name, extension = os.path.splitext(path)
    if extension != ".zip" and extension != ".txt": # check for fileformat
        sys.exit("ERROR: Sorry, only .txt or .zip files are supported")
    elif extension == ".zip": # extract the content of zip file
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall("data")
        path = "data/_chat.txt" 
    with open(path, "r", encoding="utf-16") as f: # read the content of the file
        contents = f.readlines()
    return contents


PATTERN = r"^\u200E? ?\[([\d./]*), ([\d:]*)\] ([\w ]*): (\u200E?.*)$"
def convert_chat(wa_listed):
    """
    Convert the chat history to a pandas DataFrame (with columns: date, time, 
    sender, message) and into a dictionary with the messages per sender.
    """
    chat = list() # list of all messages
    sender_messages = dict() # dictionary with key: sender, value: list of messages
    matched_before = False 

    for line in wa_listed:
        if re.match(PATTERN, line): # check if a new message starts in line
            res = re.search(PATTERN, line) # get groups of line
            # groups are: 1:date, 2:time, 3:sender, 4:message
            chat.append([res.group(1), res.group(2), res.group(3), res.group(4)])
            matched_before = True
            if res.group(3) not in sender_messages:
                sender_messages[res.group(3)] = [res.group(4)]
            else:
                sender_messages[res.group(3)].append(res.group(4))
        else:
            if not matched_before:
                sys.exit("ERROR: Sorry, the chat is not in the correct format")
            current_line = " " + line.strip("\n")
            chat[-1][3] += current_line
            sender_messages[chat[-1][2]][-1] += current_line
    chat_df = pd.DataFrame (chat, columns = ["date", "time", "sender", "message"])
    chat_df['date'] = pd.to_datetime(chat_df['date'], infer_datetime_format=True)
    return chat_df, sender_messages
