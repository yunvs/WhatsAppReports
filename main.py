from utils import getter, converter, analyzer, plotter, texter, helper

# get path to file and check if it is correct
path = getter.get_path("") # you can specify the path here if you want

# data extraction and preprocessing
converter.convert_file(path)  # convert the file to a pandas DataFrame

# data analysis
analyzer.analyze_chat() # analyze the chat and create the stats DataFrame

# data visualization
plotter.plot_data() # data visualization and plotting

# textual outputs and final PDF creation
texter.make_pdf_report()  # create txt reports and the pdf report

helper.off(error=False) # program is ending because it finished successfully