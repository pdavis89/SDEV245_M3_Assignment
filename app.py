from flask import Flask, request, render_template
import hashlib
import subprocess
import os

app = Flask(__name__)

# SHA-256 HASHING

def hash_string(text: str) -> str:
    sha = hashlib.sha256()
    sha.update(text.encode("utf-8"))
    return sha.hexdigest()

def hash_file(path: str) -> str:
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest()

# CAESAR CIPHER

def caesar(text: str, shift: int, mode: str) -> str:
    if mode == "decrypt":
        shift = -shift
    shift %= 26

    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            offset = (ord(ch) - base + shift) % 26
            result.append(chr(base + offset))
        else:
            result.append(ch)
    return "".join(result)

# DIGITAL SIGNATURE (OpenSSL)

def sign_file(private_key: str, file_path: str, signature_out: str):
    subprocess.run([
        "openssl", "dgst", "-sha256",
        "-sign", private_key,
        "-out", signature_out,
        file_path
    ], check=True)
    return signature_out

def verify_signature(public_key: str, file_path: str, signature_path: str) -> bool:
    result = subprocess.run([
        "openssl", "dgst", "-sha256",
        "-verify", public_key,
        "-signature", signature_path,
        file_path
    ], capture_output=True, text=True)
    return "Verified OK" in result.stdout

# ROUTES

@app.route("/", methods=["GET", "POST"])
def index():
    output = None

    if request.method == "POST":
        action = request.form.get("action")

        # Hash string
        if action == "hash_string":
            text = request.form.get("input_text", "")
            output = hash_string(text)

        # Hash file
        elif action == "hash_file":
            file = request.files.get("input_file")
            if file:
                path = "uploaded.bin"
                file.save(path)
                output = hash_file(path)

        # Caesar cipher
        elif action == "caesar":
            text = request.form.get("input_text", "")
            shift = int(request.form.get("shift", 3))
            mode = request.form.get("mode", "encrypt")
            output = caesar(text, shift, mode)

        # Sign file
        elif action == "sign":
            file = request.files.get("input_file")
            key = request.files.get("private_key")
            if file and key:
                file.save("msg.bin")
                key.save("priv.pem")
                sign_file("priv.pem", "msg.bin", "sig.bin")
                output = "Signature created (sig.bin)"

        # Verify signature
        elif action == "verify":
            file = request.files.get("input_file")
            sig = request.files.get("signature")
            pub = request.files.get("public_key")
            if file and sig and pub:
                file.save("msg.bin")
                sig.save("sig.bin")
                pub.save("pub.pem")
                ok = verify_signature("pub.pem", "msg.bin", "sig.bin")
                output = "Signature VALID" if ok else "Signature INVALID"

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)