# import the necessary libraries
import enchant
from django.shortcuts import render
from collections import Counter
import PyPDF2
import io
import inflect
import nltk
import string
import re
from nltk.corpus import stopwords
from django.http import JsonResponse
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from gensim.parsing.preprocessing import remove_stopwords
from .utlis import get_plot

def convert_number(text):
    p = inflect.engine()
    # split string into list of words
    temp_str = text.split()
    # initialise empty list
    new_string = []
  
    for word in temp_str:
        # if word is a digit, convert the digit
        # to numbers and append into the new_string list
        if word.isdigit():
            temp = p.number_to_words(word)
            new_string.append(temp)
  
        # append the word as it is
        else:
            new_string.append(word)
  
    # join the words of new_string to form a string
    temp_str = ' '.join(new_string)
    return temp_str
def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)
# remove whitespace from text
def remove_whitespace(text):
	return " ".join(text.split())

def remove_stopwords_again(text):
    
    text=remove_stopwords(text)
    return text
# remove stopwords function
def removestopwords(text):
	
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(['Marks','section','questions','mark','attempt','what','draw','write','read','answer','Section','What','explain','Explain','brief','Brief','Explain','Draw','Download','download','More','more'])
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stopwords]
	
    return filtered_text







def lemmatize_word(text):
    lemmatizer = WordNetLemmatizer()
    word_tokens = word_tokenize(text)
    # provide context i.e. part-of-speech
    lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in word_tokens]
    return lemmas




def preprocess(arr):
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    text="".join(arr)
    text=re.sub(r'\b\w{1,3}\b', '',text)
    text=re.sub(r'\d+', '', text)
    text=convert_number(text)
    text=remove_punctuation(text)
    text=remove_whitespace(text)
    
    text1=remove_stopwords_again(text)
    text2=removestopwords(text)

   
    return text2
def find_frequency(text):
    # Pass the split_it list to instance of Counter class.
    Counter_found = Counter(text)
    
    # most_common() produces k frequently encountered
    # input values and their respective counts.
    most_occur = Counter_found.most_common(15)
    return most_occur
  
  

    
  


  

def home(request):
    if request.method=='POST':
        #Reading first PDF
        d = enchant.Dict("en_US") 
        pdfFileObj1 = request.FILES['paper1'].read() 
        pdfReader1 = PyPDF2.PdfFileReader(io.BytesIO(pdfFileObj1))
        NumPages = pdfReader1.numPages
        i = 0
        content = []
        while (i<NumPages):
            text = pdfReader1.getPage(i)
            content.append(text.extractText())
            i +=1
        
        #Reading Second PDF


        pdfFileObj2 = request.FILES['paper2'].read() 
        pdfReader2 = PyPDF2.PdfFileReader(io.BytesIO(pdfFileObj2))
        NumPages = pdfReader2.numPages
        i = 0
        
        while (i<NumPages):
            text = pdfReader2.getPage(i)
            content.append(text.extractText())
            i +=1
        res=preprocess(content)
        res1=[]
        for i in res:
            if(d.check(i)):
                res1.append(i)
        keywords=find_frequency(res1)
        lables=[]
        data=[]
        for i in keywords:
            lables.append(i[0])
            data.append(i[1])
        chart=get_plot(lables,data)
        return render(request,'result.html',{'chart':chart})
    return render(request,'home.html')