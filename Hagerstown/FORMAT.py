import csv
import re

count= 0
with open("./Hagerstown WV PIA List of Open Cases 1.1.2020 to 4.29.2021.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company1 = str(i[3])
        company1 = company1.strip()
        company2 = str(i[4])
        company2 = company2.strip()
        company3 = str(i[5])
        company3 = company3.strip()
        ste = f"{company1} {company2} {company3}"
        ste = ste.strip()
        # print(ste)
        # comma = re.findall(r"^[^,]+",company)
        # for cco in comma:
        #     cco = str(cco)
        #     print(cco)
        # first = re.findall(r"^([\w\-]+)",company)
        # last = re.findall(r"\b(\w+)$",company)
        # fr = ''
        # fe = ''
        # for fr in first:
        #     fr = str(fr)
        #     company = company.replace(fr,'')
        #     company = company.strip()
        #     fr = fr.strip()
        # for fe in last:
        #     fe = str(fe)
        #     company = company.replace(fe,'')
        #     company = company.strip()
        # print("Sttreet No",fr)
        # print("Street Name",company)
        # print("Suffix",fe)
        with open('Hagerstown WV PIA List of Open Cases 1.1.2020 to 4.29.20211.csv','a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i[0],i[1],i[2],i[3],i[4],i[5],i[6],ste])
            count = count + 1
            print("Data saved in CSV: ",count)

