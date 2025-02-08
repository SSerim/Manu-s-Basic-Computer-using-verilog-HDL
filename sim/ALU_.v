//MULX module will take inputs from all the registers namely "data_in#number" and if any select signal is given or changed, 
//its output data_out will be adjusted according to data_in#number

module ALU #(
    parameter WIDTH=16)
    (
    input wire [WIDTH - 1:0] AC,
    input wire [WIDTH - 1:0] DR,
    input wire E, 
    input wire[2:0] op_select,
    output reg [WIDTH - 1:0] result,
    output reg CO,  //carry out 
    output reg OVF, // Overflow
    output reg N,   // Negative
    output reg Z   // Zero
);
initial begin
    result = 16'h0000;
    CO = 1'b0;
    OVF = 1'b0;
    N = 1'b0;
    Z = 1'b0;
end
always@ (*) begin
    case(op_select)
    3'b001: begin
        {CO, result} = AC + DR + E;       //Addition---- AC + DR (including Carry in) --- CO will be 1 if there is a carry out --- E is added for multi-bit operations(more than 16 bit operations)
        //OVF = ((result[WIDTH - 1] == 0) & (AC[WIDTH - 1] == 1) & (DR[WIDTH - 1] == 1)) | ((result[WIDTH - 1] == 1) & (AC[WIDTH - 1] == 0) & (DR[WIDTH - 1] == 0));
        OVF = ((result[WIDTH - 1] == 0) & (AC[WIDTH - 1] == 1) & (DR[WIDTH - 1] == 1)) | ((result[WIDTH - 1] == 1) & (AC[WIDTH - 1] == 0) & (DR[WIDTH - 1] == 0));

    end
    3'b010: begin
        result = AC & DR;         //AND---------AC & DR
        OVF = 0;
    end
    3'b011: begin               //TRANSFER----DR
        result = DR;              
        OVF = 0;

    end
    3'b100: begin    //COMPLEMENT--AC'
    result = ~AC; 
    OVF = 0;
    end
    3'b101: begin    //SHIFT RIGHT
    {result} = {E, AC[WIDTH-1:1]};
    CO = AC[0];
    OVF = 0;
    end
    3'b110: begin    //SHIFT LEFT
    result = {AC[WIDTH-2:0], E};
    CO = AC[WIDTH-1];
    OVF = 0;
    end
    default: ;
    endcase
    Z = (result == 0);
    N = (result[WIDTH-1] == 1);
end

endmodule