module Controller(
    input wire clk,
    input wire OVF, Z, N, E,
    input wire [15:0] instruction_controller,
    input wire [15:0] data_reg_content,
    input wire op_of_ien , op_of_R , FGI,
    output reg reset_tr, write_tr, load_tr, increment_tr,
    output reg reset_pc, load_pc, increment_pc,
    output reg reset_ir, write_ir, load_ir, increment_ir,
    output reg reset_ien, write_ien, load_ien, increment_ien,
    output reg reset_dr, write_dr, load_dr, increment_dr,
    output reg reset_co, write_co, load_co, increment_co,
    output reg reset_ar, write_ar, load_ar, increment_ar,
    output reg reset_ac, write_ac, load_ac, increment_ac,
    output reg[2:0] bus_selects,
    output reg write_enable,
    output reg[2:0] op_select,
    output  reg S,
    output  reg[2:0]D,
    output  reg[3:0] state,
    output reg reset_R , increment_R
);
wire inc_controller_counter, clr_controller_counter;

timer_signal_gen timer (
    .clk_controller(clk),
    .inc_controller_counter(inc_controller_counter),
    .clr_controller_counter(clr_controller_counter),
    .state_counter(state)
);

Control_signal_gen u_Control_signal_gen (
    // Connect the inputs of the upper module to the Control_signal_gen instance
    .OVF(OVF),
    .Z(Z),
    .N(N),
    .E(E),
    .state_no(state),
    .op_of_dr(data_reg_content),
    .instruction_control_signal(instruction_controller),
    .op_of_R(op_of_R),
    .op_of_ien(op_of_ien),
    .FGI(FGI),
    
    // Connect the outputs of the Control_signal_gen instance to the upper module
    .reset_tr(reset_tr),
    .write_tr(write_tr),
    .load_tr(load_tr),
    .increment_tr(increment_tr),
    
    .reset_pc(reset_pc),
    .load_pc(load_pc),
    .increment_pc(increment_pc),
    
    .reset_ir(reset_ir),
    .write_ir(write_ir),
    .load_ir(load_ir),
    .increment_ir(increment_ir),
    
    //.reset_ien(reset_ien),
    //.write_ien(write_ien),
    //.load_ien(load_ien),
    //.increment_ien(increment_ien),
    
    .reset_dr(reset_dr),
    .write_dr(write_dr),
    .load_dr(load_dr),
    .increment_dr(increment_dr),
    
    .reset_co(reset_co),
    .write_co(write_co),
    .load_co(load_co),
    .increment_co(increment_co),
    
    .reset_ar(reset_ar),
    .write_ar(write_ar),
    .load_ar(load_ar),
    .increment_ar(increment_ar),
    
    .reset_ac(reset_ac),
    .write_ac(write_ac),
    .load_ac(load_ac),
    .increment_ac(increment_ac),
    
    .bus_selects(bus_selects),
    .write_enable(write_enable),
    .op_select(op_select),
    .inc_controller_counter(inc_controller_counter),
    .clr_controller_counter(clr_controller_counter),
    .S(S),
    .D_no(D),
    .increment_ien(increment_ien),
    .reset_ien(reset_ien), 
    .reset_R(reset_R),
    .increment_R(increment_R)
);



endmodule