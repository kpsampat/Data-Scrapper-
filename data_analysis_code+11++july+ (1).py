
# coding: utf-8

# # Step 1 . Importing Library 

# In[4]:


import urllib.request                                                                         #library imported
import urllib
import urllib.parse
import urllib.request as urllib2 
from urllib.request import Request, urlopen
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
#from wordcloud import WordCloud, STOPWORDS
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import string
from nltk.corpus import stopwords
from pathlib import Path
import re 
import csv
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup


# # Step 2 . Fetching url's from KeyWord :

# In[10]:


store_links = []
new_text_1 = []
iter_item = 0
search_item = input("Enter_Search_Item : ")
while len(new_text_1)<100:
    
    url_encode = urllib.parse.quote(search_item, safe='/', encoding=None, errors=None)
    #print(url_encode)
    url_search = str("https://www.google.co.in/search?q="+url_encode+"&start="+str(iter_item))
    req = Request(url_search , headers={'User-Agent': 'Mozilla/54.0'})
    webpage = urlopen(req).read()
    url_1 = str(webpage)
    soup = BeautifulSoup(url_1,"lxml")
    redditAll = soup.find_all("a")
    redditAll = soup.get_text("a")
    for links in soup.find_all('a'):
        store_links.append(links.get('href'))
    #for lnks in store_links:
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',str(store_links))
    #urls = getURLs(str(store_links))
    #print(type(urls))
    #new_text_1 = []
    for shit in urls:
        list_1 = re.sub(r'&sa=*',"",shit)
        list_1 = shit[:-2]
        if not shit.startswith("https://maps.")|shit.startswith("https://play.")| shit.startswith("https://drive.")|shit.startswith("https://www.youtube.")|shit.startswith("https://mail.")|shit.startswith("https://photos.")|shit.startswith("https://www.google.")|shit.startswith("https://translate.")|shit.startswith("http://www.google.")|shit.startswith("https://accounts.")|shit.startswith("https://docs")|shit.startswith("https://news.")|shit.startswith("https://www.blogger.")|shit.startswith("http://webcache."):
            new_text_1.append(list_1)
    print(new_text_1)
    #print(type(new_text_1))
    print(len(new_text_1))
    with open("data_analysis_link.txt", 'w') as textfile:
        for new_link in new_text_1:
            textfile.write(new_link + "\n")
    iter_item = iter_item + 10
textfile.close()


# # Step 3 . Grabing all links and processing them

# In[11]:


links = []
with open("data_analysis_link.txt","r") as f:
    data = f.readlines() 
    for link_in_file in data:
        data1 = links.append(link_in_file.split())


# # Step 4 . Fetching HTML Data from URL

# In[ ]:


url = data1
url = input("Enter a website to extract the URL's from: ") #raw input from the user
f = urllib.request.urlopen(url) #opening the raw input by establishing socket connection with url
html = str(f.read())
print("HTML TEXT =====>>>>>>> " + html)


# # Step 5 . Cleaning the particular HTML data and converting into text

# In[16]:


#url = input("Enter a website to extract the URL's from: ") #raw input from the user
html = urllib.request.urlopen(url) 
soup = BeautifulSoup(html,"lxml")
# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out
# get text
text = soup.get_text()
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines()) 
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
new_text = '\n'.join(chunk for chunk in chunks if chunk)
print("New Text ===>>>> " + new_text)


# # Step 6 . Stop words Removal 

# In[18]:


stop_words = set(stopwords.words("english"))  # load stopwords
example_sent = (new_text).lower()
example_words = word_tokenize(example_sent)
example_words = filter(lambda x: x not in string.punctuation, example_words)
cleaned_text = list(filter(lambda x: x not in stop_words, example_words))
print(cleaned_text)


# # Step 7 . Converting the string data into normal text

# In[19]:


new_text = ""
for shit in cleaned_text:
    new_text += (' ' + shit)
print("new_text ============>>> " + new_text)


# # Step 8 . Removing of stem words from text

