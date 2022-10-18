from utils.helper import * 
from utils import getter, converter, analyzer, outputer, plotter, pdf_creater

path = getter.get_path(test=True)

# data extraction and preprocessing
converter.convert_path(path)  # convert the chat to a pandas DataFrame

analyzer.prepare_database()
analyzer.analysis_per_sender() # data analysis

analyzer.calc_remaining_stats()  # get the summary statistics for all senders

outputer.create_tetual_reports() # create the text reports
plotter.plot_data() # data visualization

pdf_creater.make_pdf_report()  # create the pdf report

off(file_end=True)