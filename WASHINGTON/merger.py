
import pandas
csv1 = pandas.read_csv('WASHINGTON COUNTY AR 04.06 Approved and Reviewed by Sarah.csv')
csv2 = pandas.read_csv('final_datset_WASHINGTON_AR.csv')
merged = csv1.merge(csv2, on='PropertyNumber')
merged.to_csv("output.csv", index=False)