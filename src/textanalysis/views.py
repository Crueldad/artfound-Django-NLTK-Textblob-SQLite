from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.apps import apps
from homepage.models import Comment
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import textblob
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
from textblob.classifiers import NaiveBayesClassifier
from textblob.classifiers import DecisionTreeClassifier
from textblob import classifiers
import re
import json 


def parse_query(updated_querystring):
    char_index = 0
    main_dict = {}

    updated_querystring = updated_querystring.replace("<QuerySet [","")
    updated_querystring = str(updated_querystring[0:-2])

    print ("String to convert to Dictionary: ",updated_querystring)

    while len(updated_querystring) > 3:

        if updated_querystring[char_index] == "{":
            # print ("should start a dictionary")
            key_string = ""
            value_string = ""
            char_index += 19
            # print (" updated_querystring[char_index] : ",  updated_querystring[char_index])

            # Get Key Name
            while updated_querystring[char_index] != "'":
                key_string += updated_querystring[char_index]
                char_index += 1
            
            # Jump to Value
            char_index += 19
            # print ("New first letter: ",  updated_querystring[char_index] )

            # Get Value
            while updated_querystring[char_index] != "'":
                value_string += updated_querystring[char_index]
                char_index += 1

            # print ("Key String: ",key_string)
            # print ("Value String: ",value_string)
            
            # Convert from string to list
            value_list = [value_string]

            if key_string in main_dict:
               list_of_comments = main_dict[key_string]
               list_of_comments.append (value_string)
            else:
                main_dict[key_string] = value_list

        # Remove Key and Value from string before starting loop again
        updated_querystring = updated_querystring[char_index+4:]

        # print ("Updated after addinging to dict:  ", updated_querystring)
        char_index = 0

    return main_dict
def textanalysis(request):
    return render(request, 'textanalysis/textanalysis.html')

def gettext(request):
    
    info = Comment.objects.values('Artwork_Title','Comment_Box').order_by('-id')
    f = str(type(info))
    first_value =  Comment.objects.all()[:1].get()

    returned_query_string = str(info)
    parsed_dictionary = parse_query(returned_query_string)


    
    for x in parsed_dictionary:
        if x == 'FISHES SWIMMING':
            FSV = parsed_dictionary['FISHES SWIMMING']
            K = []
            for sentence in FSV:
                tb=TextBlob(sentence)
                if tb.detect_language() == 'en':
                    egv = tb
                    egv = str(egv)
                    K = K+[egv]
                else:
                    egv = tb.translate(to = 'en')
                    egv = str(egv)
                    egv = egv.replace('TextBlob', '')
                    K = K + [egv]
            vader = SentimentIntensityAnalyzer()
            F = sum([vader.polarity_scores(str(sentence))['compound'] for sentence in K])/len([vader.polarity_scores(sentence)['compound'] for sentence in K])
            y = F
            
            
        if x == 'NAUTICAL WONDER':
            FSV1 = parsed_dictionary['NAUTICAL WONDER']
            Z = []
            for sentence1 in FSV1:
                tb=TextBlob(sentence1)
                if tb.detect_language() == 'en':
                    egv1 = tb
                    egv1 = str(egv1)
                    Z = Z+[egv1]
                else:
                    egv1 = tb.translate(to = 'en')
                    egv1 = str(egv1)
                    egv1 = egv1.replace('TextBlob', '')
                    Z = Z + [egv1]
            vader = SentimentIntensityAnalyzer()
            N = sum([vader.polarity_scores(str(sentence1))['compound'] for sentence1 in Z])/len([vader.polarity_scores(str(sentence1))['compound'] for sentence1 in Z])
            y = N
            
            
        if x == 'DESERT BIRD':
            FSV2 = parsed_dictionary['DESERT BIRD']
            A = []
            for sentence2 in FSV2:
                tb=TextBlob(sentence2)
                if tb.detect_language() == 'en':
                    egv2 = tb
                    egv2 = str(egv2)
                    A = A+[egv2]
                else:
                    egv2 = tb.translate(to = 'en')
                    egv2 = str(egv2)
                    egv2 = egv2.replace('TextBlob', '')
                    A = A + [egv2]
            vader = SentimentIntensityAnalyzer()
            D = sum([vader.polarity_scores(str(sentence2))['compound'] for sentence2 in A])/len([vader.polarity_scores(str(sentence2))['compound'] for sentence2 in A])
            y = D
            
            

    if -1<= y < -0.6:
        sentiment = ('Overall sentiment is Negative')
    if -.6<= y < -0.2:
        sentiment = ('Overall sentiment is Somewhat Negative')
    if -0.2 <= y < 0.2:
        sentiment = ('Overall sentiment is Neutral')
    if 0.2 <= y < .6: 
        sentiment = ('Overall sentiment is Somewhat Positive')
    if .6 <= y <= 1.0:
        sentiment =('Overall sentiment is Positive')

    if F > N and F > D:
        Best_Comment = ('The artwork with the best comments is: Fishes Swimming')
        common = parsed_dictionary['FISHES SWIMMING']
        photos = "https://i.imgur.com/NwSJbD4.jpg"
    if N > F and N > D:
        Best_Comment = ('The artwork with the best comments is: Nautical Wonder')
        common = parsed_dictionary['NAUTICAL WONDER']
        photos = "https://i.imgur.com/knBftJv.jpg"
    if D > N and D > F:
        Best_Comment = ('The artwork with the best comments is: Desert Bird')
        common = parsed_dictionary['DESERT BIRD']
        photos = "https://i.imgur.com/9BnY3kd.jpg"

    K = ''   
    for word in common:
        K = K + ' ' + word
    kp = K.replace("TextBlob", "").replace(".", "").replace("!","").replace("?","")
    K = word_tokenize(kp)
    filtered_sent= []
    stop_words= set(stopwords.words('english'))
    for w in K:
        if w not in stop_words:
            filtered_sent.append(w)
    #print(filtered_sent)
    fdist = FreqDist(filtered_sent)
    # print(len(filtered_sent))
    x = (.10*len(filtered_sent))
    if x < 1:
        x = 1
    else:
        x = int(x)
    most_common_w = 'These are the common words from all comments under the choosen artwork:', (fdist.most_common(x)) 

    
    DB = parsed_dictionary['DESERT BIRD'] 

    NW = parsed_dictionary['NAUTICAL WONDER']

    SW = parsed_dictionary['FISHES SWIMMING']

    


        
    return render(request, 'textanalysis/textanalysis.html', {'Best_Comment':Best_Comment, 'sentiment':sentiment,\
        'most_common_w':most_common_w, 'DB':DB, 'NW':NW, 'SW':SW, 'F':F, 'N':N, 'D':D, 'photos':photos})
    
   