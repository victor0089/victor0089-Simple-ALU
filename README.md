# Simple 8-Bit ALU and Reference CPU

**A computer architecture learning project: 14 ALU operations, a 4-bit instruction set, register/control-unit modeling, and test-driven verification.**

## Overview

An **Arithmetic Logic Unit (ALU)** is the part of a CPU that performs arithmetic, bitwise logic, comparisons, and shifts. This project explores the design of a simple **8-bit ALU** and how it fits into a small CPU architecture.

The design uses:

- **Two 8-bit operand registers:** `A` and `B` (unsigned values `0` through `255`).
- **One 4-bit opcode:** selects one of 16 instruction codes.
- **14 defined ALU operations:** arithmetic, logic, comparison, shifts, and data pass-through.
- **Two reserved branch instructions:** `JZ` and `JMP` (conceptual only).
- **An 8-bit result:** all arithmetic wraps modulo 256 (`0x100`).
- **Status flags:** `EQ`, `LT`, `GT`, and `Z` (`ZERO`).
- **A Python CPU model:** register loading, result storage, flag updates, and basic write-back.

### Features and current status

| Feature | Status | Details |
| --- | --- | --- |
| 8-bit ALU calculation | ✅ Implemented in Python | 14 operational opcodes |
| 4-bit opcode map | ✅ Documented | 16 codes, including two reservations |
| Two operand registers | ✅ Modeled in Python | `A` and `B`; `R` stores the result |
| Basic register write-back | ✅ Modeled in Python | `A` receives normal operation results |
| Status flags | ✅ Modeled in Python | `EQ/LT/GT` on comparison; `Z` on result |
| Automated tests | ✅ Passing | 7 unit tests |
| CSV test vectors | ✅ Checked | 84 expected input/output cases |

## Architecture

```text
                  OPCODE [3:0]
                       |
                       v
              +------------------+
              |  Control / ALU   |
              | Operation Select |
              +------------------+
                       |
  Register A [7:0] ---+---+--- Register B [7:0]
                          |
                          v
                  +---------------+
                  | 8-bit ALU     |
                  | 14 operations |
                  +---------------+
                          |
                 16-to-1 selection
                (8-bit-wide MUX)
                          |
            +-------------+-------------+
            |                           |
            v                           v
        Result [7:0]             EQ, LT, GT, Z
            |
            v
      Result register R
            |
            +----> A (write-back except CMP)
```

This diagram represents the **intended design**, not a Logisim screenshot or proof of a working circuit. The model writes back to `A` on non-comparison ALU operations; a real Logisim circuit also needs clock, load, and write-enable wiring.

## Instruction set

The ALU's first **nine instructions** are the required operations. Five additional operations make **14 ALU instructions**; the final two opcode values are reserved for branching.

| Binary opcode | Hex | Mnemonic | Meaning | Category |
| --- | --- | --- | --- | --- |
| `0000` | `0x0` | `ADD` | `(A + B) & 0xFF` | Required |
| `0001` | `0x1` | `INC` | `(A + 1) & 0xFF` | Required |
| `0010` | `0x2` | `DEC` | `(A - 1) & 0xFF` | Required |
| `0011` | `0x3` | `CMP` | Compare unsigned `A` and `B`; set `EQ/LT/GT`; result `0` | Required |
| `0100` | `0x4` | `NOT` | `(~A) & 0xFF` | Required |
| `0101` | `0x5` | `AND` | `A & B` | Required |
| `0110` | `0x6` | `OR` | `A \| B` | Required |
| `0111` | `0x7` | `SHR` | Logical right shift `A >> 1` | Required |
| `1000` | `0x8` | `SHL` | Logical left shift `(A << 1) & 0xFF` | Required |
| `1001` | `0x9` | `SUB` | `(A - B) & 0xFF` | Additional |
| `1010` | `0xA` | `XOR` | `A ^ B` | Additional |
| `1011` | `0xB` | `NAND` | `(~(A & B)) & 0xFF` | Additional |
| `1100` | `0xC` | `NOR` | `(~(A \| B)) & 0xFF` | Additional |
| `1101` | `0xD` | `PASS` | Copy `A` | Additional |
| `1110` | `0xE` | `JZ` | Jump when `Z = 1` | Reserved; not executed by ALU |
| `1111` | `0xF` | `JMP` | Unconditional jump | Reserved; not executed by ALU |

**Why the five additions?** `SUB` finds differences; `XOR` detects or toggles changed bits; `NAND` and `NOR` are universal logic operations; `PASS` provides a simple data-transfer path. The accompanying report expands on these choices.

### Result and flag behavior

