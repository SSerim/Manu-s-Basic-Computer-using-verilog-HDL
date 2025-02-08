module Register_TR #(
     parameter WIDTH = 16
)(
    input clk, reset_tr, write_tr, load_tr, increment_tr,
    input [WIDTH-1:0] DATA_tr,
    output reg [WIDTH-1:0] op_of_tr
);
    initial begin
        op_of_tr = 0;
    end

    always @(posedge clk or posedge reset_tr) begin
        if (reset_tr) begin
            op_of_tr <= 0;
        end else begin
            if (load_tr) begin
                op_of_tr <= DATA_tr;
            end else if (increment_tr) begin
                op_of_tr <= op_of_tr + 1'b1;
            end
        end
    end


endmodule
