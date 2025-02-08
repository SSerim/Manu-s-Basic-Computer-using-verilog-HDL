module Register_IR #(
     parameter WIDTH = 16
)(
    input clk, reset_ir, load_ir, increment_ir,
    input [WIDTH-1:0] DATA_ir,
    output reg [WIDTH-1:0] op_of_ir
);
    initial begin
        op_of_ir = 0;
    end

    always @(posedge clk or posedge reset_ir) begin
        if (reset_ir) begin
            op_of_ir <= 0;
        end else begin
            if (load_ir) begin
                op_of_ir <= DATA_ir;
            end else if (increment_ir) begin
                    op_of_ir <= op_of_ir + 1'b1;
            end
        end

    end


endmodule
