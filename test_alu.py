import unittest
from alu_reference import *
class TestALU(unittest.TestCase):
    def test_all_opcodes(self):
        a,b=0b10101010,0b11001100
        expected=[118,171,169,0,85,136,238,85,84,222,102,119,17,170]
        for opcode,y in enumerate(expected):
            with self.subTest(opcode=opcode): self.assertEqual(execute(opcode,a,b)[0],y)
    def test_compare_flags(self):
        self.assertEqual(execute('CMP',4,4)[1:4],(1,0,0))
        self.assertEqual(execute('CMP',4,8)[1:4],(0,1,0))
        self.assertEqual(execute('CMP',8,4)[1:4],(0,0,1))
    def test_wraparound(self):
        self.assertEqual(execute('ADD',255,1)[0],0)
        self.assertEqual(execute('DEC',0)[0],255)
        self.assertEqual(execute('SHL',128)[0],0)
    def test_branch_reservations(self):
        for opcode in (14,15):
            with self.assertRaises(ValueError): execute(opcode,1,2)
    def test_control_unit_reference(self):
        cpu=ReferenceCPU(A=7,B=3); self.assertEqual(cpu.clock_instruction(0),10)
        cpu.load(a=0b10101010,b=0b11001100); self.assertEqual(cpu.clock_instruction(5),136)
        cpu.load(a=0b10101010); self.assertEqual(cpu.clock_instruction(7),85)
    def test_program_one(self):
        self.assertEqual(sum_until_zero([5,3,9,0,88]),17)
    def test_program_two(self):
        self.assertEqual(shift_until_lsb_zero_or_ff(13),(6,1,'lsb_zero'))
        self.assertEqual(shift_until_lsb_zero_or_ff(255),(255,0,'all_ones_guard'))
        self.assertEqual(shift_until_lsb_zero_or_ff(4),(4,0,'lsb_zero'))
if __name__=='__main__': unittest.main(verbosity=2)
