import csv
import re

count= 0
with open("./input.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[0])
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
        print("Sttreet No",fr)
        print("Street Name",company)
        print("Suffix",fe)
        with open('Hagerstown WV PIA List of Open Cases 1.1.2020 to 4.29.20211.csv','a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i[0],fr,company,fe])
            count = count + 1
            print("Data saved in CSV: ",count)

