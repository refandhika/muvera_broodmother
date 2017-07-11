import MySQLdb
import sys
import re

conn = MySQLdb.connect(user='muverayeah', passwd='lantai4yeah', db='muveradb', host='muverainstance.cuejexbgtlyq.us-east-1.rds.amazonaws.com', port=3306, charset="utf8", use_unicode=True)
cursor = conn.cursor()

regex_formula = re.compile(ur'\"[A-Z].+?[\,\.]+?\".+?\.')

reload(sys)
sys.setdefaultencoding('utf8')

cursor.execute("SELECT id,content FROM antaranews_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE antaranews_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM beritasatu_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE beritasatu_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM cnnindo_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE cnnindo_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM detik_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE detik_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM fajar_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE fajar_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM jakpost_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE jakpost_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM jpnn_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE jpnn_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM kompas_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE kompas_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM liputan6_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE liputan6_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM merdeka_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE merdeka_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM metrotvnews_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE metrotvnews_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM okezone_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE okezone_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM pojoksatu_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE pojoksatu_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM republika_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE republika_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM rimanews_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE rimanews_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM rmol_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE rmol_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM sindonews_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE sindonews_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM suara_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE suara_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM tempo_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE tempo_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM teropongsenayan_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE teropongsenayan_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM tribunnews_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE tribunnews_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.execute("SELECT id,content FROM viva_data WHERE date BETWEEN '2016-06-23 00:00:00' AND '2016-06-27 07:00:00'")
data = cursor.fetchall()

for row in data :
	id = row[0]
	quote1 = ''
	quote2 = ''
	quote3 = ''
	quote4 = ''
	quote5 = ''

	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 5:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
		quote5 = str(temp[4])
	elif len(temp) == 4:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
		quote4 = str(temp[3])
	elif len(temp) == 3:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
		quote3 = str(temp[2])
	elif len(temp) == 2:
		quote1 = str(temp[0])
		quote2 = str(temp[1])
	elif len(temp) == 1:
		quote1 = str(temp[0])
	else:
		quote1 = "no quote"
	print id
	cursor.execute("""UPDATE viva_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.close()

conn.close()

sys.exit()