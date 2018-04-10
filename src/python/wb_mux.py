"""WB stage multiplexer module"""
from os import system
from myhdl import always_comb, Cosimulation

def wb_mux(sel, wb_out, rdata_in, result_in):
    """
    memory writeback mux
    :param sel: single bit selector. control signal. from mem_wb.mem_to_reg.
                1 for memory, 0 for register
    :param rdata_in: read data. input. from mem_wb.rdata_out
    :param result_in: result. input. from mem_wb.result_out
    :param wb_out: output to write to register file. to rfile.w_data
    :return: module logic
    """

    @always_comb
    def logic():
        if sel == 0:
            wb_out.next = result_in
            #print "Deassert - wb_out: {}, result_in: {}".format(wb_out.next, result_in)
        else:
            wb_out.next = rdata_in
            #print "Assert - wb_out: {}, rdata_in: {}".format(wb_out.next, rdata_in)
    return logic


def wb_mux_v(sel, wb_out, rdata_in, result_in):
    """
    memory writeback mux (verilog)
    :param sel: single bit selector. control signal. from mem_wb.mem_to_reg.
                1 for memory, 0 for register
    :param rdata_in: read data. input. from mem_wb.rdata_out
    :param result_in: result. input. from mem_wb.result_out
    :param wb_out: output to write to register file. to rfile.w_data
    :return: module logic
    """
    cmd = "iverilog -o bin/wb_mux.out src/verilog/wb_mux.v src/verilog/wb_mux_tb.v"
    system(cmd)
    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/wb_mux.out",
                        sel=sel,
                        wb_out=wb_out,
                        rdata_in=rdata_in,
                        result_in=result_in)
