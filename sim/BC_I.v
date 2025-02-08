module BC_I (
    input clk,
    input FGI,
    output [11:0] PC,
    output [11:0] AR,
    output [15:0] IR,
    output [15:0] AC,
    output [15:0] DR
);

//wires for interrupt stuff
wire op_of_R , op_of_ien, reset_R, increment_R;
// Internal signals for connecting the datapath and controller
wire reset_tr, write_tr, load_tr, increment_tr;
wire reset_pc, load_pc, increment_pc;
wire reset_ir, write_ir, load_ir, increment_ir;
wire reset_ien, write_ien, load_ien, increment_ien;
wire reset_dr, write_dr, load_dr, increment_dr;
wire reset_co, write_co, load_co, increment_co;
wire reset_ar, load_ar, increment_ar;
wire reset_ac, write_ac, load_ac, increment_ac;
wire [2:0] bus_selects;
wire write_enable;
wire [2:0] op_select;
wire S;

// Signals for the DataPath outputs
wire overflow, negative, zero, E_carryout;
wire [15:0] instruction, data_reg_content;

// Instantiate the Controller module
Controller controller_inst (
    .clk(clk),
    .OVF(overflow),
    .Z(zero),
    .N(negative),
    .E(E_carryout),
    .instruction_controller(IR),
    .data_reg_content(DR),

    .op_of_R(op_of_R),
    .op_of_ien(op_of_ien),
    .FGI(FGI),
    
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
        
    .reset_dr(reset_dr),
    .write_dr(write_dr),
    .load_dr(load_dr),
    .increment_dr(increment_dr),
    
    .reset_co(reset_co),
    .write_co(write_co),
    .load_co(load_co),
    .increment_co(increment_co),
    
    .reset_ar(reset_ar),
    .load_ar(load_ar),
    .increment_ar(increment_ar),
    
    .reset_ac(reset_ac),
    .write_ac(write_ac),
    .load_ac(load_ac),
    .increment_ac(increment_ac),
    
    .bus_selects(bus_selects),
    .write_enable(write_enable),
    .op_select(op_select),
    .S(S),
    .D(D),
    .state(state_number),

    .increment_ien(increment_ien),
    .reset_ien(reset_ien), 
    .reset_R(reset_R),
    .increment_R(increment_R)
);

// Instantiate the DataPath module
DataPath datapath_inst (
    .increment_ien(increment_ien),
    .reset_ien(reset_ien), 
    .reset_R(reset_R),
    .increment_R(increment_R),

    .clk_data(clk),
    .reset_tr(reset_tr),
    .write_tr(write_tr),
    .load_tr(load_tr),
    .increment_tr(increment_tr),
    .reset_pc(reset_pc),
    .load_pc(load_pc),
    .increment_pc(increment_pc),
    .reset_ir(reset_ir),
    .load_ir(load_ir),
    .increment_ir(increment_ir),
    .reset_dr(reset_dr),
    .write_dr(write_dr),
    .load_dr(load_dr),
    .increment_dr(increment_dr),
    .reset_co(reset_co),
    .write_co(write_co),
    .load_co(load_co),
    .increment_co(increment_co),
    .reset_ar(reset_ar),
    .load_ar(load_ar),
    .increment_ar(increment_ar),
    .reset_ac(reset_ac),
    .write_ac(write_ac),
    .load_ac(load_ac),
    .increment_ac(increment_ac),
    .bus_selects(bus_selects),
    .write_enable(write_enable),
    .op_select(op_select),
    
    // Outputs
    .overflow(overflow),
    .negative(negative),
    .zero(zero),
    .E_carryout(E_carryout),
    .instruction(IR),
    .pc_content(PC),
    .data_reg_content(DR),
    .accumulator(AC),
    .ar_content(AR),
    .bus(bus),

    .op_of_R(op_of_R),
    .op_of_ien(op_of_ien)
);

// Connect the DataPath outputs to the top module outputs
//assign PC = AR;  // Assuming AR holds the Program Counter (PC)
//assign AR = 12'b0;  // Example: you may want to connect AR to actual address lines
//assign IR = instruction;
//assign DR = data_reg_content;  // Connect DR to appropriate data register output

endmodule
