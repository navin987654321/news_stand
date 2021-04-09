from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import newsfeed.tweets as tweets
# Create your views here.

def home(request):
    search = request.GET.get('search', None)
    sia = SentimentIntensityAnalyzer()
    if search is None:
        query = 'United States'
    else:
        query = search
    data = tweets.search(query)
    context = {
        "success": True,
        "data": [],
        "topics": data["topics"],
        "search": search
    }
    for i in data["tweets"]:
        context["data"].append({
            "username": i['username'],
            "image": "https://static01.nyt.com/images/2014/08/10/magazine/10wmt/10wmt-superJumbo-v4.jpg" if len(i["photos"])==0 else i["photos"][0],
            "content": i['tweet'],
            "publishedat": i['date'],
            "url": i['link'],
            "polarity": sia.polarity_scores(i['cleaned_tweet']),
        })
    return render(request, 'home.html', context=context)