# In[20]:


from nltk import PorterStemmer
ps = PorterStemmer()                                     #stemmer library   #stemwords taken automatically
example_sents = (new_text)
example_word = word_tokenize(example_sents)
new = list(filter(lambda x: ps.stem(x), example_word))
print(new)


# # Step 9 . Converting String to text

# In[21]:


new_final = ""
for shit in new:
    new_final += (' ' + shit)
#print("new_text ============>>> " + new_final)
text_stri = new_final.lower()
match_new = re.findall(r'\b[a-z]{3,20}\b', text_stri)
new_final_done = ""
for shit in match_new:
    new_final_done += (' ' + shit)
print("new_text_done ============>>> " + new_final_done)


# # Step 10 . Removal of unwanted words 

# In[22]:


text = (new_final_done)
dicr = {"also":"","–":"","’":"","‘":"","''":"","``":"","well":""}
def repl_unwanted(text,dicr):
    for i,j in dicr.items():
        text = text.replace(i,j)
    return text
cleaned = repl_unwanted(text,dicr)   
print("Cleaned Text ========>>>>>>" + cleaned)


# # Step 11 . Calculating Frequency and writing into a file (data_analysis.csv)

# In[23]:


frequency = []
text_string = cleaned.lower()
match_pattern = re.findall(r'\b[a-z]{3,20}\b', text_string)
#print((match_pattern))
wordfreq = []
for w in match_pattern:
    wordfreq.append(match_pattern.count(w))

a_list_mixed = []
for i in range( len(wordfreq)):
    x = match_pattern[i]
    y = wordfreq[i]
    z=[x,y]
    
    if z not in a_list_mixed:
        a_list_mixed.append(z)

    
        
with open('data_analysis.csv', 'w') as csvfile:
    writer = csv.writer(csvfile,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerow(['words', 'word_frequency'])
    for item in a_list_mixed:
        writer.writerow([item[0], item[1]])
        print(item[0], item[1])


# # Step 12 . adding frequency in file as word and key 

# In[24]:


import re
import string
import csv
from pathlib import Path
import pandas as pd


my_file = Path("/home/intern/common_final.csv")
r = []    
if my_file.is_file():
    df = pd.read_csv(my_file)
    saved_column = list(df.word)
    #print(saved_column)
    
    with open('common_final.csv', 'w') as csvfile1:
        fieldnames = ['word', 'word_count']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
        writer.writeheader()      
    
    for w in a_list_mixed:
            #print(w[0])
            if w[0] in saved_column:
                #print("in if block")
                file_object = open("common_final.csv","a")
                w[1] = int(w[1]+w[1])
                print(w[0],w[1])
                z0 = (w[0],w[1])
                r.append(z0)
                fieldnames = ['word', 'word_count']
                writer = csv.DictWriter(file_object, fieldnames=fieldnames)
                writer.writerow({'word': w[0], 'word_count':w[1]})
                file_object.close()
       
                        
            else:
                #print("in else block")
                doct = open("common_final.csv","a")
                a = w[0]
                b = w[1]
                print(a,b)
                z1 = (a,b)
                r.append(z1)
                write=csv.writer(doct)
                write.writerow([a,b])
                doct.close()
    
                    
else:
   
    with open('common_final.csv', 'w') as csvfile:
        
        fieldnames = ['word', 'word_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
 
        for words in a_list_mixed:
            writer.writerow({'word': words[0] , 'word_count': words[1]})
            print(words[0], words[1])
            r.append(words[0], words[1])

            
            
from operator import itemgetter
data=list(sorted(r,key = lambda x:x[1],reverse=True))
data1=[x[0] for x in data]
#print(str(data1))
my_string1 = ' '.join(data1)
print(my_string1)


# # Step 13 . Formation of WordCloud(TagCloud)

# In[25]:


wc = WordCloud(background_color="black", max_words=1000)
wc = WordCloud(width=1024, height=768)
wc.generate(my_string1)
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()
plt.show()

