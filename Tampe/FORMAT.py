import csv
import re

count= 0
with open("./Tempe AZ- Code Violations.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[3])
        company = company.strip()
        first = re.findall(r"^[^,]+",company)
        for fr in first:
            fr = str(fr)
            company = company.replace(fr,'')
            company = company.strip()
            fr = fr.strip()
            # print(fr)
            # print(company)
            with open('Tempe AZ- Code Violations1.csv','a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i[0],i[1],i[2],i[3],fr,i[4],i[5]])
                count = count + 1
                print("Data saved in CSV: ",count)

