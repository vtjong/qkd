from qiskit import QuantumCircuit, Aer, execute
import numpy as np

backend = Aer.get_backend('qasm_simulator')

def E91_QKD(key_len, eavesdrop):
    alice_bases = []
    bob_bases = []
    alice_received = []
    bob_received = []
    for _ in range(round(9 * key_len / 2)):
        # Generate a Bell state
        cct = QuantumCircuit(2,3)
        cct.h(0)
        cct.cx(0,1)

        # If Eavesdropper taps into one measurement (say B)
        if eavesdrop:
            cct.measure(1,2)
        
        # Choose Alice's measurement basis
        basis = np.random.choice([0, 1, 2])
        alice_bases.append(basis)
        # Measuring in different directions based on basis
        if basis == 1:
            cct.ry(-np.pi/4, 0)
        elif basis == 2:
            cct.ry(-np.pi/2, 0)
            
        # Choose Bob's measurement basis
        basis = np.random.choice([1, 2, 3])
        bob_bases.append(basis)
        # Measuring in different directions based on basis
        if basis == 1:
            cct.ry(-np.pi/4,1)
        elif basis == 2:
            cct.ry(-np.pi/2, 1)
        elif basis == 3:
            cct.ry(-3*np.pi/4, 1)
            
        # Measure at intermediate interface
        cct.measure([0,1],[0,1])
        
        #run on Aer simulator   
        result = execute(cct, backend, shots=1).result()
        bits = result.get_counts(cct) # Returned dictionary
        bits = next(iter(bits)) # Get the key
        
        alice_received.append(int(bits[-1]))
        bob_received.append(int(bits[-2]))
    return np.asarray(alice_bases), np.asarray(bob_bases), np.asarray(alice_received), np.asarray(bob_received)

def correlation(obs1, obs2, bases1, bases2, i, j):
    match1 = np.nonzero(bases1 == i)
    match2 = np.nonzero(bases2 == j)
    matches = np.intersect1d(match1, match2)
    e1 = np.sum(np.logical_not(np.logical_xor(obs1[matches],  obs2[matches])))
    e2 = np.sum(np.logical_xor(obs1[matches],  obs2[matches]))
    return (e1 - e2) / (e1 + e2) if matches.shape[0] > 0 else 0

def verify(obs1, obs2, bases1, bases2):
    S = correlation(obs1, obs2, bases1, bases2, 0, 1)
    S -= correlation(obs1, obs2, bases1, bases2, 0, 3)
    S += correlation(obs1, obs2, bases1, bases2, 2, 1)
    S += correlation(obs1, obs2, bases1, bases2, 2, 3)
    return S > 2

def generate_key(key_len, eavesdrop=False):
    alice_bases, bob_bases, alice_received, bob_received = E91_QKD(key_len, eavesdrop)
    matching = (alice_bases == bob_bases)
    alice_key = alice_received[matching]
    bob_key = bob_received[matching]
    assert (alice_key == bob_key).all() # Checks that both Alice and Bob receive the same output
    secure = verify(alice_received, bob_received, alice_bases, bob_bases)
    return ''.join(map(str,alice_key)), secure