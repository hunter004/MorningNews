import requests
import sys
sys.path.append('..\MorningNews')
import config
import json

class NewsAssitant:
    """
    _summary_
    class controls pulling in api key for NewsAPI and making requests
    """
    def __init__(self, newsRequests):
        self.apikey = config.api_key
        self.newsRequests = newsRequests
        
    def _getNews(self,url):
        try:
            response = requests.get(url)
            news = json.loads(response.text)
            return news
        except:
            with open("..\MorningNews\ErrorLogs\errors.txt","a") as errorFile:
                errorFile.write(f"Error Occured during GET: {url}")
            return {'articles':[]}
                
    def _writeNews(self,data):
        try:
            with open("..\MorningNews\TodaysNews\dailynews.txt","a") as newsFile:
                newsFile.write(f"\n\nNews Group: {data['requestTitle']}\n")
                newsFile.write(f"Article Source: {data['articleSource']}\n")
                newsFile.write(f"Article Title: {data['articleTitle']}\n")
                newsFile.write(f"Published Date: {data['articleDate']}\n")
                newsFile.write(f"Link: {data['articleURL']}\n")
        except:
            with open("..\MorningNews\ErrorLogs\errors.txt","a") as errorFile:
                errorFile.write(f"Error Occurred during Article Write: {data['requestTitle']} - {data['articleTitle']}")
                
    def processNewsRequests(self):
        for r in self.newsRequests:
            requestTitle = r['Title']
            requestURL = r['URL']
            news = self._getNews(requestURL)
            for article in news['articles']:
                data = {
                    'requestTitle' : requestTitle
                    ,'articleSource' : article['source']['name']
                    ,'articleTitle' : article['title']
                    ,'articleURL' : article['url']
                    ,'articleDate' : article['publishedAt']
                    ,'content' : article['content']
                }
                self._writeNews(data)