import sys
sys.path.append('..\MorningNews')
import config
from NewsAssistant import NewsAssitant

assistant = NewsAssitant(config.newsRequests)
try:
    assistant.processNewsRequests()
    print("\nGood Morning, daily news is available\n")
except Exception as e:
    print(f"Error getting daily news: {e}")