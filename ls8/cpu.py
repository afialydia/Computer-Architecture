"""CPU functionality."""

import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
IRET = 0b00010011
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JNE = 0b01010110
JEQ = 0b01010101

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
      
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.sp = 0xf3
        self.flag = [0] * 8
      
        

    def load(self):
        """Load a program into memory."""
        address = 0
        filename = sys.argv[1]

        with open(filename) as program:
           
            for line in program:
                
                line = line.split('#')
              
                line = line[0].strip()

                if line == '':
                    continue
                self.ram[address] = int(line, 2)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        
        elif op == 'MUL':
            self.register[reg_a] *= self.register[reg_b]
        
        elif op == 'CMP':
            if self.register[reg_a] == self.register[reg_b]:
                self.flag =  0b00000001
            
            elif self.register[reg_a] < self.register[reg_b]:
                self.flag = 0b00000100
            
            elif self.register[reg_a] > self.register[reg_b]:
                self.flag = 0b00000010
        
        else:
            raise Exception("Unsupported ALU operation")
    
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        running = True
        while running:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == HLT:
         
                running = False
            
            elif instruction == CALL:
           
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2
                self.pc = self.register[operand_a]
                

            elif instruction == RET:
               
                # popped = self.ram[self.sp]
                # self.pc = popped
                self.pc = self.ram[self.sp]
                self.sp += 1
            
            elif instruction == PUSH:
                self.sp -= 1
                self.ram[self.sp] = self.register[operand_a]
                self.pc += 2

            elif instruction == POP:
                self.register[operand_a] = self.ram[self.sp]
                self.sp += 1
                self.pc += 2
            
            elif instruction == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3
            
            elif instruction == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            
            elif instruction == ADD:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3

            elif instruction == PRN:
                value = self.register[operand_a]
                print(value)
                self.pc += 2

            elif instruction == CMP:
                self.alu('CMP', operand_a, operand_b)
                self.pc += 3

            elif instruction == JMP:
                self.pc = self.register[self.ram_read(self.pc + 1)]

            elif instruction == JNE:
                if not self.flag_check():
                    reg_num = self.ram[self.pc + 1]
                    self.pc = self.register[reg_num]
                else:
                    self.pc += 2

            elif instruction == JEQ:
                if self.flag_check():
                    reg_num = self.ram[self.pc + 1]
                    self.pc = self.register[reg_num]
                else:
                    self.pc += 2

           
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value 
    
    def flag_check(self):
        return (self.flag == 1)