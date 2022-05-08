# import csv
# from collections import OrderedDict

# filenames = "dataset_for_travis.csv", "TRAVIS TX 21- SarahNew.csv"
# data = OrderedDict()
# fieldnames = []
# for filename in filenames:
#     with open(filename, "rb") as fp: # python 2
#         reader = csv.DictReader(fp)
#         fieldnames.extend(reader.fieldnames)
#         for row in reader:
#             data.setdefault(row["Folio"], {}).update(row)

# fieldnames = list(OrderedDict.fromkeys(fieldnames))
# with open("merged.csv", "wb") as fp:
#     writer = csv.writer(fp)
#     writer.writerow(fieldnames)
#     for row in data.itervalues():
#         writer.writerow([row.get(field, '') for field in fieldnames])


import pandas

csv1 = pandas.read_csv('TRAVIS TX 21- SarahNew.csv')
csv2 = pandas.read_csv('dataset_for_travis.csv')
merged = csv1.merge(csv2, on='Folio')
merged.to_csv("output.csv", index=False)