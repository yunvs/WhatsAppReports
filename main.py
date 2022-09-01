# from alive_progress import alive_bar

# with alive_bar(monitor=False, stats=False) as bar:
# bar.text = "Importing modules"

print("\n\nmain.py started")
from myfuncs import *

# Only Testing # Initializing Variables for autocomplete ###
s0, s1 = str(), str()
s0_df, s1_df = pd.DataFrame(), pd.DataFrame()
s0_df_clean, s1_df_clean = pd.DataFrame(), pd.DataFrame()
#### Only Testing ####


path = db.test_data[1]  # 0: small, 1: txt, 2: zip, 3: trash, 4: AB, 5: _chat.txt

# bar.text = "Importing and converting data"


# data extraction and preprocessing
convert_to_df(fileformat(path))  # convert the chat to a pandas dataframe
prep_db()


# data seperation, cleansing and data analysis per sender
for i, s in enumerate(db.senders):
	# bar.text = f"Cleaning and analyzing messages from {s}" #REMOVE
	df = db.chat.loc[db.chat["sender"] == s]  # dataframe with messages from sender
	db.chat_per_s.append(df)
	clean_df = cleanse_df(df["message"], s)  # get the stats for each sender
	calc_stats(clean_df) # calculate the stats for each sender
	# globals()[f"s{i}_df_clean"] = clean_df
	word_freq = calc_word_stats(clean_df, i)
	# globals()[f"s{i}_word_freq"] = word_freq

db.chat_per_s.append(db.chat_og)

# bar.text = "Calculating statistics"
calc_sum_stats()  # get the summary statistics for all senders
calc_time_stats()  # get the time stats for the chat

# bar.text = "Creating plots and tables"
make_plots()

create_txt_reports()  # get general sender stats for the chat


# bar.text = "Creating and saving report @ data/output/pdfs/"
make_pdf_report()  # create the pdf report

export(database=True)

off(file_end=True)
