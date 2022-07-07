from timeit import default_timer as timer
from myfunctions import *
start = timer() 

#### Only Testing: Path ####
test_data = ["data/chat_small.txt", "data/chat_mum.txt", "data/chat_mum.zip", 
				"tash.trash", "data/chat_AB.txt", "data/_chat.txt"]
path = test_data[1] # 0: small, 1: txt, 2: zip, 3: trash, 4: AB, 5: _chat.txt
#### Only Testing ####


# data extraction and preprocessing
good_path = fileformat(path) # check if the file is in the correct format
chat_list = convert_to_list(good_path) # convert the chat file to a list
chat = convert_to_df(chat_list) # convert the list to a pandas dataframe
db.senders =  list(chat["sender"].unique()) # get the list of senders


### Only Testing: Initializing Variables for senders and dataframes ###
s0, s1 = str(), str() # initialize the senders
s0_df, s1_df = pd.DataFrame(), pd.DataFrame() # initialize the dataframes
#### Only Testing ####


# data seperation per sender
for i, s in enumerate(db.senders):
	globals()[f"s{i}"] = s # sets a global variable for each sender
	df = chat.loc[chat["sender"] == s, "message"] # dataframe with messages from sender s
	globals()[f"s{i}_df"] = df.rename(s) # sets a global variable for each dataframe


### Exporting for testing purposes ###
chat.to_csv("data/testing/main/chat.csv", index=True) # save the dataframe to a csv file
s0_df.to_csv("data/testing/main/s0_df.csv", index=True) # save the dataframe to a csv file
s1_df.to_csv("data/testing/main/s1_df.csv", index=True) # save the dataframe to a csv file
### Exporting for testing purposes ###




db.stats_df = pd.DataFrame(index=db.senders, columns=db.stats_df_columns)


for i, s in enumerate(db.senders):
	clean_df = cleanse_df(globals()[f"s{i}_df"]) # get the stats for each sender
	globals()[f"s{i}_clean_df"] = get_stats(clean_df) # set the cleaned dataframe to the global variable


	# print(f"""
	# {GREEN(f'WA-Report for {BOLD(s)}')}:
	# {s} sent {BOLD(f'{msg_tot} messages')} and {BOLD(f'{stats["med"]} media')} in this chat.
	# A average message is {BOLD(f'{msg_avg} characters')} long and contains {BOLD(f'{msg_avg_wrds} words')}. 
	# The {BOLD('longest message')} they sent contained {BOLD(f'{msg_max} characters and {msg_max_wrds} words')}.
	# {s} sent {BOLD(f'{stats["xaud"]} audios, {stats["ximg"]} images, {stats["xvid"]} videos, {stats["xstick"]} stickers')} and {BOLD(f'{stats["xgif"]} GIFs')}.
	# They shared {BOLD(f'{stats["xcont"]} contacts, {stats["xloc"]} locations, {stats["xdoc"]} files')} and {BOLD(f'{stats["rlink"]} URLs')}.
	# {s} changed their mind {BOLD(f'{stats["xdel"]} times')} and {STRIKE(f'deleted a message')}.""")
	# if stats["xmiss"] > 0:
	# 	print(f"""	You missed {BOLD(f'{stats["xmiss"]} (video)calls')} by {s}.""")






print(f"\n\nAll Code took {timer() - start} seconds to run.")