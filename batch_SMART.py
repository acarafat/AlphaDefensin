# SMART Batch Analysis

import mechanize
from bs4 import BeautifulSoup
from time import sleep



br = mechanize.Browser()

def extract_domain(output):
    ### handle output of request
    soup = BeautifulSoup(output)
    viewer_wrap = soup.findAll('div', attrs = {'id':'viewerWrap'})[0]
    domains = str(viewer_wrap).split('smart=')[1].split('+\"')[0].split(':')[1]    
    print domains


def handle_output(output):
    try:
        extract_domain(output)
    except IndexError: 
        jobid = output.split('jobid=')[1].split('\"')[0]
        url = 'http://smart.embl-heidelberg.de/smart/job_status.pl?jobid='+jobid
        response = br.open(url)
        output = response.read()
        extract_domain(output)
        

#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Firefox')] # [('User-agent', 'Firefox')]


# Open a webpage and inspect its contents
response = br.open('http://smart.embl-heidelberg.de/smart/set_mode.cgi?NORMAL=1')

# Form for sequence analysis
br.select_form(nr=1)
#br.form = list(br.forms())[1]

br.form['SEQUENCE'] = 'MKTLVLLSALFLLAFQVQADPIQNTDEETNTEVQPQEEDQAVSVSFGNPEGSDLQEESLRDLGCYCRKRGCTRRERINGTCRKGHLMYTLCCL'

req = br.submit()
output = req.read()
#print output
#br.back()

if 'entered our processing' in output:
    sleep(10)
    jobid = output.split('jobid=')[1].split('\"')[0]
    url = 'http://smart.embl-heidelberg.de/smart/job_status.pl?jobid='+jobid
    response = br.open(url)
    output = response.read()
    extract_domain(output)
else:
    extract_domain(output)
    

    

    