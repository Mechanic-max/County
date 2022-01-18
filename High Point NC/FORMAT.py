import csv
import re

count= 0
with open("./High Point NC Acella (01-01-2020 - 04-13-2021).csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[5])
        company = company.strip()
        # comma = re.findall(r"^[^,]+",company)
        # for cco in comma:
        #     cco = str(cco)
        #     print(cco)
        first = re.findall(r"^([\w\-]+)",company)
        last = re.findall(r"\b(\w+)$",company)
        fr = ''
        fe = ''
        for fr in first:
            fr = str(fr)
            company = company.replace(fr,'')
            company = company.strip()
            fr = fr.strip()
        for fe in last:
            fe = str(fe)
            company = company.replace(fe,'')
            company = company.strip()
        # print("Sttreet No",fr)
        # print("Street Name",company)
        # print("Suffix",fe)
        with open('High Point NC Acella (01-01-2020 - 04-13-2021)1.csv','a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i[0],i[1],i[2],i[3],i[4],i[5],fr,company,fe,i[6],i[7]])
            count = count + 1
            print("Data saved in CSV: ",count)

