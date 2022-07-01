from myfunctions import *
import pandas as pd
from timeit import default_timer as timer
start = timer()

paths = ["data/chat_small.txt", "data/chat_mum.txt", 
        "data/chat_mum.zip", "tash.trash", "data/chat_AB.txt"]
path_to_file = paths[2] # 0: small, 1: mum.zip, 2: mum.txt, 3: trash, 4: AB

contents = get_content(path_to_file) # get the content of the filepath
chat_df, sender_dict = convert_chat(contents) # convert the chat to a pd.dataframe 
# (colums:date,time,sender,message) and a dictionary with the messages per sender
print(chat_df.head(10))
senders = list(sender_dict.keys()) # get all sender
sender_count = len(senders)
print(f"There are {sender_count} different senders in the chat. Which are:")
for sender in senders: print(sender)

print(f"\n\nAll Code took {timer() - start} seconds to run.") 