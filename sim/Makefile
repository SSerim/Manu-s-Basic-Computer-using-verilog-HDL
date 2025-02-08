# Makefile

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

#Add your sources one by one as below or use *.v to add all verilog files
VERILOG_SOURCES += $(PWD)/BC_I.v
VERILOG_SOURCES += $(PWD)/ALU_.v
VERILOG_SOURCES += $(PWD)/Control_signal_gen.v
VERILOG_SOURCES += $(PWD)/Controller.v
VERILOG_SOURCES += $(PWD)/DataPath.v
VERILOG_SOURCES += $(PWD)/instruction_reader.v
VERILOG_SOURCES += $(PWD)/Memory.v
VERILOG_SOURCES += $(PWD)/MULX_.v
VERILOG_SOURCES += $(PWD)/Register_AC.v
VERILOG_SOURCES += $(PWD)/Register_AR.v
VERILOG_SOURCES += $(PWD)/Register_CO.v
VERILOG_SOURCES += $(PWD)/Register_DR.v
VERILOG_SOURCES += $(PWD)/Register_IEN.v
VERILOG_SOURCES += $(PWD)/Register_IR.v
VERILOG_SOURCES += $(PWD)/Register_PC.v
VERILOG_SOURCES += $(PWD)/Register_TR.v
VERILOG_SOURCES += $(PWD)/timer_signal_gen.v
VERILOG_SOURCES += $(PWD)/FF_R.v

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
#Should be the name of the basic computer module for you
TOPLEVEL = BC_I

# MODULE is the basename of the Python test file
#Name of your python file
MODULE = test

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim