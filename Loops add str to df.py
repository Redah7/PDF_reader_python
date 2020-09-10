# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 22:29:10 2020

@author: MLCMOG001
"""

import os
import pandas as pd
import PyPDF2
import io    
import numpy as np

#NLTK PACKAGES
import nltk
import nltk.corpus

from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer,PorterStemmer
from nltk.corpus import stopwords
import re
nltk.download('wordnet')


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
#cv_list=['Du_Plessis_Morné.pdf']
#cv_list=['Kgogo_Alfred_.pdf', 'Du_Plessis_Morné.pdf', 'Booi_Lungisani.pdf','Ajayi_Olabode.pdf']
#cv_list= os.listdir(os.getcwd())

#cv_list = os.listdir(os.getcwd())
#cv_list=['Ajayi_Olabode.pdf', 'Kgogo_Alfred_.pdf']
#cv_list=['Ajayi_Olabode.pdf']

#cv_list = ['Botha_Marne.pdf', 'Charters_Daniel.pdf', 'Charters_Daniel.pdf' ]


#EMPTY DF FOR CV NAME AND ACTUAL CV 
df=pd.DataFrame(columns=['CV','cv_content'])

#LOOP THRU FOLDER, OUTPUT A DF OF ALL CV WITH CV NAME 

for cv_name in cv_list:
    pdfFileObj = open(cv_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #loop through all pages of the pdf
    for i in range(0, pdfReader.getNumPages()):
        
        df=df.append({'CV':cv_name,
                      'cv_content':pdfReader.getPage(i).extractText()
                }
    ,ignore_index=True
                )
    pdfFileObj.close()
    

#DROP BLANK STR ROWS. 1st convert empty cells to np.nan using replace() and then call dropna() 
df['cv_content'].replace('',np.nan,inplace=True)  
df.dropna(subset=['cv_content'], inplace=True)
    

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer() 

def preprocess(sentence):
    sentence=str(sentence)
    sentence = sentence.lower()
    sentence=sentence.replace('{html}',"") 
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', sentence)
    rem_url=re.sub(r'http\S+', '',cleantext)
    rem_num = re.sub('[0-9]+', '', rem_url)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(rem_num)  
    filtered_words = [w for w in tokens if len(w) > 2 if not w in stopwords.words('english')]
    stem_words=[stemmer.stem(w) for w in filtered_words]
    lemma_words=[lemmatizer.lemmatize(w) for w in stem_words]
    return " ".join(filtered_words)




df['processed_cleaned'] = df.apply(lambda row: preprocess(row['cv_content']), axis=1)
df['processed_tokenized'] = df.apply(lambda row: nltk.word_tokenize(row['processed_cleaned']), axis=1)

#explode list of cv_co ntent values
df=df.explode('processed_tokenized').reset_index(drop=True)

#df mimics the data dict of most used terms


d = {'processed_tokenized': ['data', 'sql', 'computer', 'science', 'engineering', 'database', 'oracle', 'linux', 'deeplearning', 'physics'], 'value': [4, 5, 6,1,1,5,5,5,20,20]}
datadict = pd.DataFrame(data=d)

joined_df=pd.merge(df, datadict, on='processed_tokenized', how='inner')
output_df=joined_df.groupby(['CV'])['value'].sum().reset_index()
output_df.sort_values('value', ascending=False)

'''
df = pd.DataFrame(columns=['A'])
for i in range(5):
    df = df.append({'A': i}, ignore_index=True)
df

'''




'''
temp_df = pd.DataFrame() #Temporary empty dataframe
for sent in Sentences:
    New_df = pd.DataFrame({'words': sent.words}) #Creates a new dataframe and contains tokenized words of input sentences
    temp_df = temp_df.append(New_df, ignore_index=True) #Moving the contents of newly created dataframe to the temporary dataframe
'''



