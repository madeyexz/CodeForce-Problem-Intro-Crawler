from bs4 import BeautifulSoup
import requests
import re
import os

def make_page_list():
    lst_of_page = []
    url = "https://codeforces.com/problemset?order=BY_SOLVED_DESC"
    
    # get the html file of URL
    response = requests.get(url)

    # search directly in the html.text file using regex
    for i in re.findall("problemset/problem/\d*/\w*", response.text):
        lst_of_page.append(i)
    
    # limit the quantitiy of problems to 30 problems
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

        # markdown syntax for paragraph division
        md.write("---")
        md.write("\n")
        # get content.text through finding division "problem-statement" and "p"aragraph division and merge them with new line
        contents = soup.find("div", class_ = "problem-statement").find("div", class_ = None)
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
    os.system("sed \"s/A\.//\" cf30.md > cf_crawled.md")