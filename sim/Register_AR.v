module Register_AR #(
     parameter WIDTH = 12
)(
    input clk, reset_ar, write_ar, load_ar, increment_ar,
    input [WIDTH-1:0] DATA_ar,
    output reg [WIDTH-1:0] op_of_ar
);
    initial begin
        op_of_ar = 0;
    end

    always @(posedge clk) begin
        if (reset_ar) begin
            op_of_ar <= 0;
        end else begin
            if (load_ar) begin
                op_of_ar <= DATA_ar;
            end else if (increment_ar) begin
                op_of_ar <= op_of_ar + 1'b1;
            end
        end

    end


endmodule
