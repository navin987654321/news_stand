from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import newsfeed.tweets as tweets
# Create your views here.

sia = SentimentIntensityAnalyzer()
def home(request):
    search = request.GET.get('search', None)
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

def newsapi(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)

    if search is None:
        url = "https://newsapi.org/v2/top-headlines?country={}&apiKey={}".format("us", settings.NEWSAPI_KEY)
    else:
        url = "https://newsapi.org/v2/everything?q={}&apiKey={}".format(search, settings.NEWSAPI_KEY)
    r = requests.get(url=url)

    data = r.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]
    context = {
        "success": True,
        "data": [],
        "search": search
    }
    for i in data:
        context["data"].append({
            "title": i["title"],
            "content": "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": "" if i["urlToImage"] is None else i["urlToImage"],
            "publishedat": i["publishedAt"],
            "polarity": sia.polarity_scores("" if i["description"] is None else i["description"])
        })
    
    return render(request, 'newsapi.html', context=context)