from utils import analyzer, converter, getter, helper, outputter, plotter

# get path to file and check if it is correct
lines = getter.get_file(
	"")  # <-- specify path here or in the terminal when running the script

# data extraction and preprocessing
converter.convert_lines(lines)  # convert the file to a pandas DataFrame

# data analysis
analyzer.analyze_chat()  # analyze the chat and create the stats DataFrame

# data visualization
plotter.plot_data()  # data visualization and plotting

# textual outputs and final PDF creation
outputter.make_pdf_report()  # create txt reports and the pdf report

# program has finished successfully
helper.off(error=False)  # print out success message and analyzing time

# helper.export_database() # <-- uncomment this line to export all derived data
