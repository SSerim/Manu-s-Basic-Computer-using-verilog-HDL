import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge

#TRUE for printing signals
DEBUG = True

#CHANGE THE BELOW SIGNAL NAMES TO MATCH YOUR DESIGN!!!!!!!!!!!!!!!!!
def print_my_computer_please(dut):
    #Log whatever signal you want from the datapath, called before positive clock edge
    dut._log.info("************ DUT Signals ***************")
    dut._log.info(f" PC: {dut.PC.value}\t {hex(dut.PC.value)}\n\
    AR: {dut.AR.value}\t {hex(dut.AR.value)}\n\
    IR: {dut.IR.value}\t {hex(dut.IR.value)}\n\
    AC: {dut.AC.value}\t {hex(dut.AC.value)}\n\
    DR: {dut.DR.value}\t {hex(dut.DR.value)}\n")
    dut._log.info("************ Controller Signals ***************")
    dut._log.info(f"load_ir: {dut.controller_inst.load_ir.value}")
    dut._log.info("************ Datapath Signals ***************")
    dut._log.info(f"bus_selects: {hex(dut.datapath_inst.bus_selects.value)}")
    dut._log.info(f"result of alu: {hex(dut.datapath_inst.result_alu.value)}")
    dut._log.info(f"E: {hex(dut.datapath_inst.E_carryout.value)}")
    dut._log.info(f"op_of_ien: {hex(dut.datapath_inst.op_of_ien.value)}")

    

