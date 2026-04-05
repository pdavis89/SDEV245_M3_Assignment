Crypto Utility Web App
This project is a Flask‑based web application that provides a simple interface for experimenting with core cryptographic concepts. It includes tools for hashing, basic substitution ciphers, and digital signatures. The app is designed to run locally or be deployed on Render using Gunicorn.

Features
1. SHA‑256 Hashing
The app supports hashing both:
- Input strings
- Uploaded files
Files are processed in streaming chunks to support large uploads without consuming excessive memory.

2. Caesar Cipher (Encrypt/Decrypt)
A classic substitution cipher used for learning and demonstration.
The app allows you to:
- Encrypt text with a chosen shift value
- Decrypt text using the same shift
- Preserve case and non‑alphabetic characters
This is not intended for real security, but it’s useful for understanding how substitution ciphers work.

3. Digital Signatures (OpenSSL)
The app integrates with OpenSSL to simulate real digital signature workflows.
You can:
- Upload a file and a private key to generate a signature
- Upload a file, signature, and public key to verify authenticity
This demonstrates how asymmetric cryptography ensures integrity and non‑repudiation.