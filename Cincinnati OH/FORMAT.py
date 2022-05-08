import csv
import re

count= 0
with open("./input.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[1])
        company = company.strip()
        first = re.findall(r"^([\w\-]+)",company)
        fr = ''
        for fr in first:
            fr = str(fr)
            company = company.replace(fr,'')
            company = company.strip()
            fr = fr.strip()

        # print("Street No",fr)
        # print("Street Name",company)

        with open('input1.csv','a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i[0],i[1],fr,company,i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22]])
            count = count + 1
            print("Data saved in CSV: ",count)

