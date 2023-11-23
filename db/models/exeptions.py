

from fastapi import HTTPException, status


USER_NOT_FOUND = HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                            detail="No se encontro el usuario",
                            headers={"WWW-Authenticate": "Bearer"},)

USER_EXIST = HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                            detail="El usuario ya existe",
                            headers={"WWW-Authenticate": "Bearer"},)

USER_DONT_CREATE = HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                            detail="No se pudo crear el usuario",
                            headers={"WWW-Authenticate": "Bearer"},)