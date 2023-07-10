
import ctypes

class Coprocessor:
    
    def __init__(self):
        self._analyze()
        
    def _txt_in_list(self):
        B = []
        f = open('commands.txt')
        for line in f.readlines():
            line = line.replace("\n","").replace(",","")
            A = line.split(" ")
            B.append(A)
        return B

    def _analyze(self):
        self._PC = 0
        self._TC = 2
        self._StackPointer = 0
        self._reg_l = [0,0,0,0,0,0,0,0]
        self._reg_l_in754 = [self._in754(self._reg_l[0]), self._in754(self._reg_l[1]), self._in754(self._reg_l[2]), self._in754(self._reg_l[3]), self._in754(self._reg_l[4]), self._in754(self._reg_l[5]), self._in754(self._reg_l[6]), self._in754(self._reg_l[7])]
        txt_list = self._txt_in_list()
        self.StackPointer = 0
        for self._i in txt_list:
            self._command = self._i[0]
            if self._command == "push":
                self._push()
                self.print1()
            elif self._command == "dup":
                self._dup()
                self.print1()
            elif self._command == "add":
                self._add()
                self.print1()
            elif self._command == "rev":
                self._rev()
                self.print1()
            elif self._command == "div":
                self._div()
                self.print1()
            else:
                print("Введена неправильна команда")
                
    def _in754(self, num):
        x = bin(ctypes.c_uint.from_buffer(ctypes.c_float(num)).value)
        return x.replace('0b', '').rjust(32, '0')
    
    def _push(self):
        self._reg_l_in754[self.StackPointer] = self._in754(float(self._i[1]))
        self._reg_l[self.StackPointer] = float(self._i[1])
        self.StackPointer += 1
        if self._reg_l[self.StackPointer - 1] < 0:
            self._PS = 1
        elif self._reg_l[self.StackPointer - 1] >= 0:
            self._PS = 0
    
    def _dup(self):
        self._reg_l_in754[self.StackPointer] =  self._reg_l_in754[self.StackPointer - 1]
        self._reg_l[self.StackPointer] = self._reg_l[self.StackPointer - 1]
        self.StackPointer += 1
        if self._reg_l[self.StackPointer - 1] < 0:
            self._PS = 1
        elif self._reg_l[self.StackPointer - 1] >= 0:
            self._PS = 0
    
    def _add(self):
        self._reg_l[self.StackPointer - 2] += self._reg_l[self.StackPointer - 1]
        self._reg_l_in754[self.StackPointer - 2] = self._in754(float(self._reg_l[self.StackPointer - 2]))
        self.StackPointer -= 1
        if self._reg_l[self.StackPointer - 3] < 0:
            self._PS = 1
        elif self._reg_l[self.StackPointer - 3] >= 0:
            self._PS = 0
        
    def _rev(self):
        q = self._reg_l_in754[self.StackPointer - 1]
        self._reg_l_in754[self.StackPointer - 1] = self._reg_l_in754[self.StackPointer - 2]
        self._reg_l_in754[self.StackPointer - 2] = q
        
        q1 = self._reg_l[self.StackPointer - 1]
        self._reg_l[self.StackPointer - 1] = self._reg_l[self.StackPointer - 2]
        self._reg_l[self.StackPointer - 2] = q1
        if self._reg_l[self.StackPointer - 2] < 0:
            self._PS = 1
        elif self._reg_l[self.StackPointer - 2] >= 0:
            self._PS = 0
        
    def _div(self):
        self._reg_l[self.StackPointer - 2] = (self._reg_l[self.StackPointer - 1])/(self._reg_l[self.StackPointer - 2])
        self._reg_l_in754[self.StackPointer - 2] = self._in754(float(self._reg_l[self.StackPointer - 2]))
        self.StackPointer -= 1
        if self._reg_l[self.StackPointer - 2] < 0:
            self._PS = 1
        elif self._reg_l[self.StackPointer - 2] >= 0:
            self._PS = 0
   
    def print1(self):
        self._PC += 1
        print("IR = ", self._i[0])
        print("R0 = ", self._reg_l_in754[0])
        print("R1 = ", self._reg_l_in754[1])
        print("R2 = ", self._reg_l_in754[2])
        print("R3 = ",self._reg_l_in754[3])
        print("R4 = ",self._reg_l_in754[4])
        print("R5 = ",self._reg_l_in754[5])
        print("R6 = ",self._reg_l_in754[6])  
        print("R7 = ",self._reg_l_in754[7])
        print("Stack Pointer is in ", self.StackPointer + 1, " string")
        print("PC = ", self._PC)
        print("TC = ",self._TC)
        if self._PS == 0:
            print("PS =  +")
        elif self._PS == 1:
            print("PS =  -")
        
Coprocessor()       