from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import itertools

date = input("Enter the date you want to scrape EX(mm/dd/yy): ")
page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}#days")
def get_data(page):
    src = page.content
    soup = BeautifulSoup(src, 'lxml')
    champoinshap = soup.find_all('div', {'class': 'matchesHpCntnr'})

    # Create lists
    champoinshaps = []
    matches_times = []
    matches_teamsA = []
    matches_teamsB = []
    matches_statuss = []
    matches_scores = []
   
    def get_matches_details(page):
        #get champoinshaps
        matches = soup.find_all('a', {'class': 'tourTitle'})
        for match in matches:
            champoinshaps.append(match.find('h2').text.strip())


    def get_matches_times(page):
        #get matches times
        matches_time = soup.find_all('div', {'class': 'MResult'})
        for match in matches_time:
            matches_times.append(match.find('span', {'class': 'time'}).text.strip())
        
        
    def get_matches_teams(page):
        #get matches teamsA
        matches_team = soup.find_all('div', {'class': 'teams teamA'})
        for match in matches_team:
            matches_teamsA.append(match.find('p').text.strip())
        #get matches teamsB
        matches_team = soup.find_all('div', {'class': 'teams teamB'})
        for match in matches_team:
            matches_teamsB.append(match.find('p').text.strip())
            

    def get_matches_scores(page):
        #get matches scores
        matches_score = soup.find_all('div', {'class': 'MResult'})

        # Iterate over each match
        for match in matches_score:
            # Find the score elements within the match
            score_match = match.find_all('span', {'class': 'score'})
            # Concatenate the scores with a "-" separator
            score = f'{score_match[0].text.strip()} - {score_match[1].text.strip()}'
            # Append the score to the list
            matches_scores.append(score)
        

    
    def get_matches_status(page):
        #get matches status
        matches_status = soup.find_all('div', {'class': 'topData'})
        for match in matches_status:
            states = match.find('div', {'class': 'matchStatus'}).text.strip()
            matches_statuss.append(states)
    
        
    get_matches_details(page)
    get_matches_times(page)
    get_matches_teams(page)
    get_matches_scores(page)
    get_matches_status(page)
    
    #save data in csv file
    result = itertools.zip_longest(champoinshaps, matches_teamsA, matches_scores, matches_teamsB, matches_times, matches_statuss, fillvalue=None)
    data = pd.DataFrame(result,columns=["champoinshaps","teams A","scores","teams B","times","states"])
    data.to_csv('Scraper-Yalla-Kora.csv', index=False, encoding='utf-8')


get_data(page)
