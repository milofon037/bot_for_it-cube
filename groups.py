import requests
from bs4 import BeautifulSoup

url = "https://itcube.stavdeti.ru/apply_for_training"


def raspisanie(end_url):
    all_groups = []
    response = requests.get(url + end_url)

    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table")

    al = table.find_all("td")
    for i in range(4, len(al), 4):
        if not '(Основные места закончились, ребёнок будет записан в резерв)' in al[i].text:
            group = (al[i].text.strip(), al[i + 1].text.strip() + ' ' + al[i + 2].text.strip())
            all_groups.append(group)
    return all_groups
