

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

USER_DONT_EXIST = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail="El usuario no existe",
                            headers={"WWW-Authenticate": "Bearer"},)
USER_INACTIVE = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo",
                             headers={"WWW-Authenticate": "Bearer"},)

WRONG_USER = HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                            detail="El usuario es incorrecto",
                            headers={"WWW-Authenticate": "Bearer"},)

WRONG_PASSW= HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                            detail="La contraseña es incorrecta.",
                            headers={"WWW-Authenticate": "Bearer"},)

INVALID_CREDENTIALS = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Credenciales inválidas",
                                    headers={"WWW-Authenticate": "Bearer"},)


def raise_exept(status_code: int, detail: str):
    return HTTPException(status_code = status_code,
                                    detail=detail,
                                    headers={"WWW-Authenticate": "Bearer"},)