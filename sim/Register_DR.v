module Register_DR #(
     parameter WIDTH = 16
)(
    input clk, reset_dr, write_dr, load_dr, increment_dr,
    input [WIDTH-1:0] DATA_dr,
    output reg[WIDTH-1:0] op_of_dr
);
    initial begin
        op_of_dr = 0;
    end

    always @(posedge clk) begin
        if (reset_dr) begin
            op_of_dr <= 0;
        end else begin
            if (load_dr) begin
                op_of_dr <= DATA_dr;
            end else if (increment_dr) begin
                op_of_dr <= op_of_dr + 1'b1;
            end
        end
    end


endmodule
