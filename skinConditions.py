# https://youtu.be/OQydrlSzxnE
"""
https://arguswaikhom.medium.com/web-scraping-word-meaning-with-beautifulsoup-99308ead148a

install the following things
#for the application development
1. pip install streamlit
#for downloading images
2. pip install git+https://github.com/Joeclinton1/google-images-download.git
Please remember that this method has a limit of 100 images. 

3.#install pytrends
pip install pytrends

https://www.premiumleads.com/en/blog/seo/how-to-get-google-trends-data-with-pytrends-and-python/

"""

from functools import cache
import streamlit as st
from google_images_download import google_images_download
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
#import the libraries
import pandas as pd

st.set_page_config(layout="wide", initial_sidebar_state = "collapsed" )


from pytrends.request import TrendReq

cat = 420  
#, google trend category for skin conditions refer https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories

geo='US' #,  location to search for term

timeframe = '2021-07-30 2022-07-30'

kw_list = ['Diseases']

pytrends = TrendReq(hl='en-US')

#We indicate the query that we want to carry out
words_list = [""]
    
#We pass all the parameters we want to the request (filtered)
pytrends.build_payload(words_list, cat=420, timeframe="today 12-m", geo="US")
    
#We run pytrends.related_topics()
pytrends.related_topics()
    
#We indicate that we want the topics with an increasing volume
#during the established period of time
trend_analysis = pytrends.related_topics()
keywords= trend_analysis.get(words_list[0]).get("top")
df = pd.DataFrame(keywords)

st.write(df)




st.header("Welcome to the Skin condition search application")

st.markdown("This application provides the information about skin condition in common races in North America.")

cssStyleBlueButton = '''
    div.css-1kyxreq.etr89bj2{
            background-color: rgb(255, 255, 255);
            border:1px solid #0f0c0c;
            PADDING:30PX 30PX 30PX 30PX;
            border-radius: 10PX;
            }
    image:first-of-type{
            border: 1px solid #ddd;
            border-radius: 10px;
            padding:30PX 30PX 30PX 30PX;
            hieght: 150px;
            }
    img:hover {
            box-shadow: 0 0 2px 1px black;
            border-radius: 15px;

    }

    '''
st.markdown('<style>{}</style>'.format(cssStyleBlueButton), unsafe_allow_html=True)

pt = os.getcwd()


#instantiate the class
response = google_images_download.googleimagesdownload()

#Function to download images from google for different races
def downloadImage(skincondition,limit):
    keywords = []
    races = ["Native American", 'Asian','African American', 'Hispanic', "Caucasian"]


    for race in races:
        keywords.append(skincondition + ' in ' + race)
    keywords =', '.join(keywords)

    arguments = {"keywords":keywords,"limit":limit,"print_urls":False}
    paths = response.download(arguments)
    return paths




#Function to get general imformation about skin condition from WenbMD
def show_definitions(soup):
    print()
    #senseList = []
    titles = soup.find_all('p', class_='search-results-doc-title')
    descriptions = soup.find_all('p', class_='search-results-doc-description')

    #st.write(senses)
    definitions = {}
    for title,description in zip(titles[0:3],descriptions):
        definitions[title.text] = description.text
    
    return definitions



with st.form("my_form"):
    
    title = st.text_input('Enter the name of the skin condition e.g. vitilago,acne  ', '')
    count = st.slider('How many images do you want to see?', 2, 10, 2)
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted and title != "":

        
        #getting the information from WebMD
        word_to_search = title
        scrape_url = 'https://www.webmd.com/search/search_results/default.aspx?query=' + title

        st.write(f'''For detailed below information, check out this link [WebMD]({scrape_url})''')
        
        headers = {"User-Agent": ""}
        web_response = requests.get(scrape_url, headers=headers)

        if web_response.status_code == 200:
            soup = BeautifulSoup(web_response.text, 'html.parser')
            try:
                definitions = show_definitions(soup)
                for key,value in definitions.items():
                    key,value = '**' + key.strip() + '**',   value.strip() 
                    
                    st.markdown( rf'''{key} : {value}''')
            except AttributeError:
                print('Condition not found in WebMD!!')

        
        else:
            print('Failed to get response...')







        #getting pictures from the internet    
        paths = downloadImage(title.capitalize(),count)

        acnecontainer = st.container()

        picturesDictionary = {}

        for searchterm,paths in paths[0].items():
            picturesDictionary[searchterm] = []
            for path in paths:
                path = path.replace(pt,"")
                path = '.'+ path.replace("\\", "/")
                picturesDictionary[searchterm].append(path)

        columnCount = len(picturesDictionary)
                    
        with acnecontainer:
            cols = acnecontainer.columns([1,3,1])

    

        for key,value in picturesDictionary.items():
            cols[1].markdown(rf'''# {key} ''')
            cols[1].image(value,width=200)
            st.write(" ")
            st.write(" ")
