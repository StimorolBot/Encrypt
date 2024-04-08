import os
import pyAesCrypt
from fastapi import HTTPException, status

from core.config import config


async def encrypt(dir_: str, file_name: str, password: str) -> list:
    file = ""
    output_path = ""
    buffer_size = 128 * 1024
    input_file = f"{config.BASE_PATH}/{dir_}/{file_name}"

    match file_name.split("."):
        case file, ext, extension if extension in "aes":
            # Расшифровать файл
            file = f"{file}.{ext}"
            output_path = f"{config.BASE_PATH}/{dir_}/{file}"

            try:
                pyAesCrypt.decryptFile(infile=input_file, outfile=output_path, bufferSize=buffer_size, passw=password)
            except ValueError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный пароль")

        case file, extension:
            # Зашифровать файл
            file = f"{file}.{extension}.aes"
            output_path = f"{config.BASE_PATH}/{dir_}/{file}"
            pyAesCrypt.encryptFile(infile=input_file, outfile=output_path, bufferSize=buffer_size, passw=password)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неподдерживаемый формат файла")

    os.remove(input_file)
    return [output_path, file]
