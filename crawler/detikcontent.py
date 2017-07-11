import MySQLdb
import sys
import re

conn = MySQLdb.connect(user='root', passwd='', db='muvera', host='localhost', charset="utf8", use_unicode=True)
cursor = conn.cursor()

cursor.execute("SELECT id,content FROM detik_data")
data = cursor.fetchall()

regex_formula = re.compile(ur'\"[A-Z].+?[\,\.]\".+?\.')

reload(sys)
sys.setdefaultencoding('utf8')

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
		quote1 = "No Quote"
	print id
	cursor.execute("""UPDATE detik_data SET quote1 = %s, quote2 = %s, quote3 = %s, quote4 = %s, quote5 = %s WHERE id = %s""",
		(quote1, quote2, quote3, quote4, quote5, id))
	conn.commit()

cursor.close()

conn.close()

sys.exit()