from timeit import default_timer as timer
from myfunctions import *
start = timer() 

#### Only Testing: Path ####
y = 1
test_data = ["data/chat_small.txt", "data/chat_mum.txt", "data/chat_mum.zip", 
				"tash.trash", "data/chat_AB.txt", "data/_chat.txt"]
path = test_data[y] # 0: small, 1: txt, 2: zip, 3: trash, 4: AB, 5: _chat.txt
#### Only Testing ####


# data extraction and preprocessing
good_path = fileformat(path) # check if the file is in the correct format
chat_list = convert_to_list(good_path) # convert the chat file to a list
db.chat = convert_to_df(chat_list) # convert the list to a pandas dataframe
db.senders =  list(db.chat["sender"].unique()) # get the list of senders
db.stats_df = pd.DataFrame(index=db.senders, columns=db.stats_df_columns)


### Only Testing: Initializing Variables for senders and dataframes ###
s0, s1 = str(), str()
s0_df, s1_df = pd.DataFrame(), pd.DataFrame()
s0_df_clean, s1_df_clean = pd.DataFrame(), pd.DataFrame()
s0_df_report, s1_df_report = str(), str()

#### Only Testing ####


# data seperation and data analysis per sender
for i, s in enumerate(db.senders):
	globals()[f"s{i}"] = s # sets a global variable for each sender
	df = db.chat.loc[db.chat["sender"] == s, "message"] # dataframe with messages from sender s
	clean_df = cleanse_df(df.rename(s)) # get the stats for each sender
	get_stats(clean_df) # set the cleaned dataframe to the global variable
	report = get_sender_report(i)
	globals()[f"s{i}_df"] = df # sets a global variable for each dataframe
	globals()[f"s{i}_df_clean"] = clean_df
	globals()[f"s{i}_report"] = report

get_sum_stats() # get the general stats for the chat


### Exporting for testing purposes ### save the dataframe to a csv file
db.chat.to_csv("data/testing/main/chat.csv", index=True)
db.stats_df.to_csv("data/testing/main/stats_df.csv", index=True)
# s0_df.to_csv("data/testing/main/s0_df.csv", index=True)
# s0_df_clean.to_csv("data/testing/main/s0_df_clean.csv", index=True)
# s1_df.to_csv("data/testing/main/s1_df.csv", index=True)
# s1_df_clean.to_csv("data/testing/main/s1_df_clean.csv", index=True)


print(f"\n\nAll Code took {timer() - start} seconds to run.")