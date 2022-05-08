import csv
import re

count= 0
with open("./input.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[0])
        company = company.strip()
        first = re.findall(r"^[^,]+",company)
        for fr in first:
            fr = str(fr)
            # company = company.replace(fr,'')
            # company = company.strip()
            fr = fr.strip()
            # print(fr)
            # print(company)
            with open('input1.csv','a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i[0],fr])
                count = count + 1
                print("Data saved in CSV: ",count)

