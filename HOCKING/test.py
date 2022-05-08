import csv
count = 0
with open("./input_1.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        count  = count+1
        ct = f"0{company}   {count}"
        print(ct)