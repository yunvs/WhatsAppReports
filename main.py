print("\n\nmain.py started\n")
from myfuncs import *

path = db.TEST_DATA[5]  # 0: small, 1: txt, 2: zip, 3: trash, 4: AB, 5: _chat.txt

# data extraction and preprocessing
convert_file_to_df(path)  # convert the chat to a pandas DataFrame

analysis_per_sender() # data analysis

calc_remaining_stats()  # get the summary statistics for all senders

visualise_data() # data visualization

make_pdf_report()  # create the pdf report
off(file_end=True)
