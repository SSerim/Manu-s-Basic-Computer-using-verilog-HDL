module instruction_reader(
    input wire [15:0] instruction,
    output reg I,
    output reg [2:0] D,
    output reg [11:0] address
);

    always @(*) begin
        I = instruction[15];        
        address = instruction[11:0]; 
        D = instruction[14:12];       
    end

endmodule
