from utils import helper, getter, converter, analyzer, plotter, pdf_creater, texter

# get path to file and check if it is correct
path = getter.get_path(test=True) 

# data extraction and preprocessing
converter.convert_file(path)  # convert the file to a pandas DataFrame

# data analysis
analyzer.analyze_chat()

# data visualization
texter.create_texts() # create the text reports
plotter.plot_data() # data visualization

# final PDF creation
pdf_creater.make_pdf_report()  # create the pdf report

helper.off(file_end=True)