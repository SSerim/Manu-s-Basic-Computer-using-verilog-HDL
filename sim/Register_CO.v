module Register_CO(
    input clk, reset_co, write_co, load_co, inc_co,
    input data_co,
    output reg op_of_co
);
    initial begin
        op_of_co = 1'b0;
    end

    always @(posedge clk ) begin
        if (reset_co) begin
            op_of_co <= 1'b0;
        end else begin
            if (load_co) begin
                op_of_co <= data_co;
            end else if (inc_co) begin
                op_of_co <= op_of_co + 1'b1;
            end
        end
    end


endmodule
