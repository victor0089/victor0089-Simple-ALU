"""Static structural checks only. This is NOT a Logisim simulation."""
from pathlib import Path
from lxml import etree as E
import unittest, re
PROJECT=Path(__file__).with_name('Simple_8bit_ALU.circ')
class CircuitIntegrity(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.root=E.parse(str(PROJECT)).getroot()
    cls.alu=cls.root.xpath('./circuit[@name="ALU_8BIT"]')[0]
    cls.cpu=cls.root.xpath('./circuit[@name="CPU_8BIT"]')[0]
  @staticmethod
  def attrs(comp):return {a.get('name'):a.get('val') for a in comp.findall('a')}
  def assert_tunnel(self,circuit, label,at_least=1):
    return self.assertGreaterEqual(sum(1 for c in circuit.findall('comp') if c.get('name')=='Tunnel' and self.attrs(c).get('label')==label),at_least,label)
  def test_xml_format(self):
    self.assertEqual(self.root.get('source'),'2.7.1')
    self.assertEqual(self.root.find('main').get('name'),'CPU_8BIT')
  def test_14_operations_all_mux_inputs(self):
    mux=[c for c in self.alu.findall('comp') if c.get('name')=='Multiplexer']
    self.assertEqual(len(mux),1)
    self.assertEqual(self.attrs(mux[0]).get('select'),'4')
    self.assertEqual(self.attrs(mux[0]).get('width'),'8')
    for idx in range(14):
      self.assert_tunnel(self.alu,f'D{idx}',at_least=2)
  def test_instructions_and_zero_flag(self):
    for name in ['Adder','Subtractor','Shifter','Comparator','NOT Gate','AND Gate','OR Gate','XOR Gate','NAND Gate','NOR Gate']:
      self.assertIn(name,[c.get('name') for c in self.alu.findall('comp')])
    for name in ['A','B','OPCODE','RESULT','EQ','LT','GT','Z']:
      self.assertIn(name,[self.attrs(c).get('label') for c in self.alu.findall('comp') if c.get('name')=='Pin'])
  def test_cpu_registers_and_control(self):
    regs=[c for c in self.cpu.findall('comp') if c.get('name')=='Register']
    self.assertEqual(len(regs),3)
    for c in regs:self.assertEqual(self.attrs(c).get('width'),'8')
    self.assertEqual(len([c for c in self.cpu.findall('comp') if c.get('name')=='ALU_8BIT']),1)
    for sig in ['CLK','RESET','DATA_A','DATA_B','LOAD_A','LOAD_B','EXEC','A_WRITE_EN','EXEC_VALID','WB_SELECT']:
      self.assert_tunnel(self.cpu,sig)
  def test_orthogonal_grid(self):
    for circuit in [self.alu,self.cpu]:
      for c in circuit.findall('comp'):
        x,y=map(int,re.findall(r'-?\d+',c.get('loc')))
        self.assertEqual(x%10,0,c.get('loc'))
        self.assertEqual(y%10,0,c.get('loc'))
      for w in circuit.findall('wire'):
        x1,y1=map(int,re.findall(r'-?\d+',w.get('from')))
        x2,y2=map(int,re.findall(r'-?\d+',w.get('to')))
        self.assertTrue(x1==x2 or y1==y2,(x1,y1,x2,y2))
        self.assertTrue(all(a%10==0 for a in (x1,y1,x2,y2)))
  def test_symbol_pin_mapping(self):
    appear=self.alu.find('appear')
    self.assertIsNotNone(appear)
    self.assertEqual(len(appear.findall('circ-port')),8)
    pins={c.get('pin') for c in appear.findall('circ-port')}
    self.assertEqual(len(pins),8)
if __name__=='__main__':unittest.main(verbosity=2)
