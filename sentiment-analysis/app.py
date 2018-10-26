from flask import Flask
from flask import request
import os 
import glob, os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from os import environ
import json
import io
import pandas as pd


# from heapq import nlargest
# from heapq import nsmallest

app = Flask(__name__)
# global identifier


@app.route("/")
def index():
    return "Python Microservice To fetch sentiment score"

@app.route("/sentimentanalysis")
def sentiment_anlysis():
    df = pd.ExcelFile('./ticket_data.xlsx').parse('tickets_resolved')
    var1=df['FeedBack']
    l=len(var1)
    print(l)
    sentences=[]
    for i in range(l):
        sentences.append(str(var1[i]))
    print("sentences")
    print("********")
    print(sentences)
    analyzer = SentimentIntensityAnalyzer()
    data_sentiment =[{
        "Positive_Scores":[],
        "Negative_Scores":[],
        "Neutral_Scores":[],
        "Top_Five_Positives":[],
        "Top_Five_Negatives":[],
        "Overall_Sentiment_Score":0,
        "Overall_Positive_Score":0,
        "Overall_Negative_Score":0,
        "Overall_Neutral_Score":0
    }]
    # overall_pos=0
    # overall_neg=0
    # overall_neg=0
    score=0.0
    sent=0.0
    Positive_Score=0
    Negative_Score=0
    Neutral_Score=0
    for sentence in sentences:
        pos = 0
        neg = 0
        neu = 0
        vs = analyzer.polarity_scores(sentence)
        sent += vs['compound']
        pos = pos + vs['pos']
        neg = neg + vs['neg']
        neu = neu + vs['neu']
        if neg > pos :
            feedback="negative"
            data_sentiment[0]["Negative_Scores"].append({"score":neg,"sentence":sentence})
            score=score+neg
        elif neg == pos :
            feedback = "neutral"
            data_sentiment[0]["Neutral_Scores"].append({"score":neu,"sentence":sentence})
            score=score+neu
        else:
            feedback ="positive"
            data_sentiment[0]["Positive_Scores"].append({"score":pos,"sentence":sentence})
            score=score+pos
    
    Overall_Sentiment_Score= (sent / l ) * 100
    data_sentiment[0]["Overall_Sentiment_Score"] = round(Overall_Sentiment_Score, 2)

    Positive_Length=len(data_sentiment[0]["Positive_Scores"])
    for i in range(Positive_Length):
        Positive_Score = Positive_Score + data_sentiment[0]["Positive_Scores"][i]["score"]
    Overall_Positive_Score = ( Positive_Score / score ) * 100
    data_sentiment[0]["Overall_Positive_Score"]=round(Overall_Positive_Score, 2)

    Negative_length = len(data_sentiment[0]["Negative_Scores"])
    for i in range(Negative_length):
        Negative_Score = Negative_Score + data_sentiment[0]["Negative_Scores"][i]["score"]
    Overall_Negative_Score = ( Negative_Score / score ) * 100
    data_sentiment[0]["Overall_Negative_Score"]=round(Overall_Negative_Score, 2)

    Neutral_length = len(data_sentiment[0]["Neutral_Scores"])
    for i in range(Neutral_length):
        Neutral_Score = Neutral_Score + data_sentiment[0]["Neutral_Scores"][i]["score"]
    Overall_Neutral_Score = ( Neutral_Score / score ) * 100
    data_sentiment[0]["Overall_Neutral_Score"]=round(Overall_Neutral_Score, 2)

    # pairs = (json.loads(line) for line in data_sentiment[0]["Positive_Scores"])
    # largest_pairs = heapq.nlargest(5, pairs, key=lambda p: int(p[1]))
    # print([': '.join(pair) for pair in largest_pairs])
    print(Positive_Score)
    # print(data_sentiment)
    # all_positive_scores=[]
    # all_negative_scores=[]
    tags=[]
    for i in range(Positive_Length):
        sentence1=(data_sentiment[0]["Positive_Scores"][i]["sentence"])
        score1=str(data_sentiment[0]["Positive_Scores"][i]["score"])
        tags.append(""+sentence1+":"+score1+"")
       
        # largest_pairs = heapq.nlargest(3, tags, key=lambda p: int(p[1]))
        # print("*********************tags*************************")
        # print(all_positive_scores)
    for i in range(Negative_length):
        sentence1=(data_sentiment[0]["Negative_Scores"][i]["sentence"])
        score1=str(data_sentiment[0]["Negative_Scores"][i]["score"])
        tags.append(""+sentence1+":"+score1+"")
         
    # data_sentiment[0]["Top_Five_Positives"].append(nlargest(5, data_sentiment[0]["Positive_Scores"]))
    # data_sentiment[0]["Top_Five_Negatives"].append(nsmallest(5,data_sentiment[0]["Negative_Scores"]))
    print("##############")
    # print(tags)
    print(Positive_Length-5)
    # print(Positive_length-5)
    Top_Five_Positives=(sorted(data_sentiment[0]["Positive_Scores"], key=repr,reverse=True))[:-(Positive_Length-5)]
    print(Top_Five_Positives)
    if Top_Five_Positives==[]:
        Top_Five_Positives=(sorted(data_sentiment[0]["Positive_Scores"], key=repr))[:Positive_length] 
    Top_Five_Negatives=(sorted(data_sentiment[0]["Negative_Scores"], key=repr,reverse=True))[:-(Negative_length-5)] 
    print(Top_Five_Negatives)
    if Top_Five_Negatives == []:
        print("in if")
        Top_Five_Negatives=(sorted(data_sentiment[0]["Negative_Scores"], key=repr,reverse=True))[:Negative_length] 
        print(Top_Five_Negatives)
    data_sentiment[0]["Top_Five_Positives"].append(Top_Five_Positives)
    data_sentiment[0]["Top_Five_Negatives"].append(Top_Five_Negatives)
    data_sentiment=json.dumps(data_sentiment ,indent=4, sort_keys=True)
    print(data_sentiment)
   

    return data_sentiment
    
        
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
    # sentiment_anlysis()