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


def lib_parser(path, name):
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
            elif re.match(name, line):
                curr_table = Table(line.replace('\n', ''), sit_np, coc_np)

    return curr_table


def get_value_rounded(table: Table, t_rise: float, c_out: float, edge: str, to_get: str= 'delay'):
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
        t_rise = table.tr_time[i]


    if not cap_found_exact:
        i = 0
        while c_out > table.output_cap[i]:
            i += 1
        c_index = i
        c_out = table.output_cap[i]

    # print(t_index, c_index)

    if to_get == 'delay':
        if edge == 'posedge':
            lut = table.cell_rise
        elif edge == 'negedge':
            lut = table.cell_fall
        else:
            raise ValueError("[ERROR] Wrong edge type!")
    elif to_get == 'transition':
        if edge == 'posedge':
            lut = table.rise_tr
        elif edge == 'negedge':
            lut = table.fall_tr
        else:
            raise ValueError("[ERROR] Wrong edge type!")
    else:
        raise ValueError("[ERROR] Wrong type!")
    # if found_time_exact and cap_found_exact:
    #     print(f'For element {table.name} and tr_inp {t_rise}, cap_out {c_out} was found exact tr_out {lut[t_index][c_index]}\n')
    # else:
    #     print(f"For element {table.name} was not found exact value!\ntr_inp {init_t_r} was rounded to {t_rise}\ncap_out {init_c_out} was rounded to {c_out}\nFor rounded values was found tr_out {lut[t_index][c_index]}\n")

    return lut[t_index][c_index]

def get_value_interpolated(table: Table, t_rise: float, c_out: float, edge: str, to_get: str='delay'):
    if to_get == 'delay':
        if edge == 'posedge':
            lut = table.cell_rise
        elif edge == 'negedge':
            lut = table.cell_fall
        else:
            raise ValueError("[ERROR] Wrong edge type!")
    elif to_get == 'transition':
        if edge == 'posedge':
            lut = table.rise_tr
        elif edge == 'negedge':
            lut = table.fall_tr
        else:
            raise ValueError("[ERROR] Wrong edge type!")
    else:
        raise ValueError("[ERROR] Wrong type!")

    tr1 = max([x for x in table.tr_time if x <= t_rise])
    tr2 = min([x for x in table.tr_time if x >= t_rise])
    cap1 = max([x for x in table.output_cap if x <= c_out])
    cap2 = min([x for x in table.output_cap if x >= c_out])

    tr1_idx = np.where(table.tr_time == tr1)
    tr2_idx = np.where(table.tr_time == tr2)
    cap1_idx = np.where(table.output_cap == cap1)
    cap2_idx = np.where(table.output_cap == cap2)

    # print(tr1_idx, tr2_idx, cap1_idx, cap2_idx)

    q11 = lut[tr1_idx[0][0]][cap1_idx[0][0]]
    q12 = lut[tr1_idx[0][0]][cap2_idx[0][0]]
    q21 = lut[tr2_idx[0][0]][cap1_idx[0][0]]
    q22 = lut[tr2_idx[0][0]][cap2_idx[0][0]]

    if cap1 != cap2:
        f_r1 = (cap2 - c_out) / (cap2 - cap1) * q11 + (c_out - cap1) / (cap2 - cap1) * q21
        f_r2 = (cap2 - c_out) / (cap2 - cap1) * q12 + (c_out - cap1) / (cap2 - cap1) * q22
    else:
        f_r1 = q11
        f_r2 = q12

    if tr1 != tr2:
        delay = (tr2 - t_rise) / (tr2 - tr1) * f_r1 + (t_rise - tr1) / (tr2 - tr1) * f_r2
    else:
        delay = f_r1

    return delay


class Gate:
    '''
    Класс для обработки логических вентилей
    '''
    def __init__(self, name: str, path: str = 'lab1.lib'):
        self.name = name
        self.table = lib_parser(path, name)

    def get_delay(self, edge, tr_in, c_out, method):
        if method == 'rounded':
            return get_value_rounded(self.table, tr_in, c_out, edge)
        elif method == 'interpolated':
            return get_value_interpolated(self.table, tr_in, c_out, edge)
        else:
            raise ValueError("[ERROR] Wrong method!")

    def get_transition(self, edge, tr_in, c_out, method):
        if method == 'rounded':
            return get_value_rounded(self.table, tr_in, c_out, edge, 'transition')
        elif method == 'interpolated':
            return get_value_interpolated(self.table, tr_in, c_out, edge, 'transition')
        else:
            raise ValueError("[ERROR] Wrong method!")

    def propagate(self, edge, tr_in, c_out, method):
        if method == 'rounded':
            return (get_value_rounded(self.table, tr_in, c_out, edge, 'transition') +
                    get_value_rounded(self.table, tr_in, c_out, edge))
        elif method == 'interpolated':
            return (get_value_interpolated(self.table, tr_in, c_out, edge, 'transition') +
                    get_value_interpolated(self.table, tr_in, c_out, edge))
        else:
            raise ValueError("[ERROR] Wrong method!")


if __name__ == '__main__':
    and_gate = Gate(name='AND')
    print(and_gate.propagate('posedge', 0.4, 0.4, 'rounded'))
