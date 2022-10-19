# WhatsApp Reports <sub><sup><sub> README.md </sub></sup></sub> <div id="top"/>

> ### Summary  
> 1. [**Information**](#information) *about me and this project*  
>		1.1. [About me](#about-me)  
>		1.2. [About the project](#about-the-project)
> 2. [**HOW TO**](#how-to) *analyse a chat history with the program*  
>		2.1 [Export Chat](#export-chat)    
>		2.2 [Import and Process](#import-and-process)  
> 		2.3 [Get Results](#get-results)
> 3. [**Technologies**](#technologies) *used in this project*  
> 		3.1. [Programming Language](#programming-language)  
> 		3.2. [Libraries](#libraries)
> 4. [**Statistics**](#statistics) *derived from the program*  
>		4.1. [Number of Messages](#number-of-messages)  
>		4.2. [Number of User](#number-of-contacts)  
>		4.3. [Number of Groups](#number-of-groups)  
>		4.4. [Number of Chats](#number-of-chats)  
> 5. [**License**](#license) *of this project*  


<div id="information"/> <div id="about-me"/>
<br>

## Information <sub><sup> about me and about this project </sub></sup>

#### Hey 👋 Thank you for visiting my GitHub project!

My name is Yunus, I am studying Computational Linguistics at the Heinrich Heine University in Düsseldorf, Germany 👨‍💻. This is a project for my *Advanced Natural Langugae Processing* Class.

<div id="about-the-project"/>  

## 

You can use this program to analyse 🧐 your chats and get a report about the chat. It can derive statistics of both **private chats** 👤👤 (between two users) and **group chats** 👥👤👥 (with multiple users).  
🛑 None of your data will be saved in any kind, your machine will derive the statistics and discard your data afterwards. No one other than yourself, will see any of your personal information ℹ️ nor any of your messages. You can check for your self. 😉

---


<div id="how-to"/>
<div id="export-chat"/>

<div align="right">
    <b><a href="#top">⇧ back to top</a></b>
</div>

#### Before you start make sure you have Python 3 and all neccessary libraries (specifed in the [requirements.txt](requirements.txt) file) installed on your machine.


## How to <sub><sup> analyse a WhatsApp chat </sub></sup>  

First you need to export the chat from WhatsApp. Then you can import and process the chat. Finally, you will get the results.

### **1. Export from WhatsApp**:
> #### Export the chat from WhatsApp to a .txt or .zip file

To export a WhatsApp chat, go to the **information page** of that chat. You can export the chat, at the bottom of that page. WhatsApp will ask you, if you want to export the file with or without media. **Export without media files!**  

You will get a **.zip file**, which you have to save. After unziping that file, you will get the actual **.txt file**. It contains all messages of all users in that chat. You can use that file for analyzing, but if you want you can also directly upload the .zip file to the program.  

**🚨 IMPORTANT NOTE 🚨:** The program currently only works, if the chat is **exported from iOS** AND **without media files**. Preferably upload the **original file** (.txt or .zip).

##

<div id="import-and-process"/>

<div align="right">
    <b><a href="#top">⇧ back to top</a></b>
</div>

### 2. Import to the file and process it:
> #### Specify the filepath and let the program do it's thing

After you have exported the chat, you can import it into the program. You can either go main.py file and specify the **filepath of the .txt or .zip file** into the intented place (marked by a comment) or run the main.py file and enter the filepath when asked.

The program will then process the file and derive the statistics. This might take a few seconds, depending on the size of the file and your computer. 

While analyzing, the program will print out the steps it goes through and the time it took to process each step. After finalization, you will be nofitied and the program will terminate.

The terminal should look like this:

```
Plese enter the path to the chat file
Only .txt or .zip files are supported
Enter 'sample' if you dont have a file at hand
Enter the path here: sample

Analyzing file @ '.../WhatsAppReports/data/input/sample_chat.txt"'

converting the orinial file to a pandas DataFrame took 6.556389 sec
counting occurances and calculating contactwise statistics took 9.516935 sec
calculating remaining statistics for all senders took 0.787263 sec
visualising data for the final pdf report took 7.74283 sec
finishing final PDF Report took 6.080913 sec

✅ Success: Analysis finished ✅
Analyzing took 30.686177 seconds in total.
The PDF Report is located here: '.../WhatsAppReports/data/output/Report.pdf'
```

##

<div id="get-results"/>

<div align="right">
    <b><a href="#top">⇧ back to top</a></b>
</div>

### **3. Results**:
> #### Review and understand the results  

After completing the analysis, you will get a PDF report, which contains all the derived statistics in a reader friendly fromat. You can find the report in the **[output folder](data/output)**. The PDF will be named **Report.pdf**.

Text Text Text

---

<div id="technologies"/>
<div id="programming-language"/>

<div align="right">
    <b><a href="#top">⇧ back to top</a></b>
</div>

## Technologies <sub><sup> used for this project </sub></sup>  

### Programming Language: 
> #### This hole project is written in Python, but makes use of some Libraries you can find below. I worked with Anaconda, which is a distribution of the Python language for scientific computing.

<br>

**Python** is a general-purpose, high-level programming language. It is designed to make simple and easy to use, yet powerful and flexible. Python is used by a wide variety of programmers, and is especially popular for scientific computing. 


Verions used:  **Python 3.9.7** | ℹ️ [Python website](https://www.python.org/)  

<br>

**Anaconda** is a distribution of the Python and R languages for scientific computing. It includes a complete ecosystem of packages for data science, scientific computing, and software development. It is a free and open source software distribution. 


Verions used:  **Anaconda3 Navigator 2.2.0** | ℹ️ [Anaconda website](http://www.anaconda.com)  

##

<div id="libraries">

<div align="right">
    <b><a href="#top">⇧ back to top</a></b>
</div>

### 📚 Libraries:
> #### In this project I used various libraries for diffrent programming tasks. Here is a list of libraries that I used, with their websites and diffrent usages.

<br>

Libary | Website | Usage
:--- | :---: | ---:
[Numpy](https://numpy.org/) | https://numpy.org/ | for numerical calculations
[Pandas](https://pandas.pydata.org/) | https://pandas.pydata.org/ | for data analysis
[Matplotlib](https://matplotlib.org/) | https://matplotlib.org/ | for plotting
[(Seaborn)](https://seaborn.pydata.org/) | https://seaborn.pydata.org/ | for plotting
[Scikit-learn](https://scikit-learn.org/) | https://scikit-learn.org/ | for machine learning
[Nltk](https://www.nltk.org/) | https://www.nltk.org/ | for natural language processing
[Scipy](https://www.scipy.org/) | https://www.scipy.org/ | for numerical calculations
[Pytorch](https://pytorch.org/) | https://pytorch.org/ | for neural networks
[WordCloud](https://wordcloud.readthedocs.io/) | https://wordcloud.readthedocs.io/ | for word cloud generation



---

<div id="statistics"/>

<div align="right">
    <b><a href="#top">⇧ back to top</a></b>
</div>

## <sub><sup>What</sub></sup> Statistics <sub><sup>does the program derive?</sub></sup> 



<br>

This project is to help everyone with:
* Knowing which person has sent most messages
* Unique emojis used
* Most used emojis
* Time at which all the users are most actively chatting


