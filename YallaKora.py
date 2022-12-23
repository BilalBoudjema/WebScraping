import requests
from bs4 import BeautifulSoup
import csv

# page_date = input("Select The Date Of the Page in the following format MM/DD/YYYY : ")
# page = requests.get(f"https://www.yallakora.com/Match-Center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={page_date}#matchesclipPrev")
page = requests.get("https://www.yallakora.com/Match-Center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date=12/10/2022#matchesclipPrev")


def main(Page):
    src = Page.content
    soup = BeautifulSoup(src, "lxml")
    matchs_details = []
    championships = soup.find_all("div", {'class': 'matchCard'})

    def getmatchinfo(championships):
        championship_title = championships.contents[1].find('h2').text.strip()
        all_matchs = championships.contents[3].find_all('li')
        number_of_matches = len(all_matchs)

        for j in range(number_of_matches):
            # get teams names
            TeamA = all_matchs[j].find('div', {'class': 'teamA'}).text.strip()
            TeamB = all_matchs[j].find('div', {'class': 'teamB'}).text.strip()

            # get score
            match_result = all_matchs[j].find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

            # get match time
            match_time = all_matchs[j].find('div', {'class': 'MResult'}).find('span', {'class': 'time'}).text.strip()

            # add matchs info to matchs_details
            matchs_details.append({"Championship Type": championship_title, "Team A ": TeamA, "Team B ": TeamB,
                                   "Game Time": match_time, " Score": score})

    for i in range(len(championships)):
        getmatchinfo(championships[i])

    keys = matchs_details[0].keys()
    
    with open('matches_details.csv', 'w', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matchs_details)
        print("File Created")


main(page)
