from bs4 import BeautifulSoup
import time
import requests
from random import randint
import json
import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    # Add more User-Agents if needed
]

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

USER_AGENT={'User-Agent': random.choice(USER_AGENTS)}

print(USER_AGENT)
class SearchEngine:
    @staticmethod
    def search(query, sleep=True):
        if sleep:  # Prevents loading too many pages too soon
            time.sleep(randint(10, 100))
        temp_url = '+'.join(query.split())  # for adding + between words for the query
        url = 'https://www.bing.com/search?q=' + temp_url +'&count=30'
        soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
        new_results = SearchEngine.scrape_search_result(soup)
        return new_results

    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all("li", class_="b_algo", limit=10)
        results = []
        # implement a check to get only 10 results and also check that URLs must not be duplicated
        for result in raw_results:
            a_tag = result.find('a')
            if a_tag and a_tag.has_attr('href'):
                link = a_tag['href']
                # Check for duplicates
                if link not in results:
                    results.append(link)
        return results

# ############ Driver code ############
file_path = 'bing_results.json'

# Load the existing data from the file
with open(file_path, 'r') as file:
    data = json.load(file)

queries=[]
with open('100QueriesSet1.txt', 'r') as file:
    for line in file:
        # Strip newline characters and append to the list
        queries.append(line.strip())

searchresults={}

#results = SearchEngine.search("what is a greeting")
#print(results)

querynumber=0
for i in range(90,100): 
    querynumber=i+1
    results = SearchEngine.search(queries[i])
    searchresults[queries[i]]=results
    print(querynumber)
    print(results)

data.update(searchresults)

with open('bing_results.json', 'w') as file:
    json.dump(data, file, indent=4)
#print(searchresults)
#print(results)
# ####################################
