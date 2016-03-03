import csv
import re
import urlparse

#First part 
def is_valid(line):
    foo=re.compile('GET|POST|HEAD')
    foo2=re.compile('CONNECT')
    if foo.search(line):
    	reHttp=foo.search(line).group(0)
    	fooHttp=re.compile(reHttp+' http',re.IGNORECASE)
    	if fooHttp.search(line):
    		foo3=re.compile('\"'+foo.search(line).group(0)+' (http.+) .+\" ([2|3|5]\d\d)',re.IGNORECASE)
    		if foo3.search(line):
    			url=foo3.search(line).group(1)
    			query=urlparse.urlparse(url).query
    			each_query=urlparse.parse_qs(query)
    			for key, value in each_query.iteritems():
    				if len(str(value)) >= 80:    			
    					return False
    			return True		
    		else:
    			return False		
        else:	   
        	return False
    elif foo2.search(line):
    	foo3=re.compile('\"'+foo2.search(line).group(0)+'.+\" ([2|3|5]\d\d)')
    	if foo3.search(line):
    		return True
    	else:
    		return False   	 

infile =open('access_log.txt','rU')
validOutput =open('valid_access_log_tzuilee.txt','w')
inValidOutput =open('invalid_access_log_tzuilee.txt','w')

for line in infile:	    	 
    if is_valid(line):
    	validOutput.write(line)
    else:	
        inValidOutput.write(line)

validOutput.close()
inValidOutput.close()   


#Second part
def extract_ip(line):
	foo=re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
	return foo.search(line).group()

infile =open('invalid_access_log_tzuilee.txt','rU')
ips=dict()

for line in infile:
	ip=extract_ip(line)
	if ip in ips:
		ips[ip] +=1
	else:
		ips[ip]=1
tupleList=ips.items()
numbersort=sorted(tupleList, key=lambda word: word[1],reverse=True)			

output = open('suspicious_ip_summary_tzuilee.csv', 'w')
output.write('IP Address,Attempts\n')

for item in numbersort:
    output.write(item[0]+','+str(item[1])+'\n')
output.close()