@cocotb.test()
async def basic_computer_test(dut):
    """Try accessing the design."""
    dut.FGI.value = 0
    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    #Get the fallin edge to work with
    clkedge = FallingEdge(dut.clk)
    
    #Check your design for however many cycles, assert at correct clock cycles
    for cycle in range(72):
        dut._log.info(f"Clock cycle {cycle}")
        await clkedge
        
        #Log values if debugging
        if DEBUG:
            print_my_computer_please(dut)
            
        #Sımple match-case structure to test when needed
        #You should modify it according to your sample code
        match cycle:
            case 0:
                assert dut.PC.value == 0x0010 ,"PC doesn't work!"
                assert dut.AR.value == 0x0000 ,"AR doesn't work!"
                assert dut.IR.value == 0x0000 ,"IR doesn't work!"
                assert dut.AC.value == 0x0000 ,"AC doesn't work!"
                assert dut.DR.value == 0x0000 ,"DR doesn't work!"


            case 1:
                assert dut.PC.value == 0x0010 ,"PC doesn't work!"   #Fetch of 1st instruction -- Increment AC
                assert dut.AR.value == 0x0010 ,"AR doesn't work!"
                assert dut.IR.value == 0x0000 ,"IR doesn't work!"
                assert dut.AC.value == 0x0000 ,"AC doesn't work!"
                assert dut.DR.value == 0x0000 ,"DR doesn't work!"


            case 2:
                assert dut.PC.value == 0x0011 ,"PC doesn't work!"
                assert dut.AR.value == 0x0010 ,"AR doesn't work!"
                assert dut.IR.value == 0x7020 ,"IR doesn't work!"
                assert dut.AC.value == 0x0000 ,"AC doesn't work!"
                assert dut.DR.value == 0x0000 ,"DR doesn't work!"

            case 3:
                assert dut.PC.value == 0x0011, "PC doesn't work!"
                assert dut.AR.value == 0x0010 ,"AR doesn't work!"
                assert dut.IR.value == 0x7020 ,"IR doesn't work!"
                assert dut.AC.value == 0x0000 ,"AC doesn't work!"
                assert dut.DR.value == 0x0000 ,"DR doesn't work!"
            case 4:
                assert dut.PC.value == 0x0011 ,"PC doesn't work!"
                assert dut.AR.value == 0x0010 ,"AR doesn't work!"
                assert dut.IR.value == 0x7020 ,"IR doesn't work!"
                assert dut.AC.value == 0x0001, "AC WORKİNG !"   #Accumulator incremented, 1st instruction succesfuly finished
                assert dut.DR.value == 0x0000 ,"DR doesn't work!"
            case 5:
                assert dut.PC.value == 0x0011 ,"PC doesn't work!"
                assert dut.AR.value == 0x0011 ,"AR doesn't work!"    #Fetch of 2nd instruction ---- LOAD ACCUMULATOR from memory
                assert dut.IR.value == 0x7020 ,"IR doesn't work!"
                assert dut.AC.value == 0x0001 ,"AC doesn't work!"
                assert dut.DR.value == 0x0000 ,"DR doesn't work!"
            case 6:
                assert dut.PC.value == 0x0012 ,"PC doesn't work!"
                assert dut.AR.value == 0x0011 ,"AR doesn't work!"
                assert dut.IR.value == 0x2740 ,"IR doesn't work!"
                assert dut.AC.value == 0x0001, "AC doesn't work!"
                assert dut.DR.value == 0x0000 ,"DR doesn't work!"
            case 7:
                assert dut.PC.value == 0x0012,"PC doesn't work!"       
                assert dut.AR.value == 0x0011 ,"AR doesn't work!"
                assert dut.IR.value == 0x2740 ,"IR doesn't work!"
                assert dut.AC.value == 0x0001 ,"AC doesn't work!"
                assert dut.DR.value == 0x0000, "DR doesn't work!"
            case 8:
                assert dut.PC.value == 0x0012 ,"Direct LDA doesn't work!"                
                assert dut.AR.value == 0x0740, "IR not loaded properly !"
                assert dut.IR.value == 0x2740 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0001 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"
            case 9:
                assert dut.PC.value == 0x0012, "IR not loaded properly !"
                assert dut.AR.value == 0x0740 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x2740 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0030 ,"Direct LDA doesn't work!"
            case 10:
                assert dut.PC.value == 0x0012, "IR not loaded properly !"
                assert dut.AR.value == 0x0740 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x2740 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0030 ,"LDA instruction doesn't work"   #2nd instruction succesfully finished
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"
            case 11:
                assert dut.PC.value == 0x0012, "IR not loaded properly !"
                assert dut.AR.value == 0x0012 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x2740 ,"Direct LDA doesn't work!"   #Fetch of 3rd Instruction ---- AND Memory word to Accumulator
                assert dut.AC.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"  
            case 12:
                assert dut.PC.value == 0x0013, "IR not loaded properly !"
                assert dut.AR.value == 0x0012 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x0800 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"  
            case 13:
                assert dut.PC.value == 0x0013, "IR not loaded properly !"
                assert dut.AR.value == 0x0012 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x0800 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"  
            case 14:
                assert dut.PC.value == 0x0013, "IR not loaded properly !"
                assert dut.AR.value == 0x0800 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x0800 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"  
            case 15:
                assert dut.PC.value == 0x0013, "IR not loaded properly !"
                assert dut.AR.value == 0x0800 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x0800 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x00F1 ,"Direct LDA doesn't work!" 
            case 16:
                assert dut.PC.value == 0x0013, "IR not loaded properly !"
                assert dut.AR.value == 0x0800 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x0800 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x00F1 ,"Direct LDA doesn't work!"  
            case 17:
                assert dut.PC.value == 0x0013, "IR not loaded properly !"
                assert dut.AR.value == 0x0800 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x0800 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0030 ,"AND instruction doesn't work!"   #3rd instruction finished succesfully, 
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!" 
            case 18:
                assert dut.PC.value == 0x0013, "IR not loaded properly !"
                assert dut.AR.value == 0x0013 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x0800 ,"Direct LDA doesn't work!" #Fetch of 4tf instruction --- ADD memory word to Accumulator
                assert dut.AC.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"       
            case 19:
                assert dut.PC.value == 0x0014, "IR not loaded properly !"
                assert dut.AR.value == 0x0013 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x1900 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!" 
            case 20:
                assert dut.PC.value == 0x0014, "IR not loaded properly !"
                assert dut.AR.value == 0x0013 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x1900 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!" 
            case 21:
                assert dut.PC.value == 0x0014, "IR not loaded properly !"
                assert dut.AR.value == 0x0900 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x1900 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"
            case 22:
                assert dut.PC.value == 0x0014, "IR not loaded properly !"
                assert dut.AR.value == 0x0900 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x1900 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x1000 ,"Direct LDA doesn't work!" 
            case 23:
                assert dut.PC.value == 0x0014, "IR not loaded properly !"
                assert dut.AR.value == 0x0900 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x1900 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x1000 ,"Direct LDA doesn't work!"
            case 24:
                assert dut.PC.value == 0x0014, "IR not loaded properly !"
                assert dut.AR.value == 0x0900 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x1900 ,"Direct LDA doesn't work!" #4th instruction succesfuly finished
                assert dut.AC.value == 0x1030 ,"ADD Instruction doesn't work"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!" 
            case 25:
                assert dut.PC.value == 0x0014, "IR not loaded properly !"
                assert dut.AR.value == 0x0014 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x1900 ,"Direct LDA doesn't work!"  #Fetch of 5th instruction ---- Complement Accumulator
                assert dut.AC.value == 0x1030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"
            case 26:
                assert dut.PC.value == 0x0015, "IR not loaded properly !"
                assert dut.AR.value == 0x0014 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x7200 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x1030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!" 
            case 27:
                assert dut.PC.value == 0x0015, "IR not loaded properly !"
                assert dut.AR.value == 0x0014 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x7200 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x1030 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!" 
            case 28:
                assert dut.PC.value == 0x0015, "IR not loaded properly !"
                assert dut.AR.value == 0x0014 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x7200 ,"Complement Accumulator instruction doesn't work!" #5th instruction succesfuly finished
                assert dut.AC.value == 0xEFCF ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!" 
            case 29:
                assert dut.PC.value == 0x0015, "IR not loaded properly !"
                assert dut.AR.value == 0x0015 ,"Direct LDA doesn't work!" #Fetch of 6th instruction --- Store Accumulator to memory
                assert dut.IR.value == 0x7200 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0xEFCF ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"  
            case 30:
                assert dut.PC.value == 0x0016, "IR not loaded properly !"
                assert dut.AR.value == 0x0015 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x3780 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0xEFCF ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!" 
            case 31:
                assert dut.PC.value == 0x0016, "IR not loaded properly !"
                assert dut.AR.value == 0x0015 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x3780 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0xEFCF ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!" 
            case 32:
                assert dut.PC.value == 0x0016, "IR not loaded properly !"
                assert dut.AR.value == 0x0780 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x3780 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0xEFCF ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!" 
            case 33:
                assert dut.PC.value == 0x0016, "IR not loaded properly !" #Normally, Instruction must be finished here.
                assert dut.AR.value == 0x0780 ,"Direct LDA doesn't work!" #In my code, it actually stored the value to memory exactly this cycle.
                assert dut.IR.value == 0x3780 ,"Direct LDA doesn't work!" #However, In order to see it, in my controller logic, I added one more 
                assert dut.AC.value == 0xEFCF ,"Store Accumulator doesn't work!" #cycle and at that cycle, computer takes the value from memory and put it
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!" #to the data register. Therefore it will finish in next cycle.
            case 34:
                assert dut.PC.value == 0x0016, "IR not loaded properly !"
                assert dut.AR.value == 0x0780 ,"Direct LDA doesn't work!"   #Here, 6th instruction succesfuly finished.
                assert dut.IR.value == 0x3780 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0xEFCF ,"Store Accumulator doesn't work!"
                assert dut.DR.value == 0xEFCF ,"Direct LDA doesn't work!"  
            case 35:
                assert dut.PC.value == 0x0016, "IR not loaded properly !"
                assert dut.AR.value == 0x0016 ,"Direct LDA doesn't work!"  #Fetch of 7th instruction --- Circulate Right AC and E
                assert dut.IR.value == 0x3780 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0xEFCF ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF ,"Direct LDA doesn't work!" 
            case 36:
                assert dut.PC.value == 0x0017, "IR not loaded properly !"
                assert dut.AR.value == 0x0016 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x7080 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0xEFCF ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF ,"Direct LDA doesn't work!" 
            case 37:
                assert dut.PC.value == 0x0017, "IR not loaded properly !"
                assert dut.AR.value == 0x0016 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x7080 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0xEFCF ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!" 
            case 38:
                assert dut.PC.value == 0x0017, "IR not loaded properly !"
                assert dut.AR.value == 0x0016 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x7080 ,"Circulate Right instruction doesn't work!" #7th instruction succesfuly finished.
                assert dut.AC.value == 0x77E7 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
            case 39:
                assert dut.PC.value == 0x0017, "IR not loaded properly !"
                assert dut.AR.value == 0x0017 ,"Direct LDA doesn't work!" #Fetch of 8th instruction ---- CLEAR E
                assert dut.IR.value == 0x7080 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x77E7 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!" 
            case 40:
                assert dut.PC.value == 0x0018, "IR not loaded properly !"
                assert dut.AR.value == 0x0017 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x7400 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x77E7 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!" 
            case 41:
                assert dut.PC.value == 0x0018, "IR not loaded properly !"
                assert dut.AR.value == 0x0017 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x7400 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x77E7 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!" 
            case 42:
                assert dut.PC.value == 0x0018, "IR not loaded properly !"
                assert dut.AR.value == 0x0017 ,"Direct LDA doesn't work!"  #8th instruction succesfuly finished.
                assert dut.IR.value == 0x7400 ,"Direct LDA doesn't work!"   #When you make the file -- you will see E is 0 at clock_cycle 43.
                assert dut.AC.value == 0x77E7 ,""
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.E_carryout.value == 0x0, "Clear E is not working properly" 
            case 43:
                assert dut.PC.value == 0x0018, "IR not loaded properly !"
                assert dut.AR.value == 0x0018 ,"Direct LDA doesn't work!"   #Fetch of 9th instruction --- BUN 030
                assert dut.IR.value == 0x7400 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x77E7 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!" 
            case 44:
                assert dut.PC.value == 0x0019, "IR not loaded properly !"
                assert dut.AR.value == 0x0018 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x4030 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x77E7 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!" 
            case 45:
                assert dut.PC.value == 0x0019, "IR not loaded properly !"
                assert dut.AR.value == 0x0018 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x4030 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x77E7 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
            case 46:
                assert dut.PC.value == 0x0019, "IR not loaded properly !"
                assert dut.AR.value == 0x0030 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x4030 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x77E7 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
            case 47:
                assert dut.PC.value == 0x0030, "BUN doesn't work !"
                assert dut.AR.value == 0x0030 ,"BUN doesn't work!"   
                assert dut.IR.value == 0x4030 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x77E7 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
            case 48:
                assert dut.PC.value == 0x0030, "IR not loaded properly !"
                assert dut.AR.value == 0x0030, "Direct LDA doesn't work!"  #Fetch of 10th instruction ---- Clear Accumulator
                assert dut.IR.value == 0x4030 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x77E7 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
            case 49:
                assert dut.PC.value == 0x0031, "IR not loaded properly !"
                assert dut.AR.value == 0x0030 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0x7800 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x77E7 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
            case 50:
                dut.FGI.value = 1
                assert dut.PC.value == 0x0031, "IR not loaded properly !"
                assert dut.AR.value == 0x0030 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0x7800 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x77E7 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
            case 51:
                assert dut.PC.value == 0x0031, "IR not loaded properly !"
                assert dut.AR.value == 0x0030 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0x7800 ,"Direct LDA doesn't work!" #10th instruction has been finished succesfuly!
                assert dut.AC.value == 0x0000 ,"CLA instruction doesn't work"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
            case 52:
                assert dut.PC.value == 0x0031, "IR not loaded properly !"
                assert dut.AR.value == 0x0031 ,"Direct LDA doesn't work!"  #Fetch of Instruction ION 
                assert dut.IR.value == 0x7800 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"
            case 53:
                assert dut.PC.value == 0x0032, "IR not loaded properly !"
                assert dut.AR.value == 0x0031 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0xF080 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"

            case 54:
                assert dut.PC.value == 0x0032, "IR not loaded properly !"
                assert dut.AR.value == 0x0031 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0xF080 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"

            case 55:
                assert dut.PC.value == 0x0032, "IR not loaded properly !"
                assert dut.AR.value == 0x0031 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0xF080 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x1, "IEN do not work!" #Instruction ION is succesfully finished!

            case 56:
                assert dut.PC.value == 0x0032, "IR not loaded properly !"
                assert dut.AR.value == 0x0032 ,"Direct LDA doesn't work!"   #Fetch of instruction IOF 
                assert dut.IR.value == 0xF080 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x1, "IEN do not work!"

            case 57:
                assert dut.PC.value == 0x0033, "IR not loaded properly !"
                assert dut.AR.value == 0x0032 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0xF040 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x1, "IEN do not work!"

            case 58:
                assert dut.PC.value == 0x0033, "IR not loaded properly !"
                assert dut.AR.value == 0x0032 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0xF040 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x1, "IEN do not work!"

            case 59:
                assert dut.PC.value == 0x0033, "IR not loaded properly !"
                assert dut.AR.value == 0x0032 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0xF040 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"  #Instruction IOF is succesfuly finished!
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"

            case 60:
                assert dut.PC.value == 0x0033, "IR not loaded properly !"
                assert dut.AR.value == 0x0000 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0xF040 ,"Direct LDA doesn't work!"   #Fetch of interrupt cycle has started
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"   
            case 61:
                assert dut.PC.value == 0x0000, "IR not loaded properly !"
                assert dut.AR.value == 0x0000 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0xF040 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"
            case 62:
                assert dut.PC.value == 0x0001, "IR not loaded properly !"
                assert dut.AR.value == 0x0000 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0xF040 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"
            case 63:
                assert dut.PC.value == 0x0001, "IR not loaded properly !"
                assert dut.AR.value == 0x0001 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0xF040 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"
            case 64:
                assert dut.PC.value == 0x0002, "IR not loaded properly !"
                assert dut.AR.value == 0x0001 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0x4250 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"
            case 65:
                assert dut.PC.value == 0x0002, "IR not loaded properly !"
                assert dut.AR.value == 0x0001 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0x4250 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"
            case 66:
                assert dut.PC.value == 0x0002, "IR not loaded properly !"
                assert dut.AR.value == 0x0250 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0x4250 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"
            case 67:
                assert dut.PC.value == 0x0250, "IR not loaded properly !"
                assert dut.AR.value == 0x0250 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0x4250 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"
            case 68:
                assert dut.PC.value == 0x0250, "IR not loaded properly !"
                assert dut.AR.value == 0x0250 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0x4250 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"
            case 69:
                assert dut.PC.value == 0x0251, "IR not loaded properly !"
                assert dut.AR.value == 0x0250 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0x4000 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"
            case 70:
                assert dut.PC.value == 0x0251, "IR not loaded properly !"
                assert dut.AR.value == 0x0250 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0x4000 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"
            case 71:
                assert dut.PC.value == 0x0251, "IR not loaded properly !"
                assert dut.AR.value == 0x0000 ,"Direct LDA doesn't work!"   
                assert dut.IR.value == 0x4000 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0xEFCF,"Direct LDA doesn't work!"
                assert dut.datapath_inst.op_of_ien == 0x0, "IEN do not work!"
            

            



            case _:
                dut._log.info(f"Cycle count: {cycle} \n")
    
    dut._log.info("BC I test ended successfully!")

"""
    case 11:
                assert dut.PC.value == 0x0002, "IR not loaded properly !"
                assert dut.AR.value == 0x0002 ,"Direct LDA doesn't work!"   #Fetch of 3rd instruction --- Clear Accumulator
                assert dut.IR.value == 0x2740 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0020 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"
            case 12:
                assert dut.PC.value == 0x0003, "IR not loaded properly !"
                assert dut.AR.value == 0x0002 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x7800 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0020 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"
            case 13:
                assert dut.PC.value == 0x0003, "IR not loaded properly !"
                assert dut.AR.value == 0x0002 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x7800 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0020 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"
            case 14:
                assert dut.PC.value == 0x0003, "IR not loaded properly !"
                assert dut.AR.value == 0x0002 ,"Direct LDA doesn't work!"
                assert dut.IR.value == 0x7800 ,"Direct LDA doesn't work!"
                assert dut.AC.value == 0x0000 ,"Direct LDA doesn't work!"
                assert dut.DR.value == 0x0000 ,"Direct LDA doesn't work!"
             """