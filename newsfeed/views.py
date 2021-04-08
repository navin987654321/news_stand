from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from newsapi import NewsApiClient
import twint
# Create your views here.

def home(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)
    sia = SentimentIntensityAnalyzer()
    if search is None:
        query = 'United States'
    else:
        query = search
    c = twint.Config()
    c.Search = query
    c.Limit = 1000
    c.Lang = 'en'
    c.Pandas = True
    c.Hide_output = True
    twint.run.Search(c)
    data = twint.output.panda.Tweets_df[['id', 'username', 'photos', 'tweet', 'date']].to_dict(orient='index')
    context = {
        "success": True,
        "data": [],
        "search": search
    }
    for i in data.values():
        context["data"].append({
            "username": i['username'],
            "image": "https://static01.nyt.com/images/2014/08/10/magazine/10wmt/10wmt-superJumbo-v4.jpg" if len(i["photos"])==0 else i["photos"][0],
            "content": i['tweet'],
            "publishedat": i['date'],
            "polarity": sia.polarity_scores("" if i['tweet'] is None else i['tweet'])
        })
    return render(request, 'home.html', context=context)