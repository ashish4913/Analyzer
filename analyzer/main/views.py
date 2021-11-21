# import the necessary libraries
import enchant
from django.shortcuts import render
from collections import Counter
import PyPDF2
import io
import random
import matplotlib.pyplot as plt
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
from fuzzywuzzy import fuzz
from django.http import HttpResponse
from django.views.generic import View
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

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
    stopwords.extend(['Answer','answer','following','Following','Given','given','Marks','section','questions','question','Question,''mark','attempt','what','draw','write','read','answer','Section','What','explain','Explain','brief','Brief','Explain','Draw','Download','download','More','more'])
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
def find_fuzz(x,y):
    return fuzz.token_sort_ratio(x,y)
def find_cosine(X,Y):
    X_list = word_tokenize(X) 
    Y_list = word_tokenize(Y)
    
    
    sw = stopwords.words('english') 
    l1 =[];l2 =[]
    
    
    X_set = {w for w in X_list if not w in sw} 
    Y_set = {w for w in Y_list if not w in sw}
    
    
    rvector = X_set.union(Y_set) 
    for w in rvector:
        if w in X_set: l1.append(1) 
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0
    
     
    for i in range(len(rvector)):
            c+= l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine

def find_similar(arr1,arr2):
    d=dict()
    data1=[]
    data2=[]
    for i in range(len(arr1)):
        for j in range(len(arr2)):
            # if(find_fuzz(arr1[i],arr2[j])>40):
            #     print(arr1[i])
            #     print(arr2[j])
            #     print("-------------")
            try:
                x=find_cosine(arr1[i],arr2[j])

                if(x > 0.25 and  x < 0.60 and (abs(  len(arr1[i]) -   len(arr2[j])   )) in [0,1,2,3,4,5,6,7,8,9,10]  and len(arr1[i])>=13):
                    #print(arr1[i])
                    #print(arr2[j])
                    data1.append(arr1[i])
                    data2.append(arr2[j])
                    #print("-----------")
            except:
                pass
    d=zip(data1,data2)            
    return d          
class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('result.html')
        
        html = template.render(context)
        pdf = render_to_pdf('result.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "result%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
def important_questions(arr,keywords):
    imp=[]

    for i in keywords:
        for j in arr:
           
            if(i in j):
                imp.append(j)
    print(imp)
    return list(set(imp))


def home(request):
    if request.method=='POST':
        #Reading first PDF
        d = enchant.Dict("en_US") 
        pdfFileObj1 = request.FILES['paper1'].read() 
        pdfReader1 = PyPDF2.PdfFileReader(io.BytesIO(pdfFileObj1))
        NumPages = pdfReader1.numPages
        i = 0
        content = []
        arr1=[]
        arr2=[]
        while (i<NumPages):
            text = pdfReader1.getPage(i)
            t1=text.extractText()
            content.append(t1)
            arr1.append(t1)
            i +=1
        
        #Reading Second PDF


        pdfFileObj2 = request.FILES['paper2'].read() 
        pdfReader2 = PyPDF2.PdfFileReader(io.BytesIO(pdfFileObj2))
        NumPages = pdfReader2.numPages
        i = 0
        
        while (i<NumPages):
            text = pdfReader2.getPage(i)
            t2=text.extractText()
            content.append(t2)
            arr2.append(t2)
            i +=1

        arr1="".join(arr1)
        arr1=arr1.split(".")

        arr2="".join(arr2)
        arr2=arr2.split(".")
        
        q1=[]
        q2=[]
        for i in arr1:
            res1 = " ".join(i.split())
            if(not re.search(r'\d', res1)):
                q1.append(res1)
        for i in arr2:
            res2 = " ".join(i.split())
            if(not re.search(r'\d', res2)):
                q2.append(res2)
        #print(q1)
        #print(q2)

        similar_questions=find_similar(q1,q2)
        similar_questions=dict(similar_questions)
        ratio=len(similar_questions)
        if(ratio>=180):
            ratio=160

        
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
        q=q1+q2
        
        imp=important_questions(q,lables)
       
        chart=get_plot(lables,data)
        request.session['chart']=chart
        request.session['angle']=180+2*ratio
        request.session['similar']=similar_questions
        request.session['imp']=imp
        
        
       
        return render(request,'result.html',{'chart':chart,'similar':dict(similar_questions),'angle':180+2*ratio,'imp':imp})
    return render(request,'home.html')

def download_pdf(request):
    template_path = 'report.html'
    context = {'chart':request.session['chart'],'angle':request.session['angle'],'similar':request.session['similar'],'imp':request.session['imp']}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response