import os
import pyAesCrypt


def encrypt(file_path: str, password: str) -> str:
    buffer_size = 128 * 1024
    encrypt_file = f"{file_path}.aes"
    pyAesCrypt.encryptFile(infile=file_path, outfile=encrypt_file, passw=password, bufferSize=buffer_size)
    os.remove(file_path)
    return encrypt_file
