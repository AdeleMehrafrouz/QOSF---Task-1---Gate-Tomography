# QOSF - Task 1 - Gate Tomography

## Objective

Determine the parameters of the two unknown **U3(θ, φ, λ)** gates (marked with “?”) in a given quantum circuit so that the overall circuit is equivalent to a **Toffoli (CCX)** gate.

The Toffoli gate flips the third qubit (target) only when both control qubits are |1⟩.
It is also known as a **controlled-controlled-X** gate.

---

## Understanding the Problem

The Toffoli gate can be decomposed using **single-qubit rotations** and **CNOTs**.
The decomposition typically involves **T**, **T† (T-dagger)**, and **Hadamard (H)** gates.

The standard Qiskit/IBM form of the CCX is:

```
q2: --H--T--CX--T†--CX--T--CX--T†--T--H--

```
(CNOT connections occur between control qubits q₀, q₁ and the target q₂ as in the canonical decomposition.)

task's circuit matches this but replaces two single-qubit gates with **U3(θ, φ, λ)** placeholders.

---

## Step-by-Step Reasoning

1. **U3 gate definition:**

   U3(θ, φ, λ) = [[cos(θ/2), −e^{iλ}·sin(θ/2)],
                  [e^{iφ}·sin(θ/2), e^{i(φ+λ)}·cos(θ/2)]]

2. **Known mappings:**

| Gate | Meaning      | U3(θ, φ, λ)    |
| ---- | ------------ | -------------- |
| H    | Hadamard     | U3(π/2, 0, π)  |
| T    | π/8 gate     | U3(0, 0, π/4)  |
| T†   | inverse of T | U3(0, 0, −π/4) |
| I    | identity     | U3(0, 0, 0)    |

3. **Circuit analysis:**

   * The **first “?”** (at the beginning on q₂) must be **Hadamard (H)** -- it transforms a controlled-controlled-Z (CCZ) into a controlled-controlled-X (CCX). 
   * The **second “?”** (before the final CNOT–T–H sequence) must be **T-dagger (T†)** -- it corrects residual phase accumulated during earlier CNOT and T/T† operations.

---

## Final Parameters

| Gate | Meaning  | θ   | φ | λ    | Description      |
| ---- | -------- | --- | - | ---- | ---------------- |
| U3₁  | Hadamard | π/2 | 0 | π    | first “?” on q₂  |
| U3₂  | T-dagger | 0   | 0 | −π/4 | second “?” on q₂ |

[
U3_1 = U3(\tfrac{π}{2}, 0, π), \quad U3_2 = U3(0, 0, -\tfrac{π}{4})
]

---

## Verification Summary

To confirm:

1. Build both the given circuit (with the U3s inserted) and the standard Toffoli (CCX).
2. Compare their unitaries up to a global phase.
3. Run all eight basis inputs -- both produce identical outputs.

---

## Truth Table

| Input (q0 q1 q2) | Output (Toffoli) |
| ---------------- | ---------------- |
| 000              | 000              |
| 001              | 001              |
| 010              | 010              |
| 011              | 011              |
| 100              | 100              |
| 101              | 101              |
| 110              | 111              |
| 111              | 110              |

---

## Discussion

* **H (U3₁)** changes the target’s basis from Z to X, transforming a CCZ into a CCX.
* **T† (U3₂)** removes residual phases from previous entangling operations.
* The final `T(q2)` and `H(q2)` return the target to the computational basis.

Together these reproduce the **Toffoli** gate behavior exactly (up to global phase).

---

## Repository Layout

```
task1_gate_tomography/
├── main.py          # Qiskit code implementing and verifying the circuit
├── README.md        # this explanatory document
└── requirements.txt # dependencies: Qiskit, NumPy
```

---

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

---

## Conclusion

By identifying:

* **U3₁(π/2, 0, π)** = Hadamard
* **U3₂(0, 0, −π/4)** = T-dagger

the circuit becomes fully equivalent to the Toffoli (CCX).
Both **matrix** and **truth-table** verification confirm this equivalence.

[
\boxed{
U3_1 = U3(\tfrac{π}{2}, 0, π), \quad U3_2 = U3(0, 0, -\tfrac{π}{4})
}
]

---
