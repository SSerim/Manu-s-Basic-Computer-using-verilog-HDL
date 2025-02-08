//MULX module will take inputs from all the registers namely "data_in#number" and if any select signal is given or changed, 
//its output data_out will be adjusted according to data_in#number

module MULX #(
    parameter WIDTH=16)
    (
    input wire[2:0] bus_selects,
    //input wire[7:0] reg_select,
    input wire [WIDTH - 1:0] data_in1,
    input wire [WIDTH - 1:0] data_in2,
    input wire [WIDTH - 1:0] data_in3,
    input wire [WIDTH - 1:0] data_in4,
    input wire [WIDTH - 1:0] data_in5,
    input wire [WIDTH - 1:0] data_in6,
    input wire [WIDTH - 1:0] data_in7,
    output reg [WIDTH - 1:0] data_out
);
initial begin
    data_out = 16'h0000;
end

always@ (*) begin
    data_out = 16'h0000;
    case(bus_selects)
    3'b001: data_out = data_in1;
    3'b010: data_out = data_in2;
    3'b011: data_out = data_in3;
    3'b100: data_out = data_in4;
    3'b101: data_out = data_in5;
    3'b110: data_out = data_in6;
    3'b111: data_out = data_in7;
    default: ;
    endcase
end

endmodule