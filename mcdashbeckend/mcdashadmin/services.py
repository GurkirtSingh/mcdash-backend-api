import PyPDF2 as pdf
import re
from datetime import datetime as dt, timedelta
from django.contrib.auth.models import User
from .dal import get_all_usernames, add_new_shift

# regular expresions
dateRe = re.compile(r'([a-zA-Z]+) (\d{1,2}), (\d{4})')
timeRe = re.compile(r'(\d{1,2}:\d{2} [AP][M])(\d{1,2}:\d{2} [AP][M])')
# nameRe = re.compile(r'(M)([a-zA-Z]+)\s+([a-zA-Z]{1})\s+(\d{3})')
# nameRe = re.compile(r'(M)([a-zA-Z]+)\s{0,5}([a-zA-Z]?)\s{0,5}(\d{0,3})')
nameRe = re.compile(r'([AP]M)([a-zA-Z]+)\s{0,5}([a-zA-Z]{0,3})\s{0,5}([a-zA-Z]{0,3})\s{0,5}(\d{0,3})')

# function - scan_schedule_from_pdf
# file - a pdf file. contains many pages. 
# Each page has mcdonald's shift schedule for the day.
# To scan the pdf using 'PyPDF2' library. 
# search or find regular expresions and extract shift data from pdf.
def scan_schedule_from_pdf(file):
    pdfFile = pdf.PdfFileReader(file)
    usernames = get_all_usernames()
    for i in range(pdfFile.getNumPages()):
        page = pdfFile.getPage(i)
        pageText = page.extractText()
        date = None
        for line in pageText.split('\n'):
           
            if date is None:
                date = dateRe.search(line)
            else:
                time = timeRe.search(line)
                name = nameRe.search(line)
                if name and time:
                    st = dt.strptime(date.group() + time.group(2), '%B %d, %Y%I:%M %p')
                    et = dt.strptime(date.group() + time.group(1), '%B %d, %Y%I:%M %p')
                    if(et < st):
                        et += timedelta(days=1)
                    # db.insertShift(name.group(2), 'Pemberton', st,et, 'N/A')

                    # constructing username
                    # first name
                    username = name.group(2)
                    
                    # if user has a middle name
                    # it should contain 3 character
                    if len(name.group(4)) == 1:
                        if len(name.group(3)) == 3:
                            username += '_' + name.group(3)
                            username += '_' + name.group(4)
                    # if user does not have middle name
                    # last name should only contain 1 character
                    elif len(name.group(3)) >= 1:
                        username += '_' + name.group(3)[0]
                    
                    # if user's employee id is specified
                    # it should contain 3 character                  
                    if len(name.group(5)) == 3:
                        username += '_' + name.group(5)
                    username = username.lower()
                    if username in usernames:
                        add_new_shift(
                            username,
                            st,
                            et,
                            'n/a',
                            'pemberton'
                        )