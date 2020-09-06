# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 21:46:07 2020

@author: MLCMOG001
"""
import os
import pandas as pd
import PyPDF2
import io    

import nltk
import nltk.corpus
#import texthero


    
os.chdir ('C:\\Users\\MLCMOG001\\Desktop\\CV Ranker\\CV data')
cwd = os.getcwd() 

'''
#pd.read_csv("Report.csv")
# you can find find the pdf file
# pdf file object with complete code in below
#loop thru all pages in pdf and output pages as objects
for root, dirs, files in os.walk("."):
    for filename in files:
        print(filename)
        
'''



#print(list1)
#cv_list=['Ajayi_Olabode.pdf']
#cv_list=['Kgogo_Alfred_.pdf']
#cv_list=['Kgogo_Alfred_.pdf', 'Du_Plessis_Morné.pdf', 'Booi_Lungisani.pdf','Ajayi_Olabode.pdf']
#cv_list= os.listdir(os.getcwd())

cv_list = os.listdir(os.getcwd())

cv_compile_str = ""
for cv_name in cv_list:
    pdfFileObj = open(cv_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #loop through all pages of the pdf
    for i in range(0, pdfReader.getNumPages()):
        exec(f'cv_compile_str+=pdfReader.getPage(i).extractText()')
    pdfFileObj.close()



'''
NEED TO IMCLUDE A TEXT CLEANUP 

'''

# importing word_tokenize from nltk
from nltk.tokenize import word_tokenize

# Passing the string text into word tokenize for breaking the sentences
token = word_tokenize(cv_compile_str)


# finding the frequency distinct in the tokens
# Importing FreqDist library from nltk and passing token into FreqDist
from nltk.probability import FreqDist
fdist = FreqDist(token)
fdist

#list top ten words.
fdist.most_common(10)



'''
REMOVE PUNCTUATION
'''
words_no_punc=[]

#remove punctuation:
for w in token:
    if w.isalpha():
        words_no_punc.append(w.lower())
        
fdist = FreqDist(words_no_punc)
fdist



'''
REMOVE STOPWORDS
'''

#REMOVE STOP WORDS
from nltk.corpus import stopwords

#LIST OF STOPWORDS
stopwords=stopwords.words("english")

#CREATE EMPTY LIST

clean_words=[]

for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(w)

fdist = FreqDist(clean_words)
fdist

fdist.most_common(30)



'''
#CREATE EMPTY STR loop and add str together with each run
s = ""
for i in range(5):
    s+=str(i)
'''


#semi working
#This section will loop through all pages in the CV's 
#but the outputs will strat writing over each other

for cv_name in cv_list:
    pdfFileObj = open(cv_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #loop through all pages of the pdf
    for i in range(0, pdfReader.getNumPages()):
        exec(f'pdf_{i}=pdfReader.getPage(i).extractText()')
    pdfFileObj.close()
  
    
    
pdfFileObj = open('Kgogo_Alfred_.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#loop through all pages of the pdf
for i in range(0, pdfReader.getNumPages()):
    exec(f'pdf_{i}=pdfReader.getPage(i).extractText()')
pdfFileObj.close()

#hardcoded concat of all the extracted pdfs and convert to a df
concat_str=(pdf_0+pdf_1+pdf_2+pdf_3)


#need to fix this concaty
concat_series=pd.Series(concat_str)
df=concat_series.to_frame('cv')
df["id"]=['1']



# pdf file object
# you can find find the pdf file with complete code in below
#loop thru all pages in pdf and output pages as objects
pdfFileObj = open('Du_Plessis_Morné.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#loop through all pages of the pdf
for i in range(0, pdfReader.getNumPages()):
    exec(f'pdf_{i}=pdfReader.getPage(i).extractText()')
pdfFileObj.close()

#hardcoded concat of all the extracted pdfs and convert to a df
concat_str=(pdf_0+pdf_1+pdf_2)

#need to fix this concaty
concat_series=pd.Series(cv_compile_str)
df1=concat_series.to_frame('cv')
df1["id"]=['2']

#concat the 
frames = [df, df1]
result = pd.concat(frames)

#create custom pipeline
from texthero import preprocessing

custom_pipeline = [preprocessing.fillna,
                   preprocessing.lowercase,
                   preprocessing.remove_digits,
                   preprocessing.remove_punctuation,
                   preprocessing.remove_urls,
                   preprocessing.remove_stopwords,
                   preprocessing.remove_whitespace
                   ]
#altearnative for custom pipeline
#altearnative for custom pipeline
 
result['clean_cv'] = result['cv'].pipe(hero.clean, custom_pipeline)


import matplotlib.pyplot as plt

NUM_TOP_WORDS = 20

top_20 = hero.visualization.top_words(result['clean_cv']).head(NUM_TOP_WORDS)

hero.wordcloud(result['clean_cv'], max_words=100,)



#Loading NLTK
import nltk
nltk.download('punkt')


from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

text="""Hello Mr. Smith, how are you doing today? The weather is great, and city is awesome.
The sky is pinkish-blue. You shouldn't eat cardboard"""
tokenized_text=sent_tokenize(text)

tokenized_word=word_tokenize(concat_str)
print(tokenized_word)


from nltk.probability import FreqDist
fdist = FreqDist(tokenized_word)
print(fdist)



