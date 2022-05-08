import csv
import re

count= 0
with open("./input1.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[7])
        company = company.strip()
        first = re.findall(r"^([\w\-]+)",company)
        for fr in first:
            fr = str(fr)
            company = company.replace(fr,'')
            company = company.strip()
            fr = fr.strip()
            # print(fr)
            # print(company)
            with open('input2.csv','a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],fr,company])
                count = count + 1
                print("Data saved in CSV: ",count)

