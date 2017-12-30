from selenium import webdriver
import os, time
import re

LOGIN_PAGE = "https://seattleu.instructure.com"
USER_XPATH = "//input[contains(@id,'pseudonym_session_unique_id')]"
PASS_XPATH = "//input[contains(@id,'pseudonym_session_password')]"
LOGIN_XPATH = "//button[contains(@class,'Button--login')]"
SU_USER = os.environ["SU_USER"]
SU_PASS = os.environ["SU_PASS"]

HW_PAGE = "https://seattleu.instructure.com/courses/1573209/assignments/6628791"
PROB_REGEX = r"[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}"
TITLE_XPATH = "//div[contains(@class,'title-content')]"
TEXT_XPATH = "//div[contains(@class,'description user_content student-version')]"


driver = webdriver.Chrome()

driver.get(LOGIN_PAGE)
time.sleep(5)
user_element = driver.find_element_by_xpath(USER_XPATH)
user_element.send_keys(SU_USER)
time.sleep(5)
pass_element = driver.find_element_by_xpath(PASS_XPATH)
pass_element.send_keys(SU_PASS)
time.sleep(5)
login_btn = driver.find_element_by_xpath(LOGIN_XPATH)
login_btn.click()
time.sleep(5)

driver.get(HW_PAGE)
time.sleep(5)
problem_regex = re.compile(PROB_REGEX)
assn_title_el = driver.find_element_by_xpath(TITLE_XPATH)
assn_title = assn_title_el.text
text_body_el = driver.find_element_by_xpath(TEXT_XPATH)
problem_list = problem_regex.findall(text_body_el.text)

driver.quit()

latex_packages = """\\documentclass[10pt]{article}
\\usepackage{amsmath,amsfonts,amsthm,amssymb}
\\usepackage{fancyhdr}
\\usepackage{color}
\\usepackage{graphicx}
\\usepackage{enumerate}"""

latex_title = "\n\\title{"+assn_title+"}"
latex_start = """\n\\author{Joseph Koblitz}
\\begin{document}
\\maketitle
\\date\n\n"""

latex_body = ""
for problem in problem_list:
    latex_body+="\\section{"+problem+"}\n"

latex_end = "\n\n\\end{document}"
fh = open(assn_title.replace(' ','_')+".tex",'w')
fh.write(latex_packages+latex_title+latex_start+latex_body+latex_end)
fh.close()
