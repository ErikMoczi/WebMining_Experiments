from packages import weblogmining as wlm
from timeit import default_timer as timer

base_data_dir = "./data/"
input_file = base_data_dir + 'week.log'
output_file = base_data_dir + 'cleanweek.log'

start = timer()

wlm.WebLogMining(input_file, output_file)

end = timer()
print(end - start)
