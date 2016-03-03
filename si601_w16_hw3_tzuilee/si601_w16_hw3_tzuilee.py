import urllib2
from bs4 import BeautifulSoup
import re, json, time, csv

#Step 1
for i in range(1,5):
	page=50*(i-1)+1
	toPage=page+50-1
	response = urllib2.urlopen('http://www.imdb.com/search/title?at=0&genres=sci_fi&sort=user_rating&start='+str(page)+'&title_type=feature')
	html_doc = response.read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	outfile = open('step1_top_scifi_movies_'+ str(page) +'_to_' + str(toPage)+ '_tzuilee.html', 'w')
	outfile.write(soup.prettify().encode('utf-8'))
	outfile.close()


#Step 2
outfile=open('step2_top_200_scifi_movies_tzuilee.tsv','w')
outfile.write('\t'.join(['Rank', 'IMDB ID', 'Title', 'Year','Rating']) + '\n')
li=[]
for i in range(1,5):
	page=50*(i-1)+1
 	toPage=page+50-1
 	path='step1_top_scifi_movies_'+ str(page) +'_to_' + str(toPage)+ '_tzuilee.html'
	soup = BeautifulSoup(open(path), 'html.parser')
	table=soup.find("table", class_="results")
	for row in table.find_all('tr')[1:]:
		rank=unicode(row.find('td', class_="number").string).strip()[:-1]
		title=unicode(row.find('td', class_='title').find('a').string).strip()
		ID=unicode(row.find('td', class_='title').find('a').get('href')).strip()
		ID=ID.split("/")[2]
		year=unicode(row.find('td', class_='title').find('span', class_='year_type').string).strip()[1:-1]
		rating=unicode(row.find('td', class_='title').find('span', class_='rating-rating').find('span', class_='value').string).strip()
		if len(rating)==0:
			rating=="NA"
		li.append([rank,ID,title,year,rating])
for l in li:
	line = '\t'.join(l) +'\n'
	outfile.write(unicode(line).encode('utf-8'))
outfile.close()	

#Step 3
outfile=open('step3_tzuilee.txt','w')
for item in li:
	imdb_id=item[1]
	url='https://api.themoviedb.org/3/find/'+ imdb_id+'?api_key=78954bfdc25c7cd0d367bdd7bc90a82f&external_source=imdb_id'
	data=json.load(urllib2.urlopen(url))
	time.sleep(5)
	outfile.write(imdb_id +'\t')
	outfile.write(unicode(json.dumps(data)).encode('utf-8')+'\n')

#Step 4
outfile=open('step4_tzuilee.csv','w')
outfile.write('IMDB ID,Title,Year,IMDB Rating,themoviedb Rating\n')
infile =open('step3_tzuilee.txt','rU')
n=0
for line in infile:
  movie=line.split('\t')
  imdb=movie[0]
  json_str=json.loads(movie[1])
  if json_str['movie_results']!=[]:
  	if json_str['movie_results'][0]["vote_average"]!=0:
	  	themoviedbRating=unicode(json_str['movie_results'][0]["vote_average"])
	  	item=li[n][1]+','+li[n][2]+','+li[n][3]+','+li[n][4]+','+themoviedbRating
	  	outfile.write(unicode(item).encode('utf-8')+'\n')
  n+=1	
print n  	
outfile.close()




