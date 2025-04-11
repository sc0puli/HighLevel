import re
import numpy as np


class Table:
    '''
    Класс для хранения NLDM таблицы
    '''
    def __init__(self, _name, _tr_time, _output_cap):
        #create table after cell name
        self.name = _name
        self.tr_time = _tr_time
        self.output_cap = _output_cap
        #leave to fill while parsing till next cell name
        self.inner_cap = 0
        self.cell_fall = []
        self.cell_rise = []
        self.fall_tr = []
        self.rise_tr = []


def lib_parser(name, path):
    curr_table = ''
    flag_sit = 0
    flag_coc = 0
    flag_inner_cap = 0
    flag_cf = 0
    flag_cr = 0
    flag_ft = 0
    flag_rt = 0
    flag_name = 0

    with open(path, 'r', encoding='utf-8') as infile:
        for line in infile:
            #flag handling
            if flag_sit:
                # print(line)
                sit_np = np.array(line.replace("\n", "").split(","), dtype='float')
                flag_sit = 0
            if flag_coc:
                # print(line)
                coc_np = np.array(line.replace("\n", "").split(","), dtype='float')
                flag_coc = 0
            if flag_inner_cap:
                # print(line)
                curr_table.inner_cap = float(line)
                flag_inner_cap = 0

            if flag_cf:
                cf = []
                for i in range(curr_table.tr_time.size):
                    cf.append(np.array(line.replace("\n", "").split(","), dtype='float'))
                    line = next(infile)
                curr_table.cell_fall = np.vstack(cf)
                flag_cf = 0

            if flag_cr:
                cr = []
                for i in range(curr_table.tr_time.size):
                    cr.append(np.array(line.replace("\n", "").split(","), dtype='float'))
                    line = next(infile)
                curr_table.cell_rise = np.vstack(cr)
                flag_cr = 0

            if flag_ft:
                ft = []
                for i in range(curr_table.tr_time.size):
                    ft.append(np.array(line.replace("\n", "").split(","), dtype='float'))
                    line = next(infile)
                curr_table.fall_tr = np.vstack(ft)
                flag_ft = 0

            if flag_rt:
                rt = []
                for i in range(curr_table.tr_time.size):
                    rt.append(np.array(line.replace("\n", "").split(","), dtype='float'))
                    line = next(infile)
                curr_table.rise_tr = np.vstack(rt)
                flag_rt = 0
                break

            #flag catching
            if re.match("string_input_transition", line):
                flag_sit = 1
            elif re.match("column_output_capacitance", line):
                flag_coc = 1
            elif re.match("capacitance", line) and flag_name:
                flag_inner_cap = 1
            elif re.match("cell_fall", line) and flag_name:
                flag_cf = 1
            elif re.match("cell_rise", line) and flag_name:
                flag_cr = 1
            elif re.match("fall_transition", line) and flag_name:
                flag_ft = 1
            elif re.match("rise_transition", line) and flag_name:
                flag_rt = 1
            elif re.match(name, line):
                flag_name = 1
                curr_table = Table(line.replace('\n', ''), sit_np, coc_np)

    flag_name = 0
    return curr_table