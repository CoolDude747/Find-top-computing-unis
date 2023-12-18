#libraries
from selenium import webdriver  # general
from webdriver_manager.chrome import ChromeDriverManager  # downloads driver
from selenium.webdriver.common.by import By  # to find elements

from time import sleep

#####   SETUP   #####
installed_driver = ChromeDriverManager().install()  # installs driver
options = webdriver.ChromeOptions()
#options.headless = True
driver = webdriver.Chrome(installed_driver, options=options)
driver.maximize_window()

driver.get("https://www.thecompleteuniversityguide.co.uk/league-tables/rankings/computer-science")
sleep(0.5)
agree_btn = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')  # finds cookies button
driver.execute_script("arguments[0].click();", agree_btn)

sleep(0.5)

###all_info = []  # where all uni info will be stored

def get_info_for_individual(current):
    try:
        print("HELLO")
        uni_rank = driver.find_element(By.XPATH, '//*[@id="lgt_id"]/div[2]/div[2]/div[1]/ul/li[1]/div[' + str(current + 1) + ']/div/span[1]').text

    except:
        uni_rank = ""
        print("ERROR: COULDN'T FIND UNI RANK")
                                                        #'//*[@id="colOne"]/div[1]/div/div[2]/a
    #uni_view_courses_btn = driver.find_element(By.XPATH, '//*[@id="colOne"]/div['+ str(i + 1) +']/a')
    uni_view_courses_btn = driver.find_element(By.XPATH, '//*[@id="colOne"]/div['+ str(current + 1) +']/div/div[2]/a')

    #uni_view_courses_btn.click()
    driver.execute_script("arguments[0].click();", uni_view_courses_btn)  # forces click
    sleep(2)

    curl = driver.current_url
    if "clearing" in curl.split("/"):
        new_url = curl.replace("/clearing", "")
        new_url = new_url.replace("computing-and-it", "computer-science")
        new_url = new_url.replace("/no-results.html", "")
        driver.get(new_url)

    try:
        uni_name = driver.find_element(By.XPATH, '//*[@id="mainBody"]/section/section[1]/section/div/section/div[1]/div[1]/h1/a').text
        print(uni_name)
    except:
        uni_name = ""
        print("ERROR: COULDN'T FIND UNI NAME")

    num_of_courses_unrefined = driver.find_element(By.XPATH, '//*[@id="mainBody"]/section/section[1]/section/div/section/div[1]/div[1]/div/p').text
    num_of_courses = int(num_of_courses_unrefined.split()[0])  # comes in format: "11 courses for Computer Science" need to remove unnecessary stuff

    courses = []

    course_count = 1
    pages = 1  # if click on next page- keep track so know how many times need to go back in website

    for x in range(num_of_courses):
        try:
            driver.find_element(By.XPATH, '//*[@id="okGotItSRandPR"]').click()  # clicks agree button so other buttons can be clicked
        except:
            pass

        if course_count > 10:  # only 10 courses per page
            course_count = 1  # //*[@id="mainBody"]/section/section[2]/div[1]/div/nav[1]/ul/li[3]/a
            pages += 1  # //*[@id="mainBody"]/section/section[2]/div[1]/div/nav[1]/ul/li[5]/a/span
            driver.find_element(By.XPATH, '//*[@id="mainBody"]/section/section[2]/div[1]/div/nav[1]/ul/li[' + str(
                pages + 1) + ']/a').click()  # next page button
            sleep(1.5)

        """
        if course_count > 10:  # only 10 courses per page
            course_count = 1              #//*[@id="mainBody"]/section/section[2]/div[1]/div/nav[1]/ul/li[3]/a
            pages += 1                    #//*[@id="mainBody"]/section/section[2]/div[1]/div/nav[1]/ul/li[5]/a/span
            ###PREVIOUS: driver.find_element(By.XPATH, '//*[@id="mainBody"]/section/section[2]/div[1]/div/nav[1]/ul/li['+ str(pages + 1) +']/a').click()  # next page button
            #driver.find_element('xpath', '//*[@id="mainBody"]/section/section[2]/div[1]/div/nav[1]/ul/li[5]/a').click()
        things = driver.find_elements(By.CLASS_NAME, 'pglt')
        tthings = []
        print(things)
        print(len(things))
        for item in things:
            if item.text == '':
                things.remove(item)

            else:
                tthings.append(item.text)
            #sleep(1.5)


        print("fheksfkj: ")
        print(tthings)
        print(len(tthings))
        print("hirfkwiusfd")
        print(things)
        """

        course_btn = driver.find_element(By.XPATH, '//*[@id="course_count_'+ str(course_count) +'"]/a')
        print("course" + str(x))
        try:
            course_btn.click()  # forgot why this is here- check later
        except:
            print("ERROR: COULDN'T FIND COURSE")

        sleep(1)
        try:
            course_name_unrefined = driver.find_element(By.XPATH, '//*[@id="headSection"]/div[2]/section/div[1]/div[1]/h1').text
            course_name = course_name_unrefined.split("\n")[0]  # remove unnecassry stuff
        except:
            course_name = ""
            print("ERROR: COULDN'T FIND COURSE NAME")

        try:
            entry_requirement_unrefined = driver.find_element(By.XPATH, '//*[@id="subSec_entryReq"]/div[2]/div/div/div[2]/p[1]').text
            entry_requirement = entry_requirement_unrefined.split(": ")[1]  # remove
        except:
            entry_requirement = ""
            print("ERROR: COULDN'T FIND ENTRY REQUIREMENT")

        courses.append([course_name, entry_requirement])  # list of courses and grade requirements
        course_count += 1

        driver.back()  # goes to uni page with all courses

    #individual uni
    uni_info = {
        "rank": uni_rank,
        "courses": courses
    }

    #adds to overall info
    #all_info[uni_name] = uni_info

    ###all_info.append([uni_name, uni_info])

    #for page in range(pages):
    #    driver.back()
    driver.get("https://www.thecompleteuniversityguide.co.uk/league-tables/rankings/computer-science")

    return [uni_name, uni_info]

