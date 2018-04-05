import os

from myhdl import always_comb, Cosimulation


def wb_mux(mem_to_reg, rdata_in, result_in, wb_out):
    """
    Writeback Mux ALU Result / Memory data
    :param mem_to_reg: ctrl signal, from mem_wb.mem_to_reg 1 for memory, 0 for register.
    :param rdata_in: Read data input. from mem_wb.rdata_out
    :param result_in: result input. from mem_wb.result_out
    :param wb_out: output to write to register file. to rfile.w_data
    :return: module logic
    """

    @always_comb
    def logic():
        pass
        # NOT IMPLEMENTED
    return logic


def wb_mux_v(mem_to_reg, rdata_in, result_in, wb_out):
    """
    Writeback Mux ALU Result / Memory data Verilog
    :param mem_to_reg: ctrl signal, from mem_wb.mem_to_reg 1 for memory, 0 for register.
    :param rdata_in: Read data input. from mem_wb.rdata_out
    :param result_in: result input. from mem_wb.result_out
    :param wb_out: output to write to register file. to rfile.w_data
    :return: module logic
    """
    cmd = "iverilog -o wb_mux.out src/verilog/wb_mux.v src/verilog/wb_mux_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m lib/myhdl.vpi wb_mux.out",
                        mem_to_reg=mem_to_reg,
                        rdata_in=rdata_in,
                        result_in=result_in,
                        wb_out=wb_out)
