# from alive_progress import alive_bar #TODO add bar

# with alive_bar(monitor=False, stats=False) as bar: #TODO add bar
# bar.text = "Importing modules" #TODO add bar

print("\n\nmain.py started\n")
from myfuncs import *

path = db.test_data[5]  # 0: small, 1: txt, 2: zip, 3: trash, 4: AB, 5: _chat.txt

# bar.text = "Importing and converting data" #TODO add bar

# data extraction and preprocessing
convert_file_to_df(path)  # convert the chat to a pandas DataFrame

seperate_data()

# bar.text = "Calculating statistics" #TODO add bar
calc_sum_stats()  # get the summary statistics for all senders
calc_time_stats()  # get the time stats for the chat

# bar.text = "Creating plots and tables" #TODO add bar
plot_data()
create_txt_reports()  # get general sender stats for the chat


# bar.text = "Creating and saving report @ data/output/pdfs/" #TODO add bar
make_pdf_report()  # create the pdf report


off(file_end=True)
