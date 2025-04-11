import Table
import numpy as np


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
        self.table = Table.lib_parser(name, path)


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
            return (get_value_rounded(self.table, tr_in, c_out, edge, 'transition'),
                    get_value_rounded(self.table, tr_in, c_out, edge))
        elif method == 'interpolated':
            return (get_value_interpolated(self.table, tr_in, c_out, edge, 'transition'),
                    get_value_interpolated(self.table, tr_in, c_out, edge))
        else:
            raise ValueError("[ERROR] Wrong method!")