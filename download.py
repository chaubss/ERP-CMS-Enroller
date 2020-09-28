import os
import requests
import urllib.request
from urllib.parse import urlparse
import json 


USER_TOKEN = input("Enter your cms access token: ")
BASE_URL = "https://td.bits-hyderabad.ac.in/moodle/"
USER_ID = None

def scrap_urls(content):
    FILES = []
    #Looping all sections
    for section in content:
        if ("modules" in section):
            modules = section['modules']
        else:
            continue
        for module in modules:
            #Check if module has some attachments
            if "contents" in module and type(module['contents']) is list:
                attachments = module['contents']
                #Loop through each attachment
                for attachment in attachments:
                    if "type" in attachment and attachment["type"] == "file":
                        filename = attachment["filename"]
                        print(filename)
                        file_url = attachment["fileurl"] + "&token=" + USER_TOKEN 
                        FILES.insert(len(FILES), {
                            "filename" : filename,
                            "fileurl" : file_url
                        })
    return FILES

def download_files(files, folder):
    os.makedirs(os.path.join(os.getcwd(), folder))
    print("Downloading files now...")
    i = 1
    for file in files:
        filename = file["filename"]
        fileurl = file["fileurl"]
        urllib.request.urlretrieve(fileurl, os.path.join(os.getcwd(), folder, filename))  
        print("Downloaded", i, "out of", len(files))  
        i = i + 1
                       
# FETCHING USERID
url = BASE_URL +  "webservice/rest/server.php?wsfunction=core_webservice_get_site_info&moodlewsrestformat=json"
params = {
    "wstoken" : USER_TOKEN
}
r = requests.get(url, params = params).json()
USER_ID = r["userid"]

# FETCH ALL COOURSES OF THE USER
url = BASE_URL +  "webservice/rest/server.php?wsfunction=core_enrol_get_users_courses&moodlewsrestformat=json"
params = {
    "wstoken" : USER_TOKEN, 
    "userid" : USER_ID
}
r = requests.get(url, params).json()
courses = r

print("You are enrolled in following courses")
for course in courses :
    print( course["id"], course["shortname"])

COURSE_ID = input("Enter courseid of the course to download, enter `all` to download all courses: ")
COURSES = []
for course in courses:
    if COURSE_ID == "all":
        COURSES.insert(len(COURSES), {
            "courseid" : course["id"],
            "coursename" : course["shortname"]
        })
        continue
    print(COURSE_ID, course["id"])
    if int(COURSE_ID) == int(course["id"]):
        COURSES.insert(len(COURSES), {
            "courseid" : course["id"],
            "coursename" : course["shortname"]
        })
        break
url = BASE_URL + "webservice/rest/server.php?wsfunction=core_course_get_contents&moodlewsrestformat=json"

print(COURSES)
for item in COURSES:    
    courseid = item["courseid"]
    coursename = item["coursename"]
    params = {
        "wstoken" : USER_TOKEN,
        "courseid" : courseid
    }
    r = requests.get(url, params = params).json()
    files = scrap_urls(r)
    download_files(files, coursename)



