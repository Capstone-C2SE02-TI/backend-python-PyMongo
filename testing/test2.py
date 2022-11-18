import requests
import pandas as pd
import re
CLEANR = re.compile('<.*?>') 


f = open("demofile2.txt", "r",encoding='utf-8')

headCol = ['Category','StoreName','Title','Detail','SalePrice','Q1', 'PercentPrice', 'Q2', 'RawPrice', 'Link', 'Date', 'Time', 'Q3']

Category  = []
StoreName  = []
Title  = []
Detail  = []
SalePrice  = []
Q1  = []
PercentPrice  = []
Q2  = []
RawPrice  = []
Link  = []
Date  = []
Time  = []
Q3  = []

obj = re.sub(CLEANR,'',f.read())

f1 = open("demofile3.txt", "a",encoding='utf-8')
f1.write(obj)

# for ob in obj[100:102]:
#     storeName = ob.split('</td>')[0]
#     rest = ob.split('</td>')


#     for i in range(0,len(rest)):
#         rest[i] = (rest[i].replace('<td class="s6" dir="ltr">', '').replace('<td class="s8" dir="ltr">','')
#         .replace('<td class="s9 softmerge" dir="ltr"><div class="softmerge-inner" style="width:506px;left:-3px">','')
#         .replace('</div>','')
#         .replace('<td class="s10 softmerge" dir="ltr"><div class="softmerge-inner" style="width:104px;left:-1px">','')
#         .replace('<td class="s11"><a target="_blank" rel="noreferrer" href="','')
#         .replace('>https://j2team.dev/deal/436782-16067972093</a>','')
#         .replace('/tr><tr style="height: 20px"><th id="1061352006R2" style="height: 20px;" class="row-headers-background"><div class="row-header-wrapper" style="line-height: 20px">3</th><td class="s5" dir="ltr">','')
#         .replace('<td class="s16 softmerge" dir="ltr"><div class="softmerge-inner" style="width:160px;left:-1px">','')
#         )
#     try:
#         Category.append(rest[0])    
#         StoreName.append(rest[1])   
#         Title.append(rest[2])       
#         Detail.append(rest[3])      
#         SalePrice.append(rest[4])   
#         Q1.append(rest[5])
#         PercentPrice.append(rest[6])
#         Q2.append(rest[7])
#         RawPrice.append(rest[8])    
#         Link.append(rest[9])        
#         Date.append(rest[10])       
#         Time.append(rest[11])       
#         Q3.append(rest[12])
#     except:
#         continue

# df = pd.DataFrame({
#     'Category': Category,
#     'StoreName': StoreName,
#     'Title': Title,
#     'Detail': Detail,
#     'SalePrice': SalePrice,
#     'Q1': Q1,
#     'PercentPrice': PercentPrice,
#     'Q2': Q2,
#     'RawPrice': RawPrice,
#     'Link': Link,
#     'Date': Date,
#     'Time': Time,
#     'Q3': Q3
# })

# df.to_excel('D:/Coding/test.xlsx')
