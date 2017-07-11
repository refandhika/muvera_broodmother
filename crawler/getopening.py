import MySQLdb
import sys
import re
from datetime import date, timedelta

calc_today = date.today()
today = calc_today.strftime("%Y-%m-%d")
calc_yesterday = date.today() - timedelta(16)
yesterday = calc_yesterday.strftime("%Y-%m-%d")

conn = MySQLdb.connect(user='muverayeah', passwd='lantai4yeah', db='muveradb', host='muverainstance.cuejexbgtlyq.us-east-1.rds.amazonaws.com', port=3306, charset="utf8", use_unicode=True)
cursor = conn.cursor()

opening_formula = re.compile(ur'\s*[A-Z].+?\.')

reload(sys)
sys.setdefaultencoding('utf8')

cursor.execute("SELECT id,content FROM media_data WHERE date BETWEEN %s AND %s", (yesterday, today))
data = cursor.fetchall()

for row in data :
	id = row[0]
	temp = re.findall(opening_formula,str(row[1]))
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
	cursor.execute("""UPDATE media_data SET opening = %s WHERE id = %s""",
		(opening, id))
	conn.commit()

cursor.close()

conn.close()

sys.exit()