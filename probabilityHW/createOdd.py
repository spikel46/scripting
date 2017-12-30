import os, sys
import re

assn = sys.argv[1]
assn_title = assn.split('.')[0]
numProbs = 75

FILEPARSE_RE = r"ch([\d]{1,2})-([\d]{1,2})\.tex"
result = re.match(FILEPARSE_RE, assn)

if(not result):
    print ("byeeeeee")
    exit()

chapter = result[1]
section = result[2]

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
for i in range(1,numProbs,2):
    latex_body+="\\section{"+str(chapter)+"."+str(section)+"."+str(i)+"}\n"

latex_end = "\n\n\\end{document}"
fh = open(assn,'w')
fh.write(latex_packages+latex_title+latex_start+latex_body+latex_end)
fh.close()
