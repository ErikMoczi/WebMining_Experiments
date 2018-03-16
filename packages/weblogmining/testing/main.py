from packages.weblogmining.DataTransformation import *

# testing
base_data_dir = "../../../projects/WebLogMining/data/"
input_file = base_data_dir + 'week.log'
output_file = base_data_dir + 'cleanweek.log'

testing = {}

with open(input_file) as f:
    for line in f:
        out = process_data(line)

for item in testing:
    print(item)
