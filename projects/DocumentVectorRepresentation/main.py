import pandas as pd
import treetagger
import docanalysis

base_data_dir = "./data/"
documents_dir = base_data_dir + "documents/"
tagger_dir = base_data_dir + "taggs/"
out_put_file_name = base_data_dir + "vektorova_reprezentacia.xlsx"

treetagger.Lematization(documents_dir, tagger_dir)
out = docanalysis.Analysis(tagger_dir)

writer = pd.ExcelWriter(out_put_file_name, engine='xlsxwriter')
pd.DataFrame(out.data).to_excel(writer, sheet_name='data')
pd.DataFrame(out.binary_freq).to_excel(writer, sheet_name='BinarnaFrekvencia')
pd.DataFrame(out.log_freq).to_excel(writer, sheet_name='LogaritmickaFrekvencia')
pd.DataFrame(out.inverse_freq).to_excel(writer, sheet_name='InverznaFrekvencia')
writer.save()
