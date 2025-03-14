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

def find_round(table: Table, t_rise: float, c_out: float, edge: str):
    found_time_exact, cap_found_exact = False, False
    t_index, c_index = 0, 0
    init_t_r, init_c_out = t_rise, c_out

    for i, time in enumerate(table.tr_time):
        if time == t_rise:
            t_index = i
            found_time_exact = True

    for i, cap in enumerate(table.output_cap):
        if cap == c_out:
            c_index = i
            cap_found_exact = True

    if not found_time_exact:
        i = 0
        while t_rise > table.tr_time[i]:
            i += 1
        t_index = i
        t_rise = table.output_cap[i]


    if not cap_found_exact:
        i = 0
        while c_out > table.output_cap[i]:
            i += 1
        c_index = i
        c_out = table.output_cap[i]

    # print(t_index, c_index)

    if edge == 'posedge':
        lut = table.cell_rise
    elif edge == 'negedge':
        lut = table.cell_fall
    else:
        print("[ERROR] Wrong edge type!")
        return -1

    if found_time_exact and cap_found_exact:
        print(f'For element {table.name} and tr_inp {t_rise}, cap_out {c_out} was found exact tr_out {lut[t_index][c_index]}\n')
    else:
        print(f"For element {table.name} was not found exact value!\ntr_inp {init_t_r} was rounded to {t_rise}\ncap_out {init_c_out} was rounded to {c_out}\nFor rounded values was found tr_out {lut[t_index][c_index]}\n")

def interpolate(x, x1, x2, q11, q21):
    return ((x2 - x)/(x2 - x1)) * q11 + ((x-x1)/(x2-x1)) * q21

def find_interpolate(table: Table, t_rise: float, c_out: float, edge: str):
    if edge == 'posedge':
        lut = table.cell_rise
    elif edge == 'negedge':
        lut = table.cell_fall
    else:
        print("[ERROR] Wrong edge type!")
        return 1

    i = 0
    while t_rise > table.tr_time[i]:
        i += 1
    t_left = table.tr_time[i - 1]
    t_right = table.tr_time[i]

    j = 0
    while c_out > table.output_cap[j]:
        j += 1
    c_left = table.output_cap[j - 1]
    c_right = table.output_cap[j]

    Q11, Q12, Q21, Q22 = lut[i - 1][j - 1], lut[i - 1][j], lut[i][j - 1], lut[i][j]
    print(Q11, Q12, Q21, Q22)
    f1 = interpolate(c_out, c_left, c_right, Q11, Q21)
    print(f1)
    f2 = interpolate(c_out, c_left, c_right, Q12, Q22)
    print(f2)
    f3 = interpolate(t_rise, t_left, t_right, f1, f2)

    print(f'For element {table.name} and tr_inp {t_rise}, cap_out {c_out} was interpolated tr_out {f3}\n')

    return f3

if __name__ == '__main__':
    lib_table = lib_parser('lab1.lib', 'AND')
    find_round(lib_table, t_rise=0.62, c_out=1.6, edge='posedge')
    find_interpolate(lib_table, t_rise=0.62, c_out=1.6, edge='posedge')
