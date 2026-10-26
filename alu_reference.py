"""Educational reference CPU / ALU model. Not a substitute for Logisim hardware."""
from dataclasses import dataclass
MNEMONICS = ('ADD','INC','DEC','CMP','NOT','AND','OR','SHR','SHL','SUB','XOR','NAND','NOR','PASS','JZ','JMP')

def execute(op, a, b=0):
    """Unsigned 8-bit ALU. Returns (8-bit result, EQ, LT, GT, ZERO)."""
    if not (0 <= a <= 255 and 0 <= b <= 255):
        raise ValueError('Operands must be unsigned bytes')
    if isinstance(op, str):
        op = MNEMONICS.index(op.upper())
    if not (0 <= op <= 13):
        raise ValueError('14 and 15 are reserved for branching, not ALU operations')
    results = ((a+b)&255, (a+1)&255, (a-1)&255, 0, (~a)&255,
               a&b, a|b, a>>1, (a<<1)&255, (a-b)&255, a^b,
               (~(a&b))&255, (~(a|b))&255, a)
    return results[op], int(op==3 and a==b), int(op==3 and a<b), int(op==3 and a>b), int(results[op]==0)

@dataclass
class ReferenceCPU:
    # Proposed two-register, A-destination architecture. R stores last ALU result.
    A:int=0
    B:int=0
    R:int=0
    Z:int=0
    EQ:int=0
    LT:int=0
    GT:int=0

    def load(self, a=None, b=None):
        if a is not None:
            if not 0 <= a <= 255: raise ValueError('A must be byte')
            self.A=a
        if b is not None:
            if not 0 <= b <= 255: raise ValueError('B must be byte')
            self.B=b

    def clock_instruction(self, opcode):
        op = (
            MNEMONICS.index(opcode.upper())
            if isinstance(opcode, str)
            else opcode
        )

        result, eq, lt, gt, zero = execute(
            op, self.A, self.B
        )

        self.R = result
        self.Z = zero
        self.EQ = eq
        self.LT = lt
        self.GT = gt

        if op != 3:
            self.A = result

        return result


def sum_until_zero(sequence):
    """Treat input B as externally refreshed each iteration; wrap at 8 bits."""
    cpu=ReferenceCPU(A=0)
    for value in sequence:
        cpu.load(b=value)
        if cpu.B==0: return cpu.A
        cpu.clock_instruction(0)
    raise ValueError('Missing terminating zero input')

def shift_until_lsb_zero_or_ff(start):
    """Stops BEFORE shifting if A==0xFF; stops if LSB==0; else shift right."""
    cpu=ReferenceCPU(A=start)
    steps=0
    while True:
        if cpu.A==255: return cpu.A,steps,'all_ones_guard'
        if (cpu.A&1)==0: return cpu.A,steps,'lsb_zero'
        cpu.clock_instruction(7); steps+=1
