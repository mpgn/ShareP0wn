import json
import requests
import socket
from requests_ntlm import HttpNtlmAuth
from urlparse import urlsplit

with open('target_url.txt') as target_list:
    urls = target_list.read().splitlines()
with open('path_list.txt') as path_list:
    paths = path_list.read().splitlines()
users = json.load(open("user_list.txt",'r'))

# write the head of the csv file
def head_csv():
    with open('result_sharepwn.csv', 'a') as report:
        report.write('URL,IP,SharePoint,X-SharePointHealthScore,IIS,ASP.NET,' + ','.join(str(p) for p in paths)+"\n")

def write_csv(code):
    with open('result_sharepwn.csv', 'a') as report:
        report.write(str(code))

# get the version of the SharePoint regarding the headers
# for best result, use a valid user: if exist second user is selected otherwise anonymous
def get_infos_target(url):
    infos_headers = []
    #get the IP adress
    ip = socket.gethostbyname(urlsplit(url).netloc)
    infos_headers.append(ip)
    # get the headers
    if len(users['users']) > 1:
        try:
            r = requests.get(url, auth=HttpNtlmAuth(users['users'][1]['username'], users['users'][1]['password']))
        except requests.exceptions.ConnectionError:
            return 0
    else:
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            return 0
    if 'MicrosoftSharePointTeamServices' in r.headers:
        version = r.headers['MicrosoftSharePointTeamServices']
        if int(version[0:2]) == 6:
            version = version + " SP 2003"
        elif int(version[0:2]) == 12:
            version = version + " SP 2007"
        elif int(version[0:2]) == 14:
            version = version + " SP 2010"
        elif int(version[0:2]) == 15:
            version = version + " SP 2013"
        infos_headers.append(version)
        #print "\t SharePoint version", version
    else:
        infos_headers.append('unknow')
        #print "[-] Version of SharePoint not found"
    if 'X-SharePointHealthScore' in r.headers:
        infos_headers.append(r.headers['X-SharePointHealthScore'])
        #print "\t X-SharePointHealthScore", r.headers['X-SharePointHealthScore']
    else:
        infos_headers.append('unknow')
    if 'Server' in r.headers:
        infos_headers.append(r.headers['Server'])
    else:
        infos_headers.append('unknow')
    if 'x-aspnet-version' in r.headers:
        infos_headers.append(r.headers['x-aspnet-version'])
    else:
        infos_headers.append('unknow')
    with open('result_sharepwn.csv', 'a') as report:
        report.write(url + ',' + ','.join(str(p) for p in infos_headers)+',')

    return 1

# get user rights regarding the path
def get_user_right(url,path):
    current_user = ""
    for user in users['users']:
        if user['username'] != "anonymous":
            r = requests.get(url+path, auth=HttpNtlmAuth(user['username'], user['password']))
            if r.status_code == 200 and (r.text.find("SharePointError") == -1):
                print '\t', r.status_code, user['username'], path
                current_user = user['username']
                break;
        else:
            r = requests.get(url+path)
            if r.status_code == 200 and (r.text.find("SharePointError") == -1):
                print '\t', r.status_code, user['username'], path
                current_user = user['username']
                break;
    if len(current_user) > 0:
        write_csv(user['username'] +',')
    else:
        write_csv('nobody,')

print "[+] Writting the header of the CSV"
head_csv()
for url in urls:
    print "[+] Getting information:", url
    if get_infos_target(url):
        print "[+] Checking the path", url
        for path in paths:
            get_user_right(url,path)
        write_csv("OK\n")
    else:
        print "[-] Connexion refused", url
print "[+] Finished, open the CSV and check if there is something to exploit, see README for more"
