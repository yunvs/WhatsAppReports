from timeit import default_timer as timer
from myfuncs import *
t = [timer()]

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

t.append(timer())
print(GREEN(f"\n extraction and preprocessing took {t[-1] - t[-2]} seconds"))

# data seperation, cleansing and data analysis per sender
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

t.append(timer())
print(GREEN(f"\n data seperation, cleansing and data analysis took {t[-1] - t[-2]} seconds"))


create_pdf_report()  # create the pdf report
t.append(timer())
print(GREEN(f"\n PDF creation took {t[-1] - t[-2]} seconds"))


db_export()
t.append(timer())
print(GREEN(f"\n final exporting took {t[-1] - t[-2]} seconds"))


print(f"\n\nAll Code took {timer() - t[0]} seconds to run.")
