import csv
import re

count= 0
with open("./Sahuarita AZ Acella (01-01-2020 - 03-23-2021) Code Enforcement.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[5])
        company = company.strip()
        # comma = re.findall(r"^[^,]+",company)
        # for cco in comma:
        #     cco = str(cco)
        #     print(cco)
        first = re.findall(r"^([\w\-]+)",company)
        # last = re.findall(r"\b(\w+)$",company)
        fr = ''
        fe = ''
        for fr in first:
            fr = str(fr)
            company = company.replace(fr,'')
            company = company.strip()
        #     fr = fr.strip()
        # for fe in last:
        #     fe = str(fe)
        #     company = company.replace(fe,'')
        #     company = company.strip()
        # print("Sttreet No",fr)
        # print("Street Name",company)
        # print("Suffix",fe)
        with open('Sahuarita AZ Acella (01-01-2020 - 03-23-2021) Code Enforcement1.csv','a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i[0],i[1],i[2],i[3],i[4],fr,company,i[5]])
            count = count + 1
            print("Data saved in CSV: ",count)

