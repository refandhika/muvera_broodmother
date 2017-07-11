import MySQLdb
import sys
import re

conn = MySQLdb.connect(user='root', passwd='', db='muvera', host='localhost', charset="utf8", use_unicode=True)
cursor = conn.cursor()

cursor.execute("SELECT id,content FROM detik_data")
data = cursor.fetchall()

regex_formula = re.compile(ur'\s*[A-Z].+?\.')

reload(sys)
sys.setdefaultencoding('utf8')

for row in data :
	id = row[0]
	temp = re.findall(regex_formula,str(row[1]))
	if len(temp) >= 4:
		opening = str(temp[0])+str(temp[1])+str(temp[2])+str(temp[3])
	elif len(temp) == 3:
		opening = str(temp[0])+str(temp[1])+str(temp[2])
	elif len(temp) == 2:
		opening = str(temp[0])+str(temp[1])
	elif len(temp) == 1:
		opening = str(temp[0])
	else :
		opening = 'no content'
	print id
	cursor.execute("""UPDATE detik_data SET opening = %s WHERE id = %s""",
		(opening, id))
	conn.commit()

cursor.close()

conn.close()

sys.exit()