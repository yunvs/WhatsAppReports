from timeit import default_timer as timer
from myfuncs import *
start = timer()

# Only Testing # Initializing Variables for autocomplete ###
s0, s1 = str(), str()
s0_df, s1_df = pd.DataFrame(), pd.DataFrame()
s0_df_clean, s1_df_clean = pd.DataFrame(), pd.DataFrame()
#### Only Testing ####


path = db.test_data[1]  # 0: small, 1: txt, 2: zip, 3: trash, 4: AB, 5: _chat.txt


# data extraction and preprocessing
good_path = fileformat(path)  # check if the file is in the correct format
db.chat = convert_to_df(good_path)  # convert the chat to a pandas dataframe
db.senders = list(db.chat["sender"].unique())  # get the list of senders
db.cstats_df = pd.DataFrame(index=db.senders, columns=db.stats_dict.keys())

# cleaned_df = cleanse_df(db.chat) # cleanse the dataframe

# data seperation and data analysis per sender
for i, s in enumerate(db.senders):
    # globals()[f"s{i}"] = s  # sets a global variable for each sender
    df = db.chat.loc[db.chat["sender"] == s, "message", ]  # dataframe with messages from sender
    # globals()[f"s{i}_df"] = df  # sets a global variable for each dataframe
    clean_df = cleanse_df(df, s)  # get the stats for each sender
    calc_stats(clean_df)  # set the cleaned dataframe to the global variable
    # globals()[f"s{i}_df_clean"] = clean_df
    word_freq = calc_word_stats(clean_df)
    # globals()[f"s{i}_word_freq"] = word_freq


get_sum_stats()  # get the summary statistics for all senders


create_pdf_report()  # create the pdf report

db_export()


print(f"\n\nAll Code took {timer() - start} seconds to run.")
