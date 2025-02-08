module FF_R (
    input clk, reset_R, increment_R,
    output reg op_of_R
);
    initial begin
        op_of_R = 0;
    end

    always @(posedge clk) begin
        if (reset_R) begin
            op_of_R <= 0;
        end else if (increment_R) begin
            op_of_R <= op_of_R + 1'b1;
            end
        end
endmodule
