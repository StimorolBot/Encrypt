import os
import pyAesCrypt


def encrypt(file_path: str, password: str) -> str:
    buffer_size = 128 * 1024
    extension = file_path.split(".")[-1]

    match extension:
        case "aes":
            path = file_path.split(".aes")[0]
            pyAesCrypt.decryptFile(infile=file_path, outfile=path, passw=password, bufferSize=buffer_size)
        case _:
            path = f"{file_path}.aes"
            pyAesCrypt.encryptFile(infile=file_path, outfile=path, passw=password, bufferSize=buffer_size)
    os.remove(file_path)
    return path
