import csv
import re

count= 0
with open("./input2.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[10])
        company = company.strip()
        first = re.findall(r"\s\b(\w+)$",company)
        for fr in first:
            fr = str(fr)
            company = company.replace(fr,'')
            fr = fr.strip()
            # print(fr)
            # print(company)
            with open('input3.csv','a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],company,fr,i[11]])
                count = count + 1
                print("Data saved in CSV: ",count)


            #     for fr in first:
            # fr = str(fr)
            # second = re.findall(r"",fr)
            # print(second)