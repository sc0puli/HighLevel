
import Gate

class Scheme:
    def __init__(self, gate_list):
        self.gate_list = gate_list



if __name__ == '__main__':
    and_gate = Gate.Gate(name='AND')
    print(and_gate.propagate('posedge', 0.4, 0.4, 'rounded'))

    # xnor_gate = Gate.Gate(name='XNOR')
    nor_gate = Gate.Gate(name='NOR')
    # and_xnor_nor = Scheme([Gate.Gate(name='AND'), Gate.Gate(name='XNOR'), Gate.Gate(name='NOR')])
    # print (and_xnor_nor.gate_list)

