import sys, re
import simplejson as json
from pyspark import SparkContext

sc = SparkContext(appName="PythonBigram")
input_file = sc.textFile("hdfs:///user/yuhangw/yelp_academic_dataset.json")

def cat_hi(data):
  cat_bussiness_list = []
  stars = data.get('stars', None)
  city=data.get('city',None)
  review_count=data.get('review_count',None)
  neighborhoods = data.get('neighborhoods', None)
  if neighborhoods:
  	for neighborhood in neighborhoods:  		
  		cat_bussiness_list.append(((city,neighborhood),(review_count,stars,1)))
  else:
  	neighborhood="Unknown"
  	cat_bussiness_list.append(((city,neighborhood),(review_count,stars,1)))
  return cat_bussiness_list

if len(sys.argv) < 2:
  print "need to provide input and output dir"
else:
  outputdir = sys.argv[1]  

cat_bussiness = input_file.map(lambda line: json.loads(line))\
					  .filter(lambda x : x.get('type', '') == 'business')\
                      .flatMap(cat_hi)\
                      .reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2]+y[2]))\
                      .mapValues(lambda x: (x[2],x[0], x[1]/x[2]))\
					            .map(lambda t:(t[0][0],t[0][1], t[1][0], t[1][1],t[1][2]))\
             		      .sortBy(lambda x: (x[0],x[2]*-1), ascending = True, numPartitions=1)
                      
cat_bussiness.map(lambda t : t[0] + '\t' + t[1]+ '\t' +str(t[2])+'\t'+ str(t[3])+'\t'+ str(t[4])).repartition(1).saveAsTextFile(outputdir)
