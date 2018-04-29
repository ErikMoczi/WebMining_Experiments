import packages.weblogmining as wlm

base_data_dir = "./data/"
input_file = base_data_dir + 'week.log'
output_file = base_data_dir + 'cleanData.log'
stt_q = 151

wlm.clean_up_data(input_file, output_file)
wlm.session_identifier(output_file, stt_q)
