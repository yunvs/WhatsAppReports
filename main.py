import pandas as pd
from myfunctions import *
from textStyle import *
from timeit import default_timer as timer
start = timer() 

paths = ["data/chat_small.txt", "data/chat_mum.txt",
		"data/chat_mum.zip", "tash.trash", "data/chat_AB.txt"]
path_to_file = paths[0] # 0: small, 1: mum.txt, 2: mum.zip, 3: trash, 4: AB


contents = get_content(path_to_file) # get the content of the filepath
chat_df, sender_dict = convert_chat(contents) # convert the chat to a pd.dataframe
# (colums:date,time,sender,message) and a dictionary with the messages per sender

senders = list(sender_dict.keys()) # get a list of all senders
sender0, sender1 = str(), str() # initialize the senders
sender0_df, sender1_df = pd.DataFrame(), pd.DataFrame() # initialize the dataframes



for i, s in enumerate(senders):
	globals()[f"sender{i}"] = senders[i] # sets variables the diffrent senders
	globals()[f"sender{str(i)}_df"] = pd.DataFrame(sender_dict[s], columns = [s]) # create a dataframe for each sender



# # # Exporting for testing purposes
# chat_df.to_csv("data/testing/main/chat_df.csv", index=False) # save the dataframe to a csv file
# sender0_df.to_csv("data/testing/main/sender0_df.csv", index=False) # save the dataframe to a csv file
# sender1_df.to_csv("data/testing/main/sender1_df.csv", index=False) # save the dataframe to a csv file


# print()
# print(f"This chat is between {sender0} and {sender1}.")
# print(f"Overall there were {chat_df.shape[0]} messages send:")
# print(f"{sender0} sent {sender0_df.shape[0]} and {sender1} sent {sender1_df.shape[0]} messages.")
# print()


for i, s in enumerate(senders):
	messages_df, stats = cleanse_df(globals()[f"sender{i}_df"]) # get the stats for each sender
	msg_tot, msg_avg, msg_max, msg_min = get_stats(messages_df)

	print(f"""
	{GREEN(f'WA-Report for {BOLD(s)}')}:
	{s} sent {BOLD(f'{msg_tot} messages')} and {BOLD(f'{stats["media"]} media')} in this chat.
	The {BOLD('average length')} of {s} messages is {BOLD(f'{msg_avg} characters')}, 
	The {BOLD('longest message')} they sent contained {BOLD(f'{msg_max} characters')}.
	{s} sent {BOLD(f'{stats["audio"]} audios, {stats["image"]} images, {stats["video"]} videos, {stats["sticker"]} stickers')} and {BOLD(f'{stats["gif"]} GIFs')}.
	They shared {BOLD(f'{stats["contact"]} contacts, {stats["location"]} locations')} and {BOLD(f'{stats["document"]} documents')}.
	{s} changed their mind {BOLD(f'{stats["deleted"]} times')} and {STRIKE(f'deleted a message')}.""")
	if stats["missed"] > 0:
		print(f"""	{BOLD(f'{stats["missed"]} (video)calls')} by {s} were missed.""")





print(f"\n\nAll Code took {timer() - start} seconds to run.")