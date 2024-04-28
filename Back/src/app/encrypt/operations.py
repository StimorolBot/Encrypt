import os
import pyAesCrypt
from typing import TYPE_CHECKING
from fastapi import HTTPException, status

from core.operations.crud import Crud
from core.logger import encrypt_logger
from src.app.encrypt.models.model import FileTable

if TYPE_CHECKING:
    from pydantic import EmailStr
    from sqlalchemy.ext.asyncio import AsyncSession

from core.setting import setting


async def encrypt(dir_: "EmailStr", file_name: str, password: str, session: "AsyncSession", base_path: str = setting.base_path) -> list:
    buffer_size = 128 * 1024
    input_file = f"{base_path}/{dir_}/{file_name}"

    try:
        match file_name.split("."):
            case file, ext, extension if extension in "aes":
                # Расшифровать файл
                file = f"{file}.{ext}"
                output_path = f"{base_path}/{dir_}/{file}"

                try:
                    pyAesCrypt.decryptFile(infile=input_file, outfile=output_path, bufferSize=buffer_size, passw=password)
                except ValueError:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный пароль")

            case file, extension:
                # Зашифровать файл
                file = f"{file}.{extension}.aes"
                output_path = f"{base_path}/{dir_}/{file}"
                pyAesCrypt.encryptFile(infile=input_file, outfile=output_path, bufferSize=buffer_size, passw=password)

            case _:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неподдерживаемый формат файла")

        await Crud.create(session=session, table=FileTable, data_dict={"email": dir_, "name": file})
        os.remove(input_file)
        return [output_path, file]

    except ValueError:
        encrypt_logger.error(msg=f"Не удалось найти указанный путь: {input_file}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")
