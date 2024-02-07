#!/usr/bin/env python3
"""
this docs contains functions to
defines the hash_password function to return a hashed password
"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """this function to define the password
    args:
        password: the password to be hashed
    return:
        the result is returning a hashed password
    """
    by = password.encode()

    haspw = hashpw(by, bcrypt.gensalt())
    return haspw


def is_valid(hashed_password: bytes, password: str) -> bool:
    """this function is to check whether a password is valid
    args:
        hashed_password: the hashed password
        password: the password in string
    return:
        return the result wether the password is correct or not
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
