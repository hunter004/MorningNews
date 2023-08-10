import sys
sys.path.append('..\MorningNews')
import requests
import config
import json
from datetime import datetime,timedelta
import os

class NewsAssitant:
    """
    class controls pulling in api key for NewsAPI and making requests
    """
    def __init__(self, newsRequests):
        self.apikey = config.api_key
        self.newsRequests = newsRequests
        self.formattedDatetime = f"{datetime.now().year}_{datetime.now().month}_{datetime.now().day}"
        
    def _getNews(self,url):
        """
        GET request to NewsAPI api
        Args:
            url (string): url to submit to api request containing the api_key
        Returns:
            dictionary<string,array>: returns json response from get request formatted into python dictionary
        """
        try:
            response = requests.get(url)
            news = json.loads(response.text)
            return news
        except Exception as e:
            with open("..\MorningNews\ErrorLogs\errors.txt","a") as errorFile:
                errorFile.write(f"{self.formattedDatetime}: Error Occured during GET: {url}\n{e}\n\n")
            return {'articles':[]}
        
    def _cleanOldNewsFiles(self):
        """
        Looks at TodaysNews directory and deletes files greater than 7 days old
        """
        for filename in os.listdir("..\MorningNews\TodaysNews"): 
            file_path = os.path.join("..\MorningNews\TodaysNews", filename)  
            try:
                if os.path.isfile(file_path) and (datetime.now() - timedelta(days=7))>datetime.fromtimestamp(os.path.getctime(file_path)):
                    os.remove(file_path)    
            except Exception as e:  
                print(f"{self.formattedDatetime}: Error deleting {file_path}: {e}")
             
    def _writeNews(self,data):
        """
        Writes data about News articles to dailynews file
        Args:
            data (dictionary<string,string>): data dictionary containing information about news article
        """
        try:   
            with open(f"..\MorningNews\TodaysNews\dailynews_{self.formattedDatetime}.txt","a") as newsFile:
                newsFile.write(f"Article Title: {data['articleTitle']}\n")
                newsFile.write(f"Description: {data['articleDescription']}\n")
                newsFile.write(f"Article Source: {data['articleSource']}\n")
                newsFile.write(f"\n\nNews Group: {data['requestTitle']}\n")
                newsFile.write(f"Published Date: {data['articleDate']}\n")             
                newsFile.write(f"Link: {data['articleURL']}\n")
        except Exception as e:
            with open("..\MorningNews\ErrorLogs\errors.txt","a") as errorFile:
                errorFile.write(f"{self.formattedDatetime}: Error Occurred during Article Write: {data['requestTitle']} - {data['articleTitle']}\n{e}\n\n")
                
    def processNewsRequests(self):
        """
        processes request submitted
        cleans old news
        calls api to get news
        appends any new data to the daily news article
        """
        self._cleanOldNewsFiles()
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
                    ,'articleDescription' : article['description']
                }
                self._writeNews(data)