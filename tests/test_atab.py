from apepi import Atab
from os import path

def get_test_file(filename):
    script_dir = path.dirname(__file__)
    return path.join(script_dir,"testdata",filename)

def test_header_atab1():
    file1 = get_test_file("time_scores00_T_2M.dat")
    atab=Atab(file1,sep=" ")
    reference_header={'Number of data columns': ['19'], 'Model name': ['COSMO'], 'Number of data rows': ['48'], 'End time': ['2017-01-13', '2300', '', '+000'], 'Width of text label column': ['0'], 'Number of integer label columns': ['7'], 'Format': 'ATAB', 'Description': ['2m', 'Temperature'], 'Parameter': ['T_2M'], 'Unit': ['degC'], 'Missing value code': ['-0.999900E+09'], 'Model version': ['593@ch'], 'Number of thresholds': ['0']}
    assert(atab.header==reference_header)

def test_data_atab1():
    file1 = get_test_file("time_scores00_T_2M.dat")
    atab=Atab(file1,sep=" ")
    reference_col = [158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158]
    assert(list(atab.data['NMOD'])==reference_col)
    reference_row = [2017.0, 1.0, 12.0, 2.0, 0.0, 0.0, 0.0, 158.0, 146.0, 146.0, -1.1999600000000001, 2.60812, 2.9064700000000001, 3.1352199999999999, -7.6108000000000002, 9.8909000000000002, 0.74934599999999996, 12.507, -1.339, -0.139041, 3.9459900000000001, 4.2297400000000005, -15.058, -13.4, 4.8666999999999998, 6.5]
    assert(list(atab.data.loc[2])==reference_row)

def test_header_atab2():
    file1 = get_test_file("kenda_mean_301_ce.csv")
    atab=Atab(file1)
    reference_header = {'Format': 'XLS_TABLE;1.5', 'Grid_j': ['196'], 'Grid_i': ['1'], 'Missing_value_code': ['-99999.0'], 'Number_of_integer_label_columns': ['2'], 'Experiment': ['301'], 'End_time': ['2017-01-10', '1200', '+000'], 'Width_of_text_label_column': ['-1'], 'Height': ['119.6'], 'Number_of_real_label_columns': ['0'], 'Latitude': ['46.051'], 'Number_of_data_columns': ['8'], 'Number_of_data_rows': ['22'], 'Start_time': ['2016-12-20', '1200', '+000'], 'Indicator': ['ce'], 'Longitude': ['0.148']}
    assert(atab.header==reference_header)


def test_data_atab2():
    file1 = get_test_file("kenda_mean_301_ce.csv")
    atab=Atab(file1)
    reference_col=['112', '0', 'ce', '2.0', '2.0', '2.1', '2.1', '2.0', '2.0', '2.0', '1.9', '1.9', '1.9', '1.9', '1.9', '1.8', '1.8', '1.9', '1.8', '1.8', '1.7', '1.6', '1.7', '1.7', '1.8']
    assert(list(atab.data["W_SO"])==reference_col)
    reference_row=['DATE_TIME', 'LEAD_TIME', 'ce', 'ce', 'ce', 'ce', 'ce', 'ce', 'ce', 'ce', '301']
    assert(list(atab.data.loc[2])==reference_row)
    
