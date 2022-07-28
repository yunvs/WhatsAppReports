from myfuncs import *

print(BLUE("starting code"))

# Only Testing # Initializing Variables for autocomplete ###
s0, s1 = str(), str()
s0_df, s1_df = pd.DataFrame(), pd.DataFrame()
s0_df_clean, s1_df_clean = pd.DataFrame(), pd.DataFrame()
#### Only Testing ####


path = db.test_data[1]  # 0: small, 1: txt, 2: zip, 3: trash, 4: AB, 5: _chat.txt


# data extraction and preprocessing
convert_to_df(fileformat(path))  # convert the chat to a pandas dataframe
db.stats_df = pd.DataFrame(index=db.senders, columns=db.stats_dict.keys())


# data seperation, cleansing and data analysis per sender
for i, s in enumerate(db.senders):
    # globals()[f"s{i}"] = s
    df = db.chat.loc[db.chat["sender"] == s, "message", ]  # dataframe with messages from sender
    # globals()[f"s{i}_df"] = df
    clean_df = cleanse_df(df, s)  # get the stats for each sender
    calc_stats(clean_df)  # set the cleaned dataframe to the global variable
    # globals()[f"s{i}_df_clean"] = clean_df
    word_freq = calc_word_stats(clean_df)
    # globals()[f"s{i}_word_freq"] = word_freq


calc_sum_stats()  # get the summary statistics for all senders

make_plots()

db.reports = get_txt_reports()  # get general sender stats for the chat

make_pdf_report()  # create the pdf report

export(database=True)

time("end")