module Register_IEN (
    input clk, reset_ien, increment_ien,
    output reg op_of_ien
);
    initial begin
        op_of_ien = 0;
    end

    always @(posedge clk) begin
        if (reset_ien) begin
            op_of_ien <= 0;
        end else if (increment_ien) begin
            op_of_ien <= op_of_ien + 1'b1;
            end
        end
endmodule
