from bs4 import BeautifulSoup
import requests
import re
import os

def make_page_list():
    lst_of_page = []
    url = "https://codeforces.com/problemset?order=BY_SOLVED_DESC"
    
    # get the html file of URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    for i in soup.find_all("a", href = re.compile("problemset/problem/.*")):
        # original method: lst_of_page.append(re.match("<a href=\"(/problemset/problem/.*)\"",i.text).group(1))
        
        # the above forloop returns another html format file
        # unpack the html file dictionary and extract all "href"
        # access its attributes using item.attrs["attribute"]
        lst_of_page.append(i.attrs["href"])
        # lst_of_page.append(i)

    return lst_of_page[:60:2]

def print_title_to_md(lst=make_page_list()):

    # initiate the fetching process
    count = 1
    for i in lst:
        url = "https://codeforces.com/" + i
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # data fetching

        # get title.text through finding division "problem-statement" and its sub-division "title"
        title = soup.find("div", class_ = "problem-statement").find("div", class_ = "title").get_text()

        # markdown syntax for title-size fonts
        md.write("## " + str(count) + "." + title)
        md.write("\n")
        count += 1

        md.write("\n")
        # get content.text through finding division "problem-statement" and "p"aragraph division and merge them with new line
        contents = soup.find("div", class_ = "problem-statement").find("div", class_= None)
        md.write("".join(i.text + "\n" for i in contents.find_all("p")))
        md.write("\n")
        md.write("\n")


if __name__ == "__main__":
    
    make_page_list()

    # open cf30.md, if NOT exist, create one
    try:
        md = open("cf30.md","w")
    except:
        os.system("touch cf30.md")
        md = open("cf30.md","w")

    print_title_to_md()
    # remove all the "A." thing
    os.system("sed \"s/A\.//\" cf30.md > cf30_substituted.md")
