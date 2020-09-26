import requests
from bs4 import BeautifulSoup


sess = requests.session()

def login_to_erp(username, password):
    login_url = 'https://sis.erp.bits-pilani.ac.in/psp/sisprd/?cmd=login&languageCd=ENG&'
    payload = {'userid': username, 'pwd': password}
    r = sess.post(login_url, data=payload)
    if r.url[-1] == 'T':
        print('Logged in to ERP.')
    else:
        print('Login unsuccessful for ERP.')
        exit()

def get_courses():
    url = 'https://sis.erp.bits-pilani.ac.in/psc/sisprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HC_SSS_STUDENT_CENTER&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL=https%3a%2f%2fsis.erp.bits-pilani.ac.in%2fpsc%2fsisprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentURL=https%3a%2f%2fsis.erp.bits-pilani.ac.in%2fpsc%2fsisprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentProvider=HRMS&PortalCRefLabel=Student%20Center&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fsis.erp.bits-pilani.ac.in%2fpsp%2fsisprd%2f&PortalURI=https%3a%2f%2fsis.erp.bits-pilani.ac.in%2fpsc%2fsisprd%2f&PortalHostNode=HRMS&NoCrumbs=yes&PortalKeyStruct=yes'
    r = sess.get(url)
    pool = BeautifulSoup(r.text, features="html.parser")
    courses = []
    # limit of 100 courses
    for i in range(1, 100):
        try:
            a = pool.find(id = 'trSTDNT_WEEK_SCHD$0_row' + str(i)).contents
            course_name = a[3].contents[1].contents[0].contents[0]
            courses.append(course_name)
        except:
            break
    return courses
        

