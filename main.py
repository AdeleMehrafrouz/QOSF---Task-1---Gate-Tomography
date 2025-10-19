# main.py
# QOSF Screening Task 1 — Gate Tomography
# Goal: Find U3 parameters for the two black boxes so the given circuit equals a Toffoli (CCX).
#
# Results used below:
#   First "?" on q2  = H              = U3(π/2, 0, π)
#   Second "?" on q2 = T-dagger (T†)  = U3(0,   0, −π/4)

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector
import numpy as np

def global_phase_equivalent(U, V, atol=1e-10):
    """
    Check if unitaries U and V are equal up to a global phase.
    """
    # inner product to estimate relative phase
    alpha = np.vdot(U.flatten(), V.flatten())
    if np.isclose(alpha, 0.0, atol=atol):
        # inner product zero: matrices are orthogonal — definitely not equal up to phase
        return False
    phase = alpha / abs(alpha)
    return np.allclose(U, phase * V, atol=atol)

def truth_table(circ):
    """
    Apply 'circ' to each 3-qubit computational basis |abc>, return the
    most likely output bitstring for each input (deterministic for Clifford+T).
    """
    results = {}
    for a in "01":
        for b in "01":
            for c in "01":
                label = a + b + c  # q0 q1 q2 in order
                psi_in = Statevector.from_label(label)
                psi_out = psi_in.evolve(circ)
                # find the basis state with max probability
                probs = np.abs(psi_out.data)**2
                # Qiskit basis ordering for 3 qubits is |q2 q1 q0> in the bitstring of Statevector
                # I'll convert max index back to a string in q0 q1 q2 order for readability.
                max_idx = int(np.argmax(probs))
                # statevector basis indexing: bitstring is (q2 q1 q0)
                bits_q2q1q0 = format(max_idx, "03b")
                # reorder to q0 q1 q2 for clarity
                bits_q0q1q2 = bits_q2q1q0[::-1]
                results[label] = bits_q0q1q2
    return results


def pretty_print_truth_table(tt):
    print("Input(q0q1q2) -> Output(q0q1q2)")
    for k in sorted(tt.keys()):
        print(f"    {k} -> {tt[k]}")


# -----------------------------
# 1) Build circuit with U3s in the two '?' positions
# -----------------------------
def build_circuit_with_u3():
    qc = QuantumCircuit(3, name="Task1Circuit")
    # Qubit roles: q0, q1 are controls; q2 is target.

    # First "?" on q2 is a Hadamard = U3(π/2, 0, π)
    qc.u(np.pi/2, 0.0, np.pi, 2)
    qc.t(0)                  # T(q0)
    qc.cx(0, 1)              # CX(q0 -> q1)
    qc.tdg(1)                # T†(q1)
    qc.cx(0, 1)              # CX(q0 -> q1)
    qc.t(1)                  # T(q1)
    qc.cx(1, 2)              # CX(q1 -> q2)
    qc.tdg(2)                # T†(q2)
    qc.cx(0, 2)              # CX(q0 -> q2)
    qc.t(2)                  # T(q2)
    qc.cx(1, 2)              # CX(q1 -> q2)

    # Second "?" on q2 is T-dagger = U3(0, 0, −π/4)
    qc.u(0.0, 0.0, -np.pi/4, 2)

    qc.cx(0, 2)              # CX(q0 -> q2)
    qc.t(2)                  # T(q2)
    qc.h(2)                  # H(q2)

    return qc


# -----------------------------
# 2) Build a reference Toffoli (CCX)
# -----------------------------
def build_reference_toffoli():
    ref = QuantumCircuit(3, name="CCX_ref")
    ref.ccx(0, 1, 2)
    return ref


# -----------------------------
# 3) Verification
# -----------------------------
def main():
    taskcircuit = build_circuit_with_u3()
    ref = build_reference_toffoli()

    # Unitary comparison (up to global phase)
    U = Operator(taskcircuit).data
    V = Operator(ref).data
    eq = global_phase_equivalent(U, V)

    print("=== Unitary Equivalence Check ===")
    print("Equivalent to Toffoli up to global phase:", eq)

    # Truth table check
    print("\n=== Truth Table — Task1 Circuit ==")
    tt_task1 = truth_table(taskcircuit)
    pretty_print_truth_table(tt_task1)

    print("\n=== Truth Table — Reference CCX ===")
    tt_ref = truth_table(ref)
    pretty_print_truth_table(tt_ref)

    # Confirm truth tables match exactly
    tt_match = tt_task1 == tt_ref
    print("\nTruth tables identical:", tt_match)

    # Final pass/fail summary
    print("\n=== Summary ===")
    if eq and tt_match:
        print("PASS: With U3_1 = U3(π/2, 0, π) and U3_2 = U3(0, 0, −π/4), the circuit equals CCX.")
    else:
        print("FAIL: Circuits did not match; double-check gate order and parameters.")

if __name__ == "__main__":
    main()
