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
senders =  list(chat["sender"].unique()) # get the list of senders
stats_df = pd.DataFrame(index=db.senders, columns=db.stats_df_columns)
db.senders = senders
db.stats_df = stats_df
# db.prepare()


### Only Testing: Initializing Variables for senders and dataframes ###
s0, s1 = str(), str()
s0_df, s1_df = pd.DataFrame(), pd.DataFrame()
s0_df_clean, s1_df_clean = pd.DataFrame(), pd.DataFrame()
#### Only Testing ####


# data seperation per sender a
for i, s in enumerate(senders):
	globals()[f"s{i}"] = s # sets a global variable for each sender
	df = chat.loc[chat["sender"] == s, "message"].rename(s) # dataframe with messages from sender s
	clean_df = cleanse_df(df) # get the stats for each sender
	get_stats(clean_df) # set the cleaned dataframe to the global variable
	# making dataframes for each sender globally accessible
	globals()[f"s{i}_df"] = df # sets a global variable for each dataframe
	globals()[f"s{i}_df_clean"] = clean_df



### Exporting for testing purposes ### save the dataframe to a csv file
chat.to_csv("data/testing/main/chat.csv", index=True)
s0_df.to_csv("data/testing/main/s0_df.csv", index=True)
s0_df_clean.to_csv("data/testing/main/s0_df_clean.csv", index=True)
s1_df.to_csv("data/testing/main/s1_df.csv", index=True)
s1_df_clean.to_csv("data/testing/main/s1_df_clean.csv", index=True)




for i, s in enumerate(senders):
	print_report(i)






print(f"\n\nAll Code took {timer() - start} seconds to run.")