from collections import Counter
from operator import itemgetter
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup


def scrap_page(page, list):
    soup = BeautifulSoup(page.content, "lxml")
    user_soup = soup("span",
                     "cept-merchant-name text--b text--color-greyShade link")
    for merchant in user_soup:
        list += [
            merchant.contents[0]
        ]


user = input("Nom du membre à analyser:")

# Déterminer le nombre de page de deals
###########################################################
url = f"https://www.dealabs.com/profile/{user}/bons-plans?"
headers = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                   "AppleWebKit/537.36 (KHTML, like Gecko)"
                   "Chrome/83.0.4103.116 Safari/537.36")
}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, "lxml")
data_soup = soup("button",
                 "text--color-brandPrimary")
# Transformation en entier et suppression spaces
num_page = int((data_soup[1].string).strip())
###########################################################

# Liste des marchants des deals
###########################################################
merchants = []
for i in range(1, num_page):
    url = f"https://www.dealabs.com/profile/{user}/bons-plans?page={i}"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                       "AppleWebKit/537.36 (KHTML, like Gecko)"
                       "Chrome/83.0.4103.116 Safari/537.36")
    }
    page = requests.get(url, headers=headers)
    scrap_page(page, merchants)
###########################################################


# Création du graphique avec matplotlib
###########################################################
counts = Counter(merchants)
counts_plot = sorted(
    counts.items(), key=itemgetter(1)
)  # Sort a list of tuples by 2nd item
plt.style.use("fivethirtyeight")
plt.barh(*zip(*counts_plot))
plt.show()
###########################################################
