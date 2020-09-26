from erp import login_to_erp, get_courses
from cms import get_separated, get_search_results, get_course_to_enroll

uid = input('Enter ERP username: ')
password = input('Enter ERP password: ')
login_to_erp(uid, password)
courses_jum = get_courses()
course_tuples = get_separated(courses_jum)
token = input('Enter Moodle Token: ')
for course_tuple in course_tuples:
    search_results = get_search_results(token, course_tuple)
    get_course_to_enroll(token, search_results, course_tuple)