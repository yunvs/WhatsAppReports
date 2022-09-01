# from alive_progress import alive_bar

# with alive_bar(monitor=False, stats=False) as bar:
# bar.text = "Importing modules"

print("\n\nmain.py started\n")
from myfuncs import *

path = db.test_data[1]  # 0: small, 1: txt, 2: zip, 3: trash, 4: AB, 5: _chat.txt

# bar.text = "Importing and converting data"

# data extraction and preprocessing
convert_to_df(fileformat(path))  # convert the chat to a pandas dataframe
prepare_db()

seperate_data()

# bar.text = "Calculating statistics"
calc_sum_stats()  # get the summary statistics for all senders
calc_time_stats()  # get the time stats for the chat

# bar.text = "Creating plots and tables"
plot_data()
create_txt_reports()  # get general sender stats for the chat


# bar.text = "Creating and saving report @ data/output/pdfs/"
make_pdf_report()  # create the pdf report

export(database=True)

off(file_end=True)
