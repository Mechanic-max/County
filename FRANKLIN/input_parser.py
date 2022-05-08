import re
import csv

count = 0
with open("./input.csv", 'r') as input_file:
        reader = csv.reader(input_file,delimiter=",")
        for i in reader:
            company = str(i[0])
            street_no = re.findall(r"^[^\s]+",company)
            street_Name = re.findall(r"\s\w.*\s",company)
            print(company,street_no,street_Name)
            with open('test.csv','a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow([company,street_no,street_Name])
                count = count + 1
                print("Data saved in CSV: ",count)