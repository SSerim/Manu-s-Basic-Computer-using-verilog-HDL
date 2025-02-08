module DataPath(
    input wire clk_data,
    input wire reset_tr, write_tr, load_tr, increment_tr,
    input wire reset_pc, load_pc, increment_pc,
    input wire reset_ir, load_ir, increment_ir,
    input wire reset_ien, increment_ien,
    input wire reset_R, increment_R,
    input wire reset_dr, write_dr, load_dr, increment_dr,
    input wire reset_co, write_co, load_co, increment_co,
    input wire reset_ar, load_ar, increment_ar,
    input wire reset_ac, write_ac, load_ac, increment_ac,
    input wire[2:0] bus_selects,
    input write_enable,
    input wire[2:0] op_select,
    output wire overflow,negative,zero, E_carryout,
    output reg[15:0] instruction,
    output reg[11:0] pc_content,
    output reg[11:0] ar_content,
    output reg[15:0] data_reg_content,
    output reg[15:0] accumulator,
    output [15:0] bus,
    output reg op_of_ien,
    output reg op_of_R
);
wire[15:0] DATA_pc,DATA_ar,bus_out,result_alu; 
assign bus = bus_out;
wire[15:0] data_in1d,data_in2d,data_in3d,data_in4d,data_in5d,data_in6d,data_in7d;
assign pc_content = data_in2d_11;
assign ar_content = data_in1d_11;
assign data_reg_content = data_in3d;
assign accumulator = data_in4d;
//This part for adjusting the length of I/O of PC
wire[11:0] DATA_pc_in = DATA_pc[11:0];
wire[11:0] data_in2d_11;
assign data_in2d[11:0] = data_in2d_11;
assign data_in2d[15:12] = 4'b000;
//Finished adjustment of PC
//This part for adjusting the length of I/O of AR
wire[11:0] DATA_ar_in = DATA_ar[11:0];
wire[11:0] data_in1d_11;
assign data_in1d[11:0] = data_in1d_11;
assign data_in1d[15:12] = 4'b000;
//Finished adjustment of AR
wire co_carryout;
Register_IEN interrupt(
    .clk(clk_data),
    .reset_ien(reset_ien),
    .increment_ien(increment_ien),
    .op_of_ien(op_of_ien)
);
FF_R R(
    .clk(clk_data),
    .reset_R(reset_R),
    .increment_R(increment_R),
    .op_of_R(op_of_R)
);
MULX common_bus(
    .bus_selects(bus_selects),
    .data_in1(data_in1d),
    .data_in2(data_in2d),
    .data_in3(data_in3d),
    .data_in4(data_in4d),
    .data_in5(instruction),
    .data_in6(data_in6d),
    .data_in7(data_in7d),
    .data_out(bus_out)
);

Register_TR temp_reg(
    .clk(clk_data),
    .reset_tr(reset_tr),
    .write_tr(write_tr),
    .load_tr(load_tr),
    .increment_tr(increment_tr),
    .DATA_tr(bus_out),
    .op_of_tr(data_in6d)
);

Register_PC prog_counter(
    .clk(clk_data),
    .reset_pc(reset_pc),
    .load_pc(load_pc),
    .increment_pc(increment_pc),
    .DATA_pc(bus_out[11:0]),
    .op_of_pc(data_in2d_11)
);

Register_IR instr_reg(
    .clk(clk_data), 
    .reset_ir(reset_ir),
    .load_ir(load_ir),
    .increment_ir(increment_ir),
    .DATA_ir(bus_out),
    .op_of_ir(instruction)
);

Register_DR data_reg(
    .clk(clk_data),
    .reset_dr(reset_dr),
    .write_dr(write_dr),
    .load_dr(load_dr),
    .increment_dr(increment_dr),
    .DATA_dr(bus_out),
    .op_of_dr(data_in3d)
);

Register_AR address_reg(
    .clk(clk_data),
    .reset_ar(reset_ar),
    .load_ar(load_ar),
    .increment_ar(increment_ar),
    .DATA_ar(bus_out[11:0]),
    .op_of_ar(data_in1d_11)
);

Memory memo(
    .clk(clk_data),
    .write_enable(write_enable),
    .write_data(bus_out),
    .address(data_in1d_11),
    .read_data(data_in7d)
);

Register_CO carry_out(
    .clk(clk_data),
    .reset_co(reset_co),
    .inc_co(increment_co),
    .write_co(write_co),
    .load_co(load_co),
    .data_co(co_carryout),
    .op_of_co(E_carryout)
);

Register_AC accumulat(
    .clk(clk_data),
    .reset_ac(reset_ac),
    .write_ac(write_ac),
    .load_ac(load_ac),
    .increment_ac(increment_ac),
    .DATA_ac(result_alu),
    .op_of_ac(data_in4d)
);

ALU algor_log_unit(
    .AC(data_in4d),
    .DR(data_in3d),
    .E(E_carryout),
    .op_select(op_select),
    .result(result_alu),
    .CO(co_carryout),
    .OVF(overflow),
    .N(negative),
    .Z(zero)
);

endmodule