module Register_PC #(
     parameter WIDTH = 12
)(
    input clk, reset_pc, load_pc, increment_pc,
    input [WIDTH-1:0] DATA_pc,
    output reg [WIDTH-1:0] op_of_pc
);
    initial begin
        op_of_pc = 12'h010;
    end

    always @(posedge clk) begin
        if (reset_pc) begin
            op_of_pc <= 0;
        end else begin
            if (load_pc) begin
                op_of_pc <= DATA_pc;
            end else if (increment_pc) begin
                op_of_pc <= op_of_pc + 1'b1;
            end
        end

    end


endmodule
