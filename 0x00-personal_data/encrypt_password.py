#!/usr/bin/env python3
"""
    hashing ans checking password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
        generate password hash
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
        chech if password match
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