- All input operands are **unsigned 8-bit integers**.
- Addition, subtraction, increment, decrement, and left shift **truncate to eight bits**.
- `SHR` and `SHL` are **logical** shifts; empty positions fill with zero.
- `CMP` returns an ALU result of **zero**, while `EQ`, `LT`, and `GT` indicate unsigned comparison outcomes.
- `Z` is `1` **whenever the ALU result is zero**. Therefore, `CMP` produces `Z = 1` regardless of whether `A == B`; use **`EQ`**, not `Z`, to interpret comparison equality.
- `EQ`, `LT`, and `GT` are all zero for non-`CMP` operations in the current Python model.
- Carry, signed overflow, negative flags, and memory access are **not implemented**.

## Repository files

```text
.
├── README.md                         # This GitHub documentation
├── alu_reference.py                  # ALU logic, CPU state, example program models
├── test_alu.py                        # Python unittest suite
├── opcode_table.csv                  # Full 16-opcode instruction table
├── logisim_test_vectors.csv          # 84 verification cases for Logisim/manual testing
└── test_results.txt                  # Snapshot of a previous Python test run
```

## Requirements

- **Python 3.8+** recommended.
- A terminal: **PowerShell**, Command Prompt, macOS Terminal, or Linux shell.
- **No pip packages required**: the code uses only the Python standard library.
- **Logisim** or **Logisim-evolution** is needed only when you build the separate digital circuit.

## Quick start

### 1. Download the files

Download the repository as ZIP from GitHub and extract it, or clone your repository:

```bash
git clone https://github.com/victor0089/Simple-ALU.git
cd Simple-ALU
```


### 1. Run the automated tests

```bash
python -m unittest -v test_alu
```

On some Windows setups, use `py` instead of `python`:

```powershell
py -m unittest -v test_alu
```

**Expected summary:** `Ran 7 tests` followed by `OK`.

### 2. Run an ALU operation

From the same directory:

```bash
python -c "from alu_reference import execute; print(execute('ADD', 0xAA, 0xCC))"
```

Expected output:

```text
(118, 0, 0, 0, 0)
```

The result tuple is always:

```python
(result, EQ, LT, GT, ZERO)
```

`118` is `0x76`, the 8-bit result of `0xAA + 0xCC` (which wraps around modulo 256).

More examples:

```python
from alu_reference import execute

print(execute('AND', 0b10101010, 0b11001100))
# (136, 0, 0, 0, 0)   136 = 0x88

print(execute('CMP', 4, 8))
# (0, 0, 1, 0, 1)     A < B; CMP always returns result 0

print(execute('SHR', 13))
# (6, 0, 0, 0, 0)     00001101 -> 00000110
```

Execute multiline examples using the Python interpreter (`python` or `py`), then paste the code; exit with `exit()`.

## Using the CPU model

`ReferenceCPU` stores two operand registers (`A`, `B`), a result register (`R`), and four flags (`Z`, `EQ`, `LT`, `GT`). Load operands, then execute a **numeric** opcode.

```python
from alu_reference import ReferenceCPU

cpu = ReferenceCPU()
cpu.load(a=7, b=3)

result = cpu.clock_instruction(0)  # 0000 = ADD
print(result)   # 10
print(cpu.A)    # 10: written back into A
print(cpu.B)    # 3: unchanged
print(cpu.R)    # 10: last result

cpu.load(a=0b10101010, b=0b11001100)
print(cpu.clock_instruction(5))  # 0101 = AND -> 136

cpu.load(a=0b10101010)
print(cpu.clock_instruction(7))  # 0111 = SHR -> 85
```

**Implementation note:** `execute()` accepts a mnemonic string or numeric opcode, but `ReferenceCPU.clock_instruction()` should be called using **numeric opcodes** in this version. Its special `CMP` write-back check compares the opcode with integer `3`.

This is a **Python state model**, not a simulator of gate propagation or clock timing.

## Example program models (Phase Four)

The assignment requests two assembly programs. This package includes equivalent **Python reference helpers** and **conceptual assembly pseudocode** in the report; it does **not** contain an assembler, instruction memory, or an executable branch-capable CPU.

### Program 1 — Sum numbers until the next input is zero

```python
from alu_reference import sum_until_zero

print(sum_until_zero([5, 3, 9, 0, 88]))
# 17
```

The values `5`, `3`, and `9` are added. The first zero ends the loop, so `88` is not processed. The example assumes an **external input step** refreshes register `B`, as permitted for the assignment's conceptual program.

### Program 2 — Shift until the least-significant bit is zero

```python
from alu_reference import shift_until_lsb_zero_or_ff

print(shift_until_lsb_zero_or_ff(13))
# (6, 1, 'lsb_zero')

print(shift_until_lsb_zero_or_ff(255))
# (255, 0, 'all_ones_guard')
```

The program checks the special input `11111111` (`255`) **before shifting**, then checks whether the least-significant bit is already zero. If neither stopping condition applies, it performs `SHR` and repeats.

