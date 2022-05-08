import csv
import re

count= 0
with open("./mckinney TX 01-01-2020 - 04-20-2021.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[0])
        company = company.strip()
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
        # print("Street No",fr)
        # print("Street Name",company)
        # print("Suffix",fe)

        with open('./mckinney TX 01-01-2020 - 04-20-20211.csv','a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i[0],fr,company,fe,i[1],i[2],i[3],i[4],i[5],i[6]])
            count = count + 1
            print("Data saved in CSV: ",count)

