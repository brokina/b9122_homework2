import urllib3.util
from bs4 import BeautifulSoup
import urllib.request


def get(url):
    try:
        print("start open "+url)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        return webpage
    except Exception as e:
        return


# Task 1
def task1():
    result = []
    queue = ["https://press.un.org/en"]
    visited = set()
    while len(queue) > 0:
        url = queue.pop(0)
        visited.add(url)
        webpage = get(url)
        if webpage is None:
            continue
        soup = BeautifulSoup(webpage)
        for tag in soup.find_all("a", href=True):
            childUrl = tag['href']
            childUrl = urllib.parse.urljoin(url, childUrl)
            if childUrl not in visited:
                queue.append(childUrl)

        if valid1(webpage):
            with open("task1_result"+str(len(result) + 1)+".html", "w") as f:
                f.write(webpage.decode())
            result.append(url)
            print("valid " + url)
        else:
            print("not valid "+url)

        if len(result) >= 10:
            break

    with open("task1_list.txt", "w") as f:
        for url in result:
            f.write(url+"\n")


def valid1(content):
    soup = BeautifulSoup(content)
    for tag in soup.find_all("a", href=True):
        if tag.text == "Press Release" and \
                tag.attrs['href'] == "/en/press-release" and \
                tag.attrs['hreflang'] == "en":
            return "crisis" in content.decode()
    return False

task1()


# Task 2
def task2():
    current_page = 0
    result = []
    visited = set()
    while len(result) < 10:
        url = "https://www.europarl.europa.eu/news/en/press-room/page/"+str(current_page)
        webpage = get(url)
        soup = BeautifulSoup(webpage)
        for tag in soup.find_all("a", href=True):
            childUrl = tag['href']
            childUrl = urllib.parse.urljoin(url, childUrl)
            if childUrl in visited:
                continue
            visited.add(childUrl)
            content = get(childUrl)
            if valid2(content):
                with open("task2_result"+str(len(result) + 1)+".html", "w") as f:
                    f.write(content.decode())
                result.append(childUrl)
                print("valid " + childUrl)
            else:
                print("not valid "+childUrl)
        current_page += 1
    with open("task2_list.txt", "w") as f:
        for url in result:
            f.write(url+"\n")


def valid2(content):
    soup = BeautifulSoup(content)
    for span in soup.find_all("span"):
        if span.text == "Plenary session" and "ep_name" in span.attrs['class']:
            return "crisis" in content.decode()
    return False


task2()





