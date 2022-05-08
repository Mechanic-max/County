import csv
import re

with open("./te.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        company = str(company)
        land = re.findall(r"\bLOT\b\s\d*",company)
        block = re.findall(r"\bBLOCK\b\s\d*",company)
        with open('ober.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([company,land,block])