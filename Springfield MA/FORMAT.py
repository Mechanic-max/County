import csv
import re

count= 0
with open("./Springfield MA Acella (01-01-2020 - 04-12-2021) Code Enforcement.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[4])
        company = company.strip()
        comma = re.findall(r"^[^,]+",company)
        for cco in comma:
            cco = str(cco)
            cco = cco.strip()
            # print(cco)
        # first = re.findall(r"^([\w\-]+)",company)
        # last = re.findall(r"\b(\w+)$",company)
        # # fr = ''
        # fe = ''
        # # for fr in first:
        # #     fr = str(fr)
        # #     company = company.replace(fr,'')
        # #     company = company.strip()
        # #     fr = fr.strip()
        # for fe in last:
        #     fe = str(fe)
        #     company = company.replace(fe,'')
        #     company = company.strip()
        # # print("Sttreet No",fr)
        # print("Street Name",company)
        # print("Suffix",fe)
        with open('Springfield MA Acella (01-01-2020 - 04-12-2021) Code Enforcement1.csv','a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i[0],i[1],i[2],i[3],i[4],cco,i[5],i[6]])
            count = count + 1
            print("Data saved in CSV: ",count)