#//*[@id="colOne"]/div[1]/div/div[2]/a
#//*[@id="colOne"]/div[2]/div/div[2]/a





#l = {
#    "Warwick": {
#        "rating": 5,
#        "courses": [["course 1", "AAA"], ["course 2", "A*AA"]]
#    }
#}

# alternate
# l = [["warwick", {"rating": 5, "courses": [["course 1", "AAA"], ["course 2", "A*AA"]]}]]


#   uni name xpaths
# //*[@id="colOne"]/div[1]/div/a
# //*[@id="colOne"]/div[2]/div/a
# //*[@id="colOne"]/div[3]/div/a


#   uni rank xpath
# //*[@id="lgt_id"]/div[2]/div[2]/div[1]/ul/li[1]/div[1]/div/span[1]
# //*[@id="lgt_id"]/div[2]/div[2]/div[1]/ul/li[1]/div[2]/div/span[1]


#   uni view courses
# //*[@id="colOne"]/div[1]/a
# //*[@id="colOne"]/div[2]/a


#   uni view course/title
# //*[@id="mainBody"]/section/section[1]/section/div/section/div[1]/div[1]/h1/a
# //*[@id="mainBody"]/section/section[1]/section/div/section/div[1]/div[1]/h1/a


#   course options
# //*[@id="course_count_1"]/a
# //*[@id="course_count_2"]/a


#   view courses 2
# //*[@id="colOne"]/div[1]/a/span
# //*[@id="colOne"]/div[2]/a/span


#   in clearing vs normal
# https://www.thecompleteuniversityguide.co.uk/courses/university-search/undergraduate/computer-science/university-of-bath
# https://www.thecompleteuniversityguide.co.uk/clearing/courses/university-search/undergraduate/computing-and-it/university-of-bath/no-results.html

#   next page btn
#//*[@id="mainBody"]/section/section[2]/div[1]/div/nav[1]/ul/li[5]/a
#//*[@id="mainBody"]/section/section[2]/div[1]/div/nav[1]/ul/li[5]/a