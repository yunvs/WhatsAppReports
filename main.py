from timeit import default_timer as timer
from myfunctions import *
start = timer()

# Only Testing # Initializing Variables for autocomplete ###
s0, s1 = str(), str()
s0_df, s1_df = pd.DataFrame(), pd.DataFrame()
s0_df_clean, s1_df_clean = pd.DataFrame(), pd.DataFrame()
#### Only Testing ####


y = 1
path = db.test_data[y]  # 0: small, 1: txt, 2: zip, 3: trash, 4: AB, 5: _chat.txt


# data extraction and preprocessing
good_path = fileformat(path)  # check if the file is in the correct format
db.chat = convert_to_df(good_path)  # convert the chat to a pandas dataframe
db.senders = list(db.chat["sender"].unique())  # get the list of senders
db.stats_df = pd.DataFrame(index=db.senders, columns=db.stats_df_columns)


# data seperation and data analysis per sender
for i, s in enumerate(db.senders):
    # dataframe with messages from sender s
    df = db.chat.loc[db.chat["sender"] == s, "message"]
    clean_df = cleanse_df(df, s)  # get the stats for each sender
    get_stats(clean_df)  # set the cleaned dataframe to the global variable
    globals()[f"s{i}"] = s  # sets a global variable for each sender
    globals()[f"s{i}_df"] = df  # sets a global variable for each dataframe
    globals()[f"s{i}_df_clean"] = clean_df

get_sum_stats()  # get the summary statistics for all senders
reports = get_reports()  # get general ander sender stats for the chat
print("\n".join(reports))


# Export dataframes to csv files
# export("main", db.chat, db.stats_df, s0_df, s1_df, s0_df_clean, s1_df_clean)


print(f"\n\nAll Code took {timer() - start} seconds to run.")
