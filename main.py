from myfunctions import *
import pandas as pd
from timeit import default_timer as timer
start = timer()

paths = ["data/chat_small.txt", "data/chat_mum.txt", 
        "data/chat_mum.zip", "tash.trash", "data/chat_AB.txt"]
path_to_file = paths[1] # 0: small, 1: mum.txt, 2: mum.zip, 3: trash, 4: AB


contents = get_content(path_to_file) # get the content of the filepath
chat_df, sender_dict = convert_chat(contents) # convert the chat to a pd.dataframe 
# (colums:date,time,sender,message) and a dictionary with the messages per sender


sender0 = list(sender_dict.keys())[0]
sender1 = list(sender_dict.keys())[1]
sender0_df = pd.DataFrame(sender_dict[sender0], columns = ["message"])
sender1_df = pd.DataFrame(sender_dict[sender1], columns = ["message"])

""" # Use if there are more than two senders in the chat
for i, s in enumerate(sender_dict):
    globals()[f"sender{i}"] = list(sender_dict.keys())[i]
    global()[f"sender{str(i)}_df"] = pd.DataFrame(sender_dict[s], columns = ["message"])
"""


# Exporting for testing purposes
chat_df.to_csv("data/chat_df.csv", index=False) # save the dataframe to a csv file
sender0_df.to_csv("data/sender0_df.csv", index=False) # save the dataframe to a csv file
sender1_df.to_csv("data/sender1_df.csv", index=False) # save the dataframe to a csv file


print()
print(f"This chat was between {sender0} and {sender1}.")
print(f"Overall there were {chat_df.shape[0]} messages sent")
print(f"{sender0} sent {sender0_df.shape[0]} messages.")
print(f"{sender1} sent {sender1_df.shape[0]} messages.")







print(f"\n\nAll Code took {timer() - start} seconds to run.") 