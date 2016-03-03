import json
import sqlite3 as sqlite

#Part 1

infile=open('movie_actors_data.txt','rU')

with sqlite.connect('si601_w16_hw4.db') as con: 
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS movie_genre")
	cur.execute("DROP TABLE IF EXISTS movies")
	cur.execute("DROP TABLE IF EXISTS movie_actor")

	cur.execute("CREATE TABLE movie_genre(imdb_id TEXT, genre TEXT)")
	cur.execute("CREATE TABLE movies(imdb_id TEXT, title TEXT, year INTEGER, rating REAL)")
	cur.execute("CREATE TABLE movie_actor(imdb_id TEXT, actor TEXT)")	

	for line in infile:
	#Step 1	
		data=json.loads(line)
	#Step 2 insert into movie_genre
		if data['genres']!=0:
			for genre in data['genres']:
				# cur.executemany("INSERT INTO movie_genre VALUES (?, ?) ",lot)
				cur.execute("INSERT INTO movie_genre VALUES (?, ?) ",(data['imdb_id'],genre))


	#Step 3 insert into movies
		cur.execute("INSERT INTO movies VALUES (?, ?, ?, ?) ",(data['imdb_id'],data['title'],data['year'],data['rating']))

	#Step 4 insert into movie_actor
		for actor in data['actors']:
			cur.execute("INSERT INTO movie_actor VALUES (?, ?) ",([data['imdb_id'],actor]))
	#Step 5 
	print "Top 10 genres:"
	print "Genre, Movies"
	cur.execute("SELECT genre, COUNT(*) as numbercount FROM movie_genre GROUP BY genre ORDER BY numbercount DESC LIMIT 10 ")
	rows = cur.fetchall()
	for row in rows:
		print str(row[0])+', '+str(row[1])
	print '\n'

	#Step 6
	print "Movies broken down by year:"	
	print "Year, Movies"
	cur.execute("SELECT year, COUNT(*) FROM movies GROUP BY year ORDER BY year")
	rows = cur.fetchall()
	for row in rows:
		print str(row[0])+', '+str(row[1])
	print '\n'

	#Step 7
	print "Sci-Fi movies:"
	print "Title, Year, Rating"	
	cur.execute("SELECT movies.title, movies.year, movies.rating FROM movies JOIN movie_genre ON (movies.imdb_id=movie_genre.imdb_id) WHERE movie_genre.genre='Sci-Fi' ORDER BY movies.rating DESC, movies.year DESC")
	rows = cur.fetchall()
	for row in rows:
		print unicode(row[0])+', '+unicode(row[1])+', '+unicode(row[2])
	print '\n'

	#Step 8 
	print "In and after year 2000, top 10 actors who played in most movies:"
	print "Actor, Movies"
	cur.execute("SELECT movie_actor.actor, COUNT(*) as countnumber FROM movie_actor JOIN movies ON (movies.imdb_id=movie_actor.imdb_id) WHERE movies.year >=2000 GROUP BY movie_actor.actor ORDER BY countnumber DESC,movie_actor.actor LIMIT 10")
	rows = cur.fetchall()
	for row in rows:
		print str(row[0])+', '+str(row[1])	
	print '\n'

	#Step 9
	print"Pairs of actors who co-stared in 3 or more movies:" 
	print"Actor A, Actor B, Co-stared Movies"	

	cur.execute("SELECT DISTINCT a.actor, b.actor, COUNT(a.imdb_id) as countnumber FROM movie_actor a JOIN movie_actor b ON (a.imdb_id=b.imdb_id AND a.actor < b.actor) WHERE a.actor<>b.actor GROUP BY a.actor,b.actor HAVING countnumber >= 3 ORDER BY countnumber DESC, a.actor")
	rows = cur.fetchall()
	for row in rows:
		print unicode(row[0])+', '+unicode(row[1])+', '+unicode(row[2])


		

