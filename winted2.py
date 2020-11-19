import os
import csv 
import sys 
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winted5.settings')
django.setup()

from company.models import *
from user.models import *

CSV_PATH_PRODUCTS= 'win.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:

        # if row[0]:
        #     print(row[0])
        #     Tag.objects.create(name=row[0])

        # if row[1] :
        #     a1=Tag.objects.get(id=row[2])
        #     Sub_tag.objects.create(name=row[1],tag=a1)

        # if row[3] and row[4] :
        #     Maincategory.objects.create(name=row[3],image_url=row[4])

        # if row[6] :
        #     a2= Maincategory.objects.get (id= row[5])
        #     Subcategory.objects.create(maincategories=a2 , name=row[6] , image_url= row[7])

        # if row[8] :
        #     District_category.objects.create(name=row[8])

        # if row[10] and row[11] :
        #     a3=District_category.objects.get(id=row[12])
        #     District.objects.create(district_categories=a3 , name= row[11])
        
        # if row [13]:
        #     Carrer.objects.create(carrer=row[13])

        # if row [14] and row [15]:
        #     Money.objects.create(recommend=row[14],applicant=row[15])
        
        # company=row[17]
        # title = row[18]
        # contens= row[20]
        # image=row[22]
        # deadline=row[23]

        # district = row[25]
        # compensetion = row[26]
        # subcategory = row[27]
        # carrer = row [28]
        # tag = row [31]

        # if row[17] and row[18]:
        #     asd2 =District.objects.get(id=row[25])
        #     asd3=Money.objects.get(id=row[26])
        #     asd4=Subcategory.objects.get(id=row[27])
        #     asd5= Carrer.objects.get(id=row[28])
        #     asd6= Sub_tag.objects.get(id=row[31])
        #     Company.objects.create(name=company,title=title,contens=contens,image_url=image,dead_line=deadline,district=asd2,money=asd3,subcategories=asd4,carrer=asd5,sub_tag=asd6)

        # main=Maincategory.objects.get(id=row[33])
        # sub= Subcategory.objects.get(id=row[34])
        # carrer =Carrer.objects.get(id=row[35])
        # salary = row[36]

        # if row[33] and row[34]:
        #     Salary.objects.create(maincategories=main , subcategories=sub , carrer=carrer , salary=salary)  


            
                    

  
                            
            
                    