**Important:** The assembly descriptions use conceptual conditions and external flag checks. `JZ`/`JMP` are reserved, not implemented, and pseudo-operations such as `HALT`, `INPUT_B`, or `IF` are **not real machine instructions** in the given 16-opcode table.

## Building the circuit in Logisim

The package provides the intended architecture and data for checking one, but no `.circ` file. Use the following sequence as a construction guide:

1. Start a new Logisim circuit and add **8-bit inputs** `A` and `B` and a **4-bit input** `OPCODE`.
2. Build the nine required operation blocks: **ADD**, **INC**, **DEC**, **CMP**, **NOT**, **AND**, **OR**, **SHR**, and **SHL**.
3. If implementing the five optional operations too, add **SUB**, **XOR**, **NAND**, **NOR**, and **PASS**.
4. Configure a **multiplexer** with **four select bits** (16 inputs) and **8-bit data width**. Connect each ALU result bus to the input matching its numeric opcode.
5. Tie unused MUX inputs `14` and `15` to zero; the corresponding branch opcodes are not ALU results.
6. Export three **unsigned comparator outputs** (`EQ`, `LT`, `GT`) and an **8-bit result output**; derive the zero flag from the selected result.
7. Add **two 8-bit registers**, one each for `A` and `B`. Provide separate external load controls so inputs can be loaded without triggering unintended write-back.
8. Connect register outputs to ALU inputs and route the selected ALU result through the write-back path to `A`.
9. Design a control unit that correctly selects and clocks at least **ADD (`0000`)**, **AND (`0101`)**, and **SHR (`0111`)**. Prevent writing `A` on `CMP`.
10. Use single clock steps and probes to check the **ALU result, flags, register values, and write-back enable**.
11. Record real Logisim screenshots and test outcomes for the assignment. Do not report Python-only results as hardware testing.

### Manual verification examples

| Opcode | A (hex) | B (hex) | Expected result | Expected flags |
| --- | --- | --- | --- | --- |
| `0000` ADD | `FF` | `01` | `00` | `Z=1` |
| `0001` INC | `FF` | `01` | `00` | `Z=1` |
| `0010` DEC | `00` | `01` | `FF` | `Z=0` |
| `0011` CMP | `04` | `08` | `00` | `EQ=0, LT=1, GT=0, Z=1` |
| `0100` NOT | `AA` | `CC` | `55` | `Z=0` |
| `0101` AND | `AA` | `CC` | `88` | `Z=0` |
| `0110` OR | `AA` | `CC` | `EE` | `Z=0` |
| `0111` SHR | `AA` | `CC` | `55` | `Z=0` |
| `1000` SHL | `AA` | `CC` | `54` | `Z=0` |
| `1001` SUB | `04` | `08` | `FC` | `Z=0` |
| `1010` XOR | `AA` | `CC` | `66` | `Z=0` |
| `1011` NAND | `AA` | `CC` | `77` | `Z=0` |
| `1100` NOR | `AA` | `CC` | `11` | `Z=0` |
| `1101` PASS | `AA` | `CC` | `AA` | `Z=0` |

For the complete **84-case test matrix**, see [`logisim_test_vectors.csv`](logisim_test_vectors.csv). These are the result values from the Python model

## Testing and verification

Tests are implemented with Python's built-in `unittest` framework:

```bash
python -m unittest -v test_alu
```

Tests cover: all 14 ALU opcodes, three comparison outcomes, 8-bit wraparound, rejection of reserved branch opcodes, reference CPU operations, and the two Python program helpers.

**Verified for this package:** 7 tests passed and all 84 CSV test vectors were checked against the Python implementation. This **does not validate an unbuilt Logisim circuit**.

## Known limitations

- No interactive desktop or web GUI is included; run the app as **Python code**.
- No Logisim `.circ` circuit is included; a real 8-bit ALU, MUX, registers, and control unit remain to be built and tested.
- The architecture is intentionally minimal: no RAM, program counter, instruction ROM, assembler, implemented branch execution, or `HALT` instruction.
- The CPU model is not cycle-accurate; `clock_instruction()` updates Python state immediately.
- The Phase Four assembly examples are **conceptual**, not binary programs executable by this model.
- All arithmetic uses **unsigned bytes with wraparound**; signed behavior, carry, and overflow handling are omitted.

## Project phases and documentation

| Phase | Goal | Reference materials |
| --- | --- | --- |
| **One** | Nine required operations plus five justified additions | Opcode table, Python model, report |
| **Two** | Opcode design, operand choice, operation-selection MUX | `opcode_table.csv`, architecture above |
| **Three** | Registers and control logic for ADD, AND, SHR | `ReferenceCPU`, hardware build guide |
| **Four** | Two assembly programs using conceptual branching | Program helpers and pseudocode in report |

