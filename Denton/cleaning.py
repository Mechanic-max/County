# import csv
# from collections import OrderedDict

# filenames = "DENTON TX -- blk and lot added.csv", "formatted-dataset-Denton.csv"
# data = OrderedDict()
# fieldnames = []
# for filename in filenames:
#     with open(filename, "rb") as fp: # python 2
#         reader = csv.DictReader(fp)
#         fieldnames.extend(reader.fieldnames)
#         for row in reader:
#             data.setdefault(row["Name"], {}).update(row)

# fieldnames = list(OrderedDict.fromkeys(fieldnames))
# with open("merged.csv", "wb") as fp:
#     writer = csv.writer(fp)
#     writer.writerow(fieldnames)
#     for row in data.itervalues():
#         writer.writerow([row.get(field, '') for field in fieldnames])

import pandas

csv1 = pandas.read_csv('formatted-dataset-Denton.csv',low_memory=False)
csv2 = pandas.read_csv('DENTON TX -- blk and lot added.csv',low_memory=False)
merged = csv2.merge(csv1, on='Name')
merged.to_csv("output.csv", index=False)