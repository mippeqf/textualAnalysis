import json
import requests
from bs4 import BeautifulSoup


# TODO: Add parent label to labels containing "HTML" or "PDF"
# Setup
recentList = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
archiveList = "https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm"
data = []  # main dict list containing links and metadata
yearList = []  # helper list

# HTML links for past 5 years
soup = BeautifulSoup(requests.get(recentList).content, features="html.parser")
containers = soup.find_all("div", class_="panel")
for cont in containers:
    for linkTag in cont.find_all("a"):
        year = cont.find(class_="panel-heading").get_text(strip=True).replace("FOMC Meetings", "").strip()
        if linkTag != None and linkTag.has_attr("href"):  # and "minutes" in linkTag["href"].lower():
            newEntry = {"year": year, "meeting": "", "label": linkTag.get_text(), "link": linkTag["href"]}
            data.append(newEntry)


# Compile list of pages for individual archive years
soup = BeautifulSoup(requests.get(archiveList).content, features="html.parser")
yearLinks = soup.select(".panel > ul> li > a")  # CSS selector implementation based on SoupSieve
for link in yearLinks:
    if link != None:
        yearList.append("https://www.federalreserve.gov"+link["href"])  # href needs to be called with ["href"], .href does not work

# Scrape HTML links from archive year pages and add to data list
for link in yearList:
    soup = BeautifulSoup(requests.get(link).content, features="html.parser")
    year = soup.find("h3").get_text()  # not fool proof
    print("Archive year: ", year, link)
    if int(year) < 1993:
        break
    containers = soup.find_all("div", class_="panel")
    print("Number of containers: ", len(containers))
    for cont in containers:
        for linkTag in cont.find_all("a"):
            meeting = cont.find(class_="panel-heading").get_text(strip=True)
            if linkTag != None:  # and "minutes" in linkTag["href"].lower():
                newEntry = {"year": year, "meeting": meeting, "label": linkTag.get_text(), "link": linkTag["href"]}
                data.append(newEntry)
                # print("Extracted information: ", newEntry)
    print(len(data))
    print()

# Append data type
for i, entry in enumerate(data):
    entry["type"] = entry["link"].split(".")[-1]
    data[i] = entry

# Save data to textfile
f = open("data/1 fomcLinks.txt", "w")
json.dump(data, f)
