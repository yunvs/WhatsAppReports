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

senders = list(sender_dict.keys()) # get a list of all senders
sender0, sender1 = str(), str() # initialize the senders
sender0_df, sender1_df = pd.DataFrame(), pd.DataFrame() # initialize the dataframes


# Use if there are more than two senders in the chat
for i, s in enumerate(sender_dict):
	globals()[f"sender{i}"] = senders[i] 
	globals()[f"sender{str(i)}_df"] = pd.DataFrame(sender_dict[s], columns = [str(s)]) # create a dataframe for each sender



# Exporting for testing purposes
chat_df.to_csv("data/chat_df.csv", index=False) # save the dataframe to a csv file
sender0_df.to_csv("data/sender0_df.csv", index=False) # save the dataframe to a csv file
sender1_df.to_csv("data/sender1_df.csv", index=False) # save the dataframe to a csv file


# print()
# print(f"This chat is between {sender0} and {sender1}.")
# print(f"Overall there were {chat_df.shape[0]} messages send:")
# print(f"{sender0} sent {sender0_df.shape[0]} and {sender1} sent {sender1_df.shape[0]} messages.")
# print()


for i, s in enumerate(senders):
	messages_df, stats = cleanse_df(globals()[f"sender{i}_df"]) # get the stats for each sender
	msg_tot, msg_avg, msg_max, msg_min = get_stats(messages_df)


	print(f"""
		This is the WA-Report for {s}:
		{s} sent a total amound of {msg_tot} messages.
		The average length of a message is {msg_avg} characters, the longest message contained {msg_max} characters.
		{s} sent {stats["audio"]} audio messages, {stats["image"]} images, {stats["video"]} videos and {stats["sticker"]} stickers.
		{s} shared {stats["contact"]} contact cards, {"##"} locations and {"##"} documents.
		{s} changed their mind {"##"} times and deleted a message.
			""")





print(f"\n\nAll Code took {timer() - start} seconds to run.")