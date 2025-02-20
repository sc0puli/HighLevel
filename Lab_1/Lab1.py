import re
import numpy as np

class Table:
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

def lib_parser(path, name):
    tables = []
    curr_table = ''

    flag_sit = 0
    flag_coc = 0
    flag_inner_cap = 0
    flag_cf = 0
    flag_cr = 0
    flag_ft = 0
    flag_rt = 0

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
                for cell in tables:
                    if cell.name == curr_table:
                        cell.inner_cap = float(line)

                flag_inner_cap = 0

            if flag_cf:
                cf = []
                for i in range(tables[0].tr_time.size):
                    cf.append(np.array(line.replace("\n", "").split(","), dtype='float'))
                    line = next(infile)

                for cell in tables:
                    if cell.name == curr_table:
                        cell.cell_fall = np.vstack(cf)

                flag_cf = 0

            if flag_cr:
                cr = []
                for i in range(tables[0].tr_time.size):
                    cr.append(np.array(line.replace("\n", "").split(","), dtype='float'))
                    line = next(infile)

                for cell in tables:
                    if cell.name == curr_table:
                        cell.cell_rise = np.vstack(cr)

                flag_cr = 0

            if flag_ft:
                ft = []
                for i in range(tables[0].tr_time.size):
                    ft.append(np.array(line.replace("\n", "").split(","), dtype='float'))
                    line = next(infile)

                for cell in tables:
                    if cell.name == curr_table:
                        cell.fall_tr = np.vstack(ft)

                flag_ft = 0

            if flag_rt:
                rt = []
                for i in range(tables[0].tr_time.size):
                    rt.append(np.array(line.replace("\n", "").split(","), dtype='float'))
                    line = next(infile)

                for cell in tables:
                    if cell.name == curr_table:
                        cell.rise_tr = np.vstack(rt)

                flag_rt = 0

            #flag catching
            if re.match("string_input_transtion", line):
                flag_sit = 1
            elif re.match("column_output_capacitance", line):
                flag_coc = 1
            elif re.match("capacitance", line):
                flag_inner_cap = 1
            elif re.match("cell_fall", line):
                flag_cf = 1
            elif re.match("cell_rise", line):
                flag_cr = 1
            elif re.match("fall_transition", line):
                flag_ft = 1
            elif re.match("rise_transition", line):
                flag_rt = 1
            elif re.match('AND|NAND|NOR|OR|XOR|XNOR|BUF|INV', line):
                tables.append(Table(line.replace('\n',''), sit_np, coc_np))
                curr_table = line.replace('\n','')

    for table in tables:
        if table.name == name:
            return table

def find_round(table: Table, t_rise: float, c_out: float):
    found_time, cap_found = False, False
    t_index = 0
    c_index = 0

    for i, time in enumerate(table.tr_time):
        if time == t_rise:
            t_index = i
            found_time = True

    for i, cap in enumerate(table.output_cap):
        if cap == c_out:
            c_index = i
            cap_found = True

    # print(found_time, cap_found)
    # print(t_index, c_index)
    if found_time and cap_found:
        print(f'For element {table.name} and tr_inp {t_rise}, cap_out {c_out} was found tr_out {table.cell_rise[t_index][c_index]}\n')


if __name__ == '__main__':
    lib_table = lib_parser('lab1.lib', 'INV')
    find_round(lib_table, t_rise=0.4, c_out=0.4)
