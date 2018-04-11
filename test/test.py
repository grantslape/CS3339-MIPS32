from myhdl import Simulation, StopSimulation, posedge, Signal, negedge, toVerilog

from src.python.data_mem import data_mem, data_mem_v
from src.commons.settings import settings as sf
from src.commons.clock import clock_gen, half_period
from src.commons.signal_generator import unsigned_signal_set, random_unsigned_intbv, \
    random_signed_intbv, unsigned_intbv, signed_signal_set

clock, read_ctrl, write_ctrl = unsigned_signal_set(3, width=1)
mem_addr = Signal(unsigned_intbv(width=sf['MEMORY_WIDTH']))
rdata, rdata_v, wdata = signed_signal_set(3)
dut = data_mem(clk=clock,
                    address=mem_addr,
                    write_wire=write_ctrl,
                    read_wire=read_ctrl,
                    write_data=wdata,
                    read_data=rdata)

dut_v = data_mem_v(clk=clock, address=mem_addr, write_wire=write_ctrl, read_wire=read_ctrl, write_data=wdata, read_data=rdata_v)

def mon():
    for _ in range(sf['DEFAULT_TEST_LENGTH'] / 1000):
        yield clock.posedge
        yield clock.posedge


def dynamic():
    """test read/write functionality"""
    # expected = []
    # for _ in range(sf['DEFAULT_TEST_LENGTH']):
    #     expected.append(random_signed_intbv())
    for i in range(sf['DEFAULT_TEST_LENGTH'] / 1000):
        read_ctrl.next = 0
        write_ctrl.next = 1
        expected_addr = random_unsigned_intbv(width=sf['MEMORY_WIDTH'])
        mem_addr.next = expected_addr
        wdata.next = random_signed_intbv()
        yield clock.posedge
        # half_period()
        print(wdata)
        read_ctrl.next = 1
        write_ctrl.next = 0
        yield clock.posedge
        yield clock.negedge
    raise StopSimulation


def main():
    clk = clock_gen(clock)
    stim = dynamic()
    Simulation(clk, stim, dut, dut_v).run()


if __name__ == '__main__':
    main()
