from collections import Counter
from operator import itemgetter

import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup


def scrap_page(page, list):
    soup = BeautifulSoup(page.content, "lxml")  # lxml faster thant html.parser
    # bleeze 77 hot deal page (infinite scrolling)
    bleeze_soup = soup("span",
                       "cept-merchant-name text--b text--color-greyShade link")
    for merchant in bleeze_soup:
        list += [
            merchant.contents[0]
        ]


merchants = []
for i in range(1, 13):
    url = f"https://www.dealabs.com/profile/Bleezes77/bons-plans?page={i}"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                       "AppleWebKit/537.36 (KHTML, like Gecko)"
                       "Chrome/83.0.4103.116 Safari/537.36")
    }
    page = requests.get(url, headers=headers)
    scrap_page(page, merchants)


print(len(merchants))
counts = Counter(merchants)
counts_plot = sorted(
    counts.items(), key=itemgetter(1)
)  # Sort a list of tuples by 2nd item

plt.style.use("fivethirtyeight")
plt.barh(*zip(*counts_plot))
plt.show()
