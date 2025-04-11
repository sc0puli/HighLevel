import Gate


if __name__ == '__main__':
    and_gate = Gate.Gate(name='AND')
    # print(and_gate.propagate('posedge', 0.4, 0.4, 'rounded'))
    xnor_gate = Gate.Gate(name='XNOR')
    nor_gate = Gate.Gate(name='NOR')

    total_delay = 0
    total_transition = 0

    tmp_delay, tmp_transition = and_gate.propagate('posedge', 16, 43, 'interpolated')
    total_transition += tmp_transition
    total_delay += tmp_delay

    tmp_delay, tmp_transition = xnor_gate.propagate('negedge', 16, 43, 'interpolated')
    total_transition += tmp_transition
    total_delay += tmp_delay

    tmp_delay, tmp_transition = nor_gate.propagate('posedge', 16, 43, 'interpolated')
    total_transition += tmp_transition
    total_delay += tmp_delay

    print(f'For scheme AND->XNOR->NOR calculated delay : {total_delay}, transition : {total_transition}')


