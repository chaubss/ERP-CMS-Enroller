from erp import login_to_erp, get_courses
import requests

def separate_course_code(inp):
    vals = inp.split('-')
    return (vals[0].strip(), vals[1].strip())

def check_containment(inp, to_check):
    return to_check[0] in inp and to_check[1] in inp and 'FIRST SEMESTER' in inp

def get_separated(inputs):
    separated = []
    for input in inputs:
        separated.append(separate_course_code(input))
    return separated

def get_search_results(token, course_tuple):
    to_return = []
    keyword = course_tuple[0] + ' ' + course_tuple[1]
    url = 'https://td.bits-hyderabad.ac.in/moodle/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&criterianame=search'
    data = {
        'wstoken': token,
        'criteriavalue': keyword,
        'page': 1
    }
    r = requests.get(url, params = data)
    r = r.json()
    for course in r['courses']:
        course_id = course['id']
        course_name = course['displayname']
        to_return.append((course_id, course_name))
    return to_return

def enroll_in_course(token, course_tuple):
    course_id = course_tuple[0]
    url = 'https://td.bits-hyderabad.ac.in/moodle/webservice/rest/server.php?wsfunction=enrol_self_enrol_user&moodlewsrestformat=json'
    data = {
        'wstoken': token,
        'courseid': course_id
    }
    try:
        r = requests.post(url, data = data).json()
        if r['warnings'][0]['warningcode'] == '1':
            print('Already enrolled in ' + course_tuple[1])
        else:
            print('Successfully enrolled in ' + course_tuple[1])
    except:
        print('Error enrolling in ' + course_tuple[1])

def get_course_to_enroll(token, search_results, course_tuple):
    for result in search_results:
        if check_containment(result[1], course_tuple):
            enroll_in_course(token, result)
            break
