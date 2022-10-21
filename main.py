from utils import analyzer, converter, getter, helper, texter, visualizer

# get path to file and check if it is correct
lines = getter.get_file("")  # specify path here or in the terminal

# data extraction and preprocessing
converter.convert_lines(lines)  # convert the file to a pandas DataFrame

# data analysis
analyzer.analyze_chat()  # analyze the chat and create the stats DataFrame

# data visualization
visualizer.plot_data()  # data visualization and plotting

# textual outputs and final PDF creation
texter.make_pdf_report()  # create txt reports and the pdf report

# program has finished successfully
helper.off(error=False)  # print out success message and analyzing time

# helper.export_database() # uncomment to export all derived statistics