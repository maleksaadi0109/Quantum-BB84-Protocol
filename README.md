Quantum-BB84-Protocol

🚀 A Python implementation of the BB84 Quantum Key Distribution Protocol using Qiskit.
This project demonstrates how quantum mechanics can be used to securely exchange cryptographic keys between two parties (Alice and Bob) and detect the presence of an eavesdropper (Eve).

📖 Introduction

Quantum Cryptography is the next-generation approach to secure communication.
The BB84 protocol, introduced in 1984 by Charles Bennett and Gilles Brassard, is one of the first and most famous protocols for Quantum Key Distribution (QKD).

This project includes:

Simulation of BB84 protocol using Qiskit.

Demonstration of secure key exchange between Alice and Bob.

Detection of eavesdropping attempts by Eve.

Example of message encryption and decryption using the generated quantum key.

🛠️ Requirements

Make sure you have Python installed (>=3.8).
Install dependencies with:

pip install qiskit qiskit-aer matplotlib numpy

▶️ Usage

Run the project with:

python bb84.py

📂 Project Structure
Quantum-BB84-Protocol/
│── bb84.py          # Main implementation and demo
│── README.md        # Project documentation

🧪 Example Output

When running the script, you’ll see:

==================================================
QUANTUM CRYPTOGRAPHY DEMONSTRATION
BB84 Quantum Key Distribution Protocol
==================================================

1. SECURE CHANNEL (No Eavesdropper)
----------------------------------------
After sifting: 64 bits remain
Estimated error rate: 0.00%
Key exchange appears secure.
Keys match: True

2. COMPROMISED CHANNEL (With Eavesdropper)
----------------------------------------
Eve intercepted 128 qubits
After sifting: 62 bits remain
Estimated error rate: 12.90%
WARNING: High error rate detected! Possible eavesdropping.

3. QUANTUM-SECURED MESSAGE ENCRYPTION
----------------------------------------
Original message: QUANTUM SECURE
Encrypted (binary): 1010101001110...
Decrypted message: QUANTUM SECURE

==================================================
Quantum cryptography demonstration complete!

🔒 Features

✅ Full BB84 protocol simulation

✅ Eavesdropper (Eve) detection

✅ XOR-based encryption & decryption using quantum key

✅ Qiskit Aer backend simulation

🌍 Description (Arabic)

هذا المشروع يحاكي بروتوكول BB84 لتوزيع المفاتيح الكمية باستخدام بايثون ومكتبة Qiskit.
الغرض منه توضيح كيف يتم تبادل مفتاح تشفير آمن بين Alice و Bob، مع إمكانية اكتشاف وجود متجسس (Eve)، ثم استعمال المفتاح الكمي الناتج لتشفير وفك تشفير الرسائل.

📜 License

This project is open-source and available under the MIT License.
