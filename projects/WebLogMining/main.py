import packages.weblogmining as wlm

base_data_dir = "./data/"
input_file = base_data_dir + 'week.log'
output_file = base_data_dir + 'cleanData.log'

wlm.cleanUpData(input_file, output_file)
