import matplotlib.pyplot as plt
import base64
from io import BytesIO
import random
import string
from django.http import HttpResponse

def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer,formate='png')
    buffer.seek(0)
    img_png=buffer.getvalue()
    graph=base64.b64encode(img_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y):
    fig = plt.figure()
    fig = plt.figure(figsize = (15, 5))
    #Bar plot
    plt.bar(x, y, color ='green',width = 0.5)
    plt.xlabel("keywords")
    plt.ylabel("Frequency")
    plt.title("Most important keywords")
    graph=get_graph()
    return graph

