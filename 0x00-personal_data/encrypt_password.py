import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password as a byte string.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate a password against a hashed password.

    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The plain text password to validate.

    Returns:
        bool: True if the password matches the hashed
        password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
