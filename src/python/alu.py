""""
    alu: The main ALU
    input [31:0] op_1: a 32 bit operand.  from alu_mux_1
    input [31:0] op_2: a 32 bit operand.  from alu_mux_imm
    input [3:0] alu_op: The 4-bit ALU op code.  See  OpCode table.
    output [31:0] result: a 32 bit result of operation.  to ex_mem
    output z: Zero flag.  to ex_mem
"""""
def alu(op_1, op_2, alu_op):
    if(alu_op == 0001): 
        result.next = op_1 + op2
    elif(alu_op == 0010	):
        result.next = op_1 - op_2
    elif(alu_op == 0011): 
        result.next = op_1 ^ op_2
    elif(alu_op == 0100):
        result.next = op_1 | op_2
    elif(alu_op == 0101):
        result.next = op_1 & op_2
    elif(alu_op == 0110):
        result.next = op_1 << op_2
    elif(alu_op == 0111):
        result.next = op_1 >> op_2
    elif(alu_op == 1000):
        result.next = ~(op_1 or op_2)
    elif(alu_op == 1001):
        if(op_1 < op_2):
            result.next = 1
        else:
            result.next = 0

    z = true if result.next == 0 else false
