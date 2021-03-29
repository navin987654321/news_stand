from django.shortcuts import render
from django.conf import settings
import requests
from newsapi import NewsApiClient
# Create your views here.

def home(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)

    if search is None:
        url = "https://newsapi.org/v2/top-headlines?page={}&apiKey={}".format(page, settings.NEWSAPI_KEY)
    else:
        url = "https://newsapi.org/v2/top-headlines?page={}&apiKey={}&q={}".format(page, settings.NEWSAPI_KEY, search)
    
    r = requests.get(url=url)
    data = r.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Could not fetch your news feed, please try again later!")
    data = data["articles"]
    context = {
        "success": True,
        "data": [],
        "search": search
    }
    for i in data:
        context["data"].append({
            "title": i["title"],
            "description": "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": i["urlToImage"],
            "publishedat": i["publishedAt"]
        })
    return render(request, 'home.html', context=context)