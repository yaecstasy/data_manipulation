import json
import sqlite3 as sqlite
import sys

def printGenre(genre,numberList):
	number=int(numberList)
	with sqlite.connect('si601_w16_hw4.db') as con: 
		cur = con.cursor()
		cur.execute("SELECT movie_actor.actor, COUNT(*) as Numbercount FROM movie_actor JOIN movies ON (movie_actor.imdb_id=movies.imdb_id) JOIN movie_genre ON (movie_genre.imdb_id=movies.imdb_id) WHERE movie_genre.genre=(?) GROUP BY movie_actor.actor ORDER BY Numbercount DESC LIMIT (?) ",(genre,number))
		rows = cur.fetchall()
		for row in rows:
			print unicode(row[0])+', '+unicode(row[1])

print "Top " +sys.argv[2]+ " actors who played in most Drama movies:"
print "Actor, "+sys.argv[1] +"Movies Played in"
printGenre(sys.argv[1],sys.argv[2])			