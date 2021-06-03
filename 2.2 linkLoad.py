import json
import requests
from bs4 import BeautifulSoup
import pickle
from datetime import datetime
from tqdm import tqdm

# Setup
recentList = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
archiveList = "https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm"
data = []  # main dict list containing links and metadata
archiveYearsLinks = []  # helper list

#########################################################
# Scrape RECENT pages
#########################################################

# HTML links for RECENT 5 years
print("Scraping links for recent 5 years")
soup = BeautifulSoup(requests.get(recentList).content, features="html.parser")
panels = soup.find_all("div", class_="panel")
for pnl in panels:
    for minutesBox in pnl.find_all("div", class_="fomc-meeting__minutes"):
        try:
            year = pnl.find(class_="panel-heading").get_text(strip=True).replace("FOMC Meetings", "").strip()
            release = minutesBox.get_text(strip=True).split("Released ")[-1].replace(")", "")
            release = datetime.strptime(release, "%B %d, %Y").date()
            link = minutesBox.find("a", text="HTML")["href"]
            newEntry = {"year": year, "release": release, "link": "https://www.federalreserve.gov"+link}
            print(newEntry)
            data.append(newEntry)
        except Exception as e:
            print("Exception:", minutesBox.get_text(strip=True), e)

print("-------------------------------------------")

#########################################################
# Scrape ARCHIVE pages
#########################################################


def try_parsing_date(text):
    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError('no valid date format found for', text)


# Compile list of pages for individual ARCHIVE years
soup = BeautifulSoup(requests.get(archiveList).content, features="html.parser")
yearLinks = soup.select(".panel > ul> li > a")  # CSS selector implementation based on SoupSieve
for link in yearLinks:
    if link != None:
        archiveYearsLinks.append("https://www.federalreserve.gov"+link["href"])  # href needs to be called with ["href"], .href does not work

# Scrape HTML links from ARCHIVE year pages and add to data list
print("Scraping links for years older than 5")
for link in tqdm(archiveYearsLinks):
    soup = BeautifulSoup(requests.get(link).content, features="html.parser")
    year = soup.find("h3").get_text()  # not fool proof
    if int(year) < 1993:
        break
    panels = soup.find_all("div", class_="panel")
    for pnl in panels:
        linkTags = pnl.find_all("a")
        link = None
        release = None
        for tag in linkTags:
            if tag["href"].lower().find("minutes") > -1 and tag["href"].lower().find(".htm") > -1:  # That's the right one
                link = tag["href"]
                # Pretty dirty way to extract release date, won't work if keyword "Released" appears twice
                release = tag.parent.parent.get_text(strip=True)
                release = release.split("(Released ")[-1].split(")")[0] if "Release" in release else None
                print(tag.parent.parent.get_text(strip=True))
                break
            else:
                continue
        if link == None or release == None:
            print("Didn't find link containing 'minutes'")
            continue
        release = try_parsing_date(release)
        newEntry = {"year": year, "release": release, "link": "https://www.federalreserve.gov"+link}

        data.append(newEntry)

    print()

# Save data to textfile
pickle.dump(data, open("data/1fomcLinks", "wb"))
