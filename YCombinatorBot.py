from selenium import webdriver

driver = webdriver.Chrome("./chromedriver.exe")

# Defines sort options
def sort_style( by = "Popularity" ):
    sort_options = driver.find_elements_by_class_name("type-dropdown")
    if by != "Popularity":
        for s in sort_options:
            if s.text == "Popularity" or s.text == "Date":
                s.click()
                options = s.find_elements_by_class_name("dropdown-item")
                for op in options:
                    if op.text==by:
                        op.click()
                        break


# Finds and prints all required posts on one page:-
def posts_print(point = 500):
    i = 1
    all_posts = driver.find_elements_by_class_name("item-title-and-infos")
    for post in all_posts:
        hits = post.find_elements_by_class_name("ng-binding")
        points = 0
        for h in hits:
            if "points" in h.text:
                for t in h.text:
                    if t == " ": break
                    points = (points)*10 + int(t)


        title = post.find_elements_by_tag_name("h2")
        if points >= point:
            for x in title: print(str(i) + ". " + x.text)
            i += 1
            print("Points :- " + str(points))
        else:
            print("No more posts with given specs")
            return 1

    return 0
# Navigates from page 1 to given page_no

def page_navigate(total_pages = 5 , points = 500 , sort_by=1):
    pages = 0
    total_pages -= 1
    while pages < total_pages:
        curr_url = driver.current_url
        if sort_by == 1: sort_style()
        elif sort_by == 2: sort_style("Date")
        else :
            print("Wrong choice for sort by , sorting by Popularity")
            sort_style()

        flag = posts_print(points)
        if flag == 1: return
        if curr_url.index(str(pages)) != len(curr_url):
            curr_url = list(curr_url)
            pos = curr_url.index(str(pages))
            pages += 1
            curr_url[pos] = str(pages)

            next_url = ""
            for i in curr_url:
                next_url += i
            driver.get(next_url)

# Main function

def run():
    print("Running customized test")
    search_query = "hackathon"
    tmp_query = input("Enter the keyword to be searched (leave blank for hackathon): ")
    if tmp_query != "": search_query = tmp_query
    driver.get('https://news.ycombinator.com/')
    search_box = driver.find_element_by_tag_name("input")
    search_box.send_keys(search_query)
    search_box.submit()
    try:
        total_pages = int(input("Enter the no of pages to be searched for the keyword (Leave blank for 5): "))
        points = int(input("Enter the minimum no of points(Leave blank for 500):- "))
        sort_by = int(input("Posts by :- \n 1.Popularity \n2. Date :-  "))
        page_navigate(total_pages,points,sort_by)
    except:
        page_navigate()

def automated():
    print("Running fully automated test with posts greater than 500 points and search = 'hackathon' ")
    search_query = "hackathon"
    driver.get('https://news.ycombinator.com/')
    search_box = driver.find_element_by_tag_name("input")
    search_box.send_keys(search_query)
    search_box.submit()
    page_navigate()

# For customizaton , remove the "#" in the next line and put the "#" in front of automated()
#run()

# For full automation
automated()

driver.close()