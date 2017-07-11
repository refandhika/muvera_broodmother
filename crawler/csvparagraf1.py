import sys
import re
from openpyxl import load_workbook

wb = load_workbook('C:\Users\Nena Saadah Hermawan\Desktop\Python\Work\Appended\media_data_TA_20160627.xlsx', read_only=True)



ws = wb['Sheet1'] # ws is now an IterableWorksheet

reload(sys)
sys.setdefaultencoding('utf8')

regex_formula = re.compile(ur'[^.]+\.')

i = 1

with open('all_paragraf1.csv', 'w') as f:
  for row in ws.rows:
    print str(i)
    i = i + 1
    temp = re.findall(regex_formula,str(row[5].value))
    if len(temp) >= 4:
      f.write(str(temp[0])+str(temp[1])+str(temp[2])+str(temp[3])+'\n')
    elif len(temp) == 3:
      f.write(str(temp[0])+str(temp[1])+str(temp[2])+'\n')
    elif len(temp) == 2:
      f.write(str(temp[0])+str(temp[1])+'\n')
    elif len(temp) == 1:
      f.write(str(temp[0])+"\n")
    else:
      f.write("no quote\n")
