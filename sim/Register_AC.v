module Register_AC #(
     parameter WIDTH = 16
)(
    input clk, reset_ac, write_ac, load_ac, increment_ac,
    input [WIDTH-1:0] DATA_ac,
    output reg[WIDTH-1:0] op_of_ac
);
    initial begin
        op_of_ac = 0;
    end

    always @(posedge clk) begin
        if (reset_ac) begin
            op_of_ac <= 0;
        end else begin
            if (load_ac) begin  
                op_of_ac <= DATA_ac;
            end else if (increment_ac) begin
                op_of_ac <= op_of_ac + 4'h0001;
            end
        end

    end


endmodule
