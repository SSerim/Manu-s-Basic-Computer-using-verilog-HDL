module Memory(
    input clk,
    input write_enable,
    input[15:0] write_data,
    input[11:0] address,
    output reg[15:0] read_data  
);
    reg [15:0] memory [0:4095];
    initial begin
        memory[12'h001] = 16'h4250;  //Branch Unconditionally to address 250 for interrupt
        memory[12'h010] = 16'h7020; // 1. INC AC instruction at address 0
        memory[12'h011] = 16'h2740; // 2. LOAD AC instruction at address 1, its M[EA] is at address = 12'h740 and data is 16'h0020
        memory[12'h012] = 16'h0800; // 3. AND memory word to AC instruction at address 2, its M[EA] is at address = 12'h800 and data is 16'h00F1
        memory[12'h013] = 16'h1900; // 4. ADD memory word to AC instruction at address 3, its M[EA] is at address = 12'h900 and data is 16'h1000
        memory[12'h014] = 16'h7200; // 5. Complement AC instruction at adress 4
        memory[12'h015] = 16'h3780; // 6. STORE Accumulator word to the memory at the address 12'h780
        memory[12'h016] = 16'h7080; // 7. Circulate Right Accumulator and E
        memory[12'h017] = 16'h7400; // 8. Clear E
        memory[12'h018] = 16'h4030; // 9. Branch unconditionally to address 030
        memory[12'h030] = 16'h7800; // 10. Clear Accumulator
        memory[12'h031] = 16'hF080; // 11. ION
        memory[12'h032] = 16'hF040; // 12. IOF
        memory[12'h740] = 16'h0030; // Data of 2.
        memory[12'h800] = 16'h00F1; // Data of 3.
        memory[12'h900] = 16'h1000; // Data of 4.

        memory[12'h250] = 16'h4000; //Branch Unconditionally to address 0 because interrupt is finished
                // Add other instructions as needed
    end
    always @(*) begin
        read_data = memory[address]; // Read operation
    end
    always @(posedge clk) begin
        //read_data = memory[address]; // Read operation

        if (write_enable) begin
            memory[address] <= write_data; // Write operation
        end
    end

endmodule
