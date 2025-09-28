"""
Quantum Cryptography Implementation using Qiskit
BB84 Quantum Key Distribution Protocol
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import random
import hashlib

class BB84Protocol:
    """
    Implementation of BB84 Quantum Key Distribution Protocol
    """
    
    def __init__(self, key_length=16, eve_present=False):
        """
        Initialize BB84 protocol
        
        Args:
            key_length: Desired length of the final key
            eve_present: Whether an eavesdropper (Eve) is present
        """
        self.key_length = key_length
        self.eve_present = eve_present
        self.backend = Aer.get_backend('qasm_simulator')
        
    def encode_message(self, bits, bases):
        """
        Alice encodes her bits using chosen bases
        
        Args:
            bits: List of bits to encode (0 or 1)
            bases: List of bases to use (0 for Z-basis, 1 for X-basis)
        
        Returns:
            List of encoded quantum circuits
        """
        message = []
        for i in range(len(bits)):
            qc = QuantumCircuit(1, 1)
            
            # Prepare qubit based on bit value
            if bits[i] == 1:
                qc.x(0)
            
            # Apply basis
            if bases[i] == 1:  # X-basis (diagonal)
                qc.h(0)
                
            message.append(qc)
        
        return message
    
    def measure_message(self, message, bases):
        """
        Bob measures the qubits using his chosen bases
        
        Args:
            message: List of quantum circuits
            bases: Bob's measurement bases
        
        Returns:
            List of measurement results
        """
        measurements = []
        
        for i in range(len(message)):
            qc = message[i].copy()
            
            # Apply Bob's measurement basis
            if bases[i] == 1:  # X-basis
                qc.h(0)
            
            # Measure
            qc.measure(0, 0)
            
            # Execute circuit
            job = self.backend.run(transpile(qc, self.backend), shots=1)
            result = job.result()
            counts = result.get_counts(qc)
            
            # Get the measurement result
            measured_bit = int(list(counts.keys())[0])
            measurements.append(measured_bit)
        
        return measurements
    
    def eavesdrop(self, message):
        """
        Eve intercepts and measures qubits (if present)
        
        Args:
            message: List of quantum circuits
        
        Returns:
            Modified message after Eve's measurement
        """
        eve_bases = [random.randint(0, 1) for _ in range(len(message))]
        eve_results = []
        intercepted_message = []
        
        for i in range(len(message)):
            qc = message[i].copy()
            
            # Eve measures in random basis
            if eve_bases[i] == 1:
                qc.h(0)
            
            qc.measure(0, 0)
            
            # Execute circuit
            job = self.backend.run(transpile(qc, self.backend), shots=1)
            result = job.result()
            counts = result.get_counts(qc)
            measured_bit = int(list(counts.keys())[0])
            eve_results.append(measured_bit)
            
            # Eve prepares new qubit based on her measurement
            new_qc = QuantumCircuit(1, 1)
            if measured_bit == 1:
                new_qc.x(0)
            if eve_bases[i] == 1:
                new_qc.h(0)
            
            intercepted_message.append(new_qc)
        
        return intercepted_message, eve_results, eve_bases
    
    def sift_keys(self, alice_bases, bob_bases, alice_bits, bob_bits):
        """
        Sift keys by comparing bases and keeping only matching ones
        
        Args:
            alice_bases: Alice's bases
            bob_bases: Bob's bases
            alice_bits: Alice's bits
            bob_bits: Bob's measured bits
        
        Returns:
            Sifted keys for Alice and Bob
        """
        alice_key = []
        bob_key = []
        
        for i in range(len(alice_bases)):
            if alice_bases[i] == bob_bases[i]:
                alice_key.append(alice_bits[i])
                bob_key.append(bob_bits[i])
        
        return alice_key, bob_key
    
    def estimate_error_rate(self, alice_key, bob_key, sample_size=None):
        """
        Estimate error rate by comparing a sample of the keys
        
        Args:
            alice_key: Alice's sifted key
            bob_key: Bob's sifted key
            sample_size: Number of bits to compare
        
        Returns:
            Error rate and remaining keys
        """
        if sample_size is None:
            sample_size = min(len(alice_key) // 4, 10)
        
        if len(alice_key) < sample_size:
            return 1.0, [], []
        
        # Sample bits for error estimation
        sample_indices = random.sample(range(len(alice_key)), sample_size)
        sample_indices.sort(reverse=True)
        
        errors = 0
        for idx in sample_indices:
            if alice_key[idx] != bob_key[idx]:
                errors += 1
            alice_key.pop(idx)
            bob_key.pop(idx)
        
        error_rate = errors / sample_size if sample_size > 0 else 0
        
        return error_rate, alice_key, bob_key
    
    def run_protocol(self):
        """
        Run the complete BB84 protocol
        
        Returns:
            Dictionary containing protocol results
        """
        # Generate more bits than needed (due to sifting)
        n_bits = self.key_length * 4
        
        # Step 1: Alice generates random bits and bases
        alice_bits = [random.randint(0, 1) for _ in range(n_bits)]
        alice_bases = [random.randint(0, 1) for _ in range(n_bits)]
        
        # Step 2: Alice encodes and sends qubits
        message = self.encode_message(alice_bits, alice_bases)
        
        # Step 3: Eve intercepts (if present)
        if self.eve_present:
            message, eve_results, eve_bases = self.eavesdrop(message)
            print(f"Eve intercepted {len(message)} qubits")
        
        # Step 4: Bob chooses random bases and measures
        bob_bases = [random.randint(0, 1) for _ in range(n_bits)]
        bob_results = self.measure_message(message, bob_bases)
        
        # Step 5: Sift keys (keep only matching bases)
        alice_key, bob_key = self.sift_keys(alice_bases, bob_bases, alice_bits, bob_results)
        
        print(f"After sifting: {len(alice_key)} bits remain")
        
        # Step 6: Error estimation
        error_rate, alice_key, bob_key = self.estimate_error_rate(alice_key, bob_key)
        
        print(f"Estimated error rate: {error_rate:.2%}")
        
        # Step 7: Decide if key is secure
        if error_rate > 0.11:  # Threshold for detecting eavesdropping
            print("WARNING: High error rate detected! Possible eavesdropping.")
            secure = False
        else:
            print("Key exchange appears secure.")
            secure = True
        
        # Trim to desired key length
        final_alice_key = alice_key[:self.key_length]
        final_bob_key = bob_key[:self.key_length]
        
        return {
            'alice_key': final_alice_key,
            'bob_key': final_bob_key,
            'key_length': len(final_alice_key),
            'error_rate': error_rate,
            'secure': secure,
            'keys_match': final_alice_key == final_bob_key
        }

class QuantumEncryption:
    """
    Simple encryption using quantum-generated keys
    """
    
    @staticmethod
    def xor_encrypt(message, key):
        """
        XOR encryption using the quantum key
        
        Args:
            message: String message to encrypt
            key: Binary key from QKD
        
        Returns:
            Encrypted message
        """
        # Convert message to binary
        message_binary = ''.join(format(ord(c), '08b') for c in message)
        
        # Repeat key if necessary
        key_string = ''.join(str(bit) for bit in key)
        while len(key_string) < len(message_binary):
            key_string += key_string
        
        # XOR encryption
        encrypted = ''
        for i in range(len(message_binary)):
            encrypted += str(int(message_binary[i]) ^ int(key_string[i]))
        
        return encrypted
    
    @staticmethod
    def xor_decrypt(encrypted, key):
        """
        XOR decryption using the quantum key
        
        Args:
            encrypted: Encrypted binary string
            key: Binary key from QKD
        
        Returns:
            Decrypted message
        """
        # Repeat key if necessary
        key_string = ''.join(str(bit) for bit in key)
        while len(key_string) < len(encrypted):
            key_string += key_string
        
        # XOR decryption
        decrypted_binary = ''
        for i in range(len(encrypted)):
            decrypted_binary += str(int(encrypted[i]) ^ int(key_string[i]))
        
        # Convert binary to text
        decrypted = ''
        for i in range(0, len(decrypted_binary), 8):
            byte = decrypted_binary[i:i+8]
            decrypted += chr(int(byte, 2))
        
        return decrypted

# Example usage
def main():
    print("=" * 50)
    print("QUANTUM CRYPTOGRAPHY DEMONSTRATION")
    print("BB84 Quantum Key Distribution Protocol")
    print("=" * 50)
    
    # Test without eavesdropper
    print("\n1. SECURE CHANNEL (No Eavesdropper)")
    print("-" * 40)
    
    bb84 = BB84Protocol(key_length=32, eve_present=False)
    results = bb84.run_protocol()
    
    print(f"Alice's key: {results['alice_key'][:16]}...")
    print(f"Bob's key:   {results['bob_key'][:16]}...")
    print(f"Keys match: {results['keys_match']}")
    
    # Test with eavesdropper
    print("\n2. COMPROMISED CHANNEL (With Eavesdropper)")
    print("-" * 40)
    
    bb84_eve = BB84Protocol(key_length=32, eve_present=True)
    results_eve = bb84_eve.run_protocol()
    
    print(f"Alice's key: {results_eve['alice_key'][:16]}...")
    print(f"Bob's key:   {results_eve['bob_key'][:16]}...")
    print(f"Keys match: {results_eve['keys_match']}")
    
    # Demonstrate encryption with quantum key
    if results['secure'] and results['keys_match']:
        print("\n3. QUANTUM-SECURED MESSAGE ENCRYPTION")
        print("-" * 40)
        
        message = "QUANTUM SECURE"
        quantum_key = results['alice_key']
        
        # Encrypt
        encrypted = QuantumEncryption.xor_encrypt(message, quantum_key)
        print(f"Original message: {message}")
        print(f"Encrypted (binary): {encrypted[:32]}...")
        
        # Decrypt
        decrypted = QuantumEncryption.xor_decrypt(encrypted, quantum_key)
        print(f"Decrypted message: {decrypted}")
    
    print("\n" + "=" * 50)
    print("Quantum cryptography demonstration complete!")

if __name__ == "__main__":
    main()
