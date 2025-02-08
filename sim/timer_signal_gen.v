module timer_signal_gen(
    input wire clk_controller,            // Controller clock signal
    input wire inc_controller_counter,   // Signal to increment the state counter
    input wire clr_controller_counter,   // Clear signal for the state counter
    output reg [3:0] state_counter      // 4-bit state counter output
);
initial begin
    state_counter = 4'b0000;
end


// Clear the counter on reset or when it reaches the final state (4'b1111)
always @(posedge clk_controller) begin
    if (clr_controller_counter || state_counter == 4'b1111) 
        state_counter <= 4'b0000;  // Reset the counter to 0
    else if (inc_controller_counter) 
        state_counter <= state_counter + 1'b1;  // Increment state counter
end

endmodule
