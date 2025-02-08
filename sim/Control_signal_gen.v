module Control_signal_gen(
    input wire  OVF, Z, N, E,
    input wire [3:0] state_no,
    input wire [15:0] op_of_dr,
    input wire op_of_R, 
    input wire op_of_ien,
    input wire FGI,
    input wire [15:0] instruction_control_signal,
    output reg reset_tr, write_tr, load_tr, increment_tr,
    output reg reset_pc, write_pc, load_pc, increment_pc,
    output reg reset_ir, write_ir, load_ir, increment_ir,
    //output reg reset_ien, write_ien, load_ien, increment_ien,
    output reg reset_dr, write_dr, load_dr, increment_dr,
    output reg reset_co, write_co, load_co, increment_co,
    output reg reset_ar, write_ar, load_ar, increment_ar,
    output reg reset_ac, write_ac, load_ac, increment_ac,
    output reg[2:0] bus_selects,
    output reg write_enable,
    output reg[2:0] op_select,
    output reg inc_controller_counter, clr_controller_counter,
    output reg S,
    output reg [2:0] D_no,
    output reg increment_ien , reset_ien, reset_R , increment_R
);
//reg [2:0] D_no;
//assign D = D_no;
reg I;
reg [11:0] address_no;
always @(*) begin
    // Initialize control signals to default values
    reset_tr = 1'b0; write_tr = 1'b0; load_tr = 1'b0; increment_tr = 1'b0;
    reset_pc = 1'b0; write_pc = 1'b0; load_pc = 1'b0; increment_pc = 1'b0;
    reset_ir = 1'b0; write_ir = 1'b0; load_ir = 1'b0; increment_ir = 1'b0;
    reset_dr = 1'b0; write_dr = 1'b0; load_dr = 1'b0; increment_dr = 1'b0;
    reset_co = 1'b0; write_co = 1'b0; load_co = 1'b0; increment_co = 1'b0;
    reset_ar = 1'b0; write_ar = 1'b0; load_ar = 1'b0; increment_ar = 1'b0;
    reset_ac = 1'b0; write_ac = 1'b0; load_ac = 1'b0; increment_ac = 1'b0;
    write_enable = 1'b0;            D_no = 3'b000;  op_select = 3'b000;
    inc_controller_counter = 1'b0; clr_controller_counter = 1'b0; S = 1'b0;
    increment_ien = 1'b0; reset_ien = 1'b0; reset_R = 1'b0; increment_R = 1'b0;

    if ((state_no != 4'b000 )&&(state_no != 4'b001 )&&(state_no != 4'b010 )&&(op_of_ien == 1'b1)&&(FGI == 1'b1)) begin
        increment_R = 1'b1;
    end

    //Fetch and Decode
        case(state_no) 
        // PC content to AR
        4'b0000: begin
            if (op_of_R == 1'b1) begin
                reset_ar = 1'b1;
                bus_selects = 3'b010;
                load_tr = 1'b1;
                inc_controller_counter = 1'b1;
            end else begin
            write_pc = 1'b1;
            bus_selects = 3'b010;
            load_ar = 1'b1;
            inc_controller_counter = 1'b1;
            end

        end
        // AR content to IR
        4'b0001: begin
            if (op_of_R == 1'b1) begin
                bus_selects = 3'b110;
                write_enable = 1'b1;
                reset_pc = 1'b1;
                inc_controller_counter = 1'b1;
            end else begin
            increment_pc = 1'b1;
            bus_selects = 3'b111;
            load_ir = 1'b1;
            inc_controller_counter = 1'b1;      //checkpoint
            end
        end
        4'b0010: begin
            if (op_of_R == 1'b1) begin
                increment_pc = 1'b1;
                bus_selects = 3'b010;
                reset_R = 1'b1;
                reset_ien = 1'b1;
                clr_controller_counter = 1'b1;
            end else begin
            inc_controller_counter = 1'b1;  
            end
        end
        4'b0011: begin
            if((instruction_control_signal[14:12] == 3'b111) && (instruction_control_signal[15] == 1'b1)) begin
                if (instruction_control_signal[11:0] == 12'h080) begin
                    increment_ien = 1'b1;
                    clr_controller_counter = 1'b1;
                end else if (instruction_control_signal[11:0] == 12'h040) begin
                    reset_ien = 1'b1;
                    clr_controller_counter = 1'b1;
                end

            end
            if(instruction_control_signal[14:12] != 3'b111) begin
                if(instruction_control_signal[15] == 1'b0) begin
                    bus_selects = 3'b111;
                    load_ar = 1'b1;
                    inc_controller_counter = 1'b1;
                end
                else begin
                    write_pc = 1'b0;
                    bus_selects = 3'b000;
                    load_ar = 1'b0;
                    increment_pc = 1'b0;
                    load_ir = 1'b0;
                    inc_controller_counter = 1'b1;

                end
            
            end
            if((instruction_control_signal[14:12] == 3'b111) && (instruction_control_signal[15] == 1'b0) ) begin

                if(instruction_control_signal[11:0] == 12'h800) begin
                    reset_ac = 1'b1;
                    clr_controller_counter = 1'b1;
                end
                if(instruction_control_signal[11:0] == 12'h400) begin
                    reset_co = 1'b1;
                    clr_controller_counter = 1'b1;
                end
                if(instruction_control_signal[11:0] == 12'h200) begin
                    op_select = 3'b100;
                    load_ac = 1'b1;
                    clr_controller_counter = 1'b1;
                end
                if(instruction_control_signal[11:0] == 12'h100) begin
                    increment_co = 1'b1;
                    clr_controller_counter = 1'b1;
                end
                if(instruction_control_signal[11:0] == 12'h080) begin
                    op_select = 3'b101;
                    load_ac = 1'b1;
                    load_co = 1'b1;
                    clr_controller_counter = 1'b1;
                end
                if(instruction_control_signal[11:0] == 12'h040) begin
                    op_select = 3'b110;
                    clr_controller_counter = 1'b1;
                end
                if(instruction_control_signal[11:0] == 12'h020) begin
                    increment_ac = 1'b1;
                    clr_controller_counter = 1'b1;
                end
                if(instruction_control_signal[11:0] == 12'h010) begin
                    if((Z == 1'b0)&&(N==1'b0)) begin
                        increment_pc = 1'b1;
                        clr_controller_counter = 1'b1;
                    end
                    else begin
                    clr_controller_counter = 1'b1;
                    end
                end
                if(instruction_control_signal[11:0] == 12'h008) begin
                    if(N) begin
                        increment_pc = 1'b1;
                        clr_controller_counter = 1'b1;
                    end
                    else begin
                    clr_controller_counter = 1'b1;
                    end
                end
                if(instruction_control_signal[11:0] == 12'h004) begin
                    if(Z) begin
                        increment_pc = 1'b1;
                        clr_controller_counter = 1'b1;
                    end
                    else begin
                    clr_controller_counter = 1'b1;
                    end
                end
                if(instruction_control_signal[11:0] == 12'h002) begin
                    if(E == 1'b0) begin
                        increment_pc = 1'b1;
                        clr_controller_counter = 1'b1;
                    end
                    else begin
                    clr_controller_counter = 1'b1;
                    end
                end
                if(instruction_control_signal[11:0] == 12'h001) begin
                    S = 1'b0; //for halting the computer
                end
                

        end
        end
        4'b0100: begin   
            if(((instruction_control_signal[14:12] == 3'b000) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b000) && (instruction_control_signal[15] == 1'b1)) begin  //AND memory word to AC
                bus_selects = 3'b111;
                load_dr = 1'b1;
                inc_controller_counter = 1'b1;
                
            end else if(((instruction_control_signal[14:12] == 3'b001) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b001) && (instruction_control_signal[15] == 1'b1)) begin  //ADD memory word to AC
                bus_selects = 3'b111;
                load_dr = 1'b1;
                inc_controller_counter = 1'b1;
                
            end  else if(((instruction_control_signal[14:12] == 3'b010) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b010) && (instruction_control_signal[15] == 1'b1)) begin  //memory word to AC
                bus_selects = 3'b111;
                load_dr = 1'b1;
                op_select = 3'b011;
                load_ac = 1'b1;
                inc_controller_counter = 1'b1;
            end else if(((instruction_control_signal[14:12] == 3'b011) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b011) && (instruction_control_signal[15] == 1'b1)) begin  //AC to memory word
                bus_selects = 3'b100;
                write_enable = 1'b1;
                inc_controller_counter = 1'b1;
            end else if(((instruction_control_signal[14:12] == 3'b100) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b100) && (instruction_control_signal[15] == 1'b1)) begin  //branch unconditionally
                bus_selects = 3'b001;
                write_ar = 1'b1;    
                load_pc = 1'b1;
                clr_controller_counter = 1'b1;
            end else if(((instruction_control_signal[14:12] == 3'b101) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b101) && (instruction_control_signal[15] == 1'b1)) begin  //branch and save return address
                bus_selects = 3'b010;
                write_pc = 1'b1;
                write_enable = 1'b1;
                increment_ar = 1'b1;
                inc_controller_counter = 1'b1;
            end else if(((instruction_control_signal[14:12] == 3'b110) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b110) && (instruction_control_signal[15] == 1'b1)) begin  //ISZ
                bus_selects = 3'b111;
                load_dr = 1'b1;
                inc_controller_counter = 1'b1;
            end
        end
        4'b0101: begin
            if(((instruction_control_signal[14:12] == 3'b000) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b000) && (instruction_control_signal[15] == 1'b1)) begin  //AND memory word to AC
                load_dr = 1'b0;
                write_dr = 1'b1;
                op_select = 3'b010;
                inc_controller_counter = 1'b1;
            end else if(((instruction_control_signal[14:12] == 3'b001) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b001) && (instruction_control_signal[15] == 1'b1)) begin  //ADD memory word to AC
                load_dr = 1'b0;
                write_dr = 1'b1;
                op_select = 3'b001;
                inc_controller_counter = 1'b1;
            end else if(((instruction_control_signal[14:12] == 3'b001) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b001) && (instruction_control_signal[15] == 1'b1)) begin  //Branch and Save Return address
                bus_selects = 3'b001;
                write_ar = 1'b1;
                load_pc = 1'b1;
                clr_controller_counter = 1'b1;
            end  else if(((instruction_control_signal[14:12] == 3'b010) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b010) && (instruction_control_signal[15] == 1'b1)) begin  //memory word to AC
                load_ac = 1'b1;
                reset_dr = 1'b1;
                clr_controller_counter = 1'b1;
            end else if(((instruction_control_signal[14:12] == 3'b011) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b011) && (instruction_control_signal[15] == 1'b1)) begin  //AC to memory word
                bus_selects = 3'b111;
                load_dr = 1'b1;
                clr_controller_counter = 1'b1;
            end else if(((instruction_control_signal[14:12] == 3'b110) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b110) && (instruction_control_signal[15] == 1'b1)) begin  //ISZ
                increment_dr = 1'b1;
                inc_controller_counter = 1'b1;
            end
        end
        4'b0110: begin
            if(((instruction_control_signal[14:12] == 3'b000) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b000) && (instruction_control_signal[15] == 1'b1)) begin  //AND memory word to AC
                write_dr = 1'b0;
                op_select = 3'b000;
                load_ac = 1'b1;
                reset_dr = 1'b1;
                clr_controller_counter = 1'b1;
            end else if(((instruction_control_signal[14:12] == 3'b001) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b001) && (instruction_control_signal[15] == 1'b1)) begin  //ADD memory word to AC
                write_dr = 1'b0;
                op_select = 3'b000;
                load_ac = 1'b1;
                reset_dr = 1'b1;
                clr_controller_counter = 1'b1;
            end else if(((instruction_control_signal[14:12] == 3'b110) && (instruction_control_signal[15] == 1'b0)) || ( instruction_control_signal[14:12] == 3'b110) && (instruction_control_signal[15] == 1'b1)) begin  //ISZ
                if (op_of_dr == 0) begin
                    increment_pc = 1'b1;
                    clr_controller_counter = 1'b1;
                end
                else begin
                    bus_selects = 3'b011;
                    write_dr = 1'b1;
                    write_enable = 1'b1;
                end

            end
        end


        endcase
end
endmodule