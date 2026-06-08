from pwdlib.hashers.argon2 import Argon2Hasher

ARGO2_HASHER = Argon2Hasher(salt_len=64, hash_len=64)


class ARGO2PasswordHasher:
    """Class to hash password by using argon2 algorithm.

    More about argo2:
        https://en.wikipedia.org/wiki/Argon2

    """

    def hash(self, password: str) -> str:
        """Hash password by using argo2."""
        return ARGO2_HASHER.hash(password=password)

    def verify(self, hashed: str, password) -> bool:
        """Check password is compatible with some hash."""

        return ARGO2_HASHER.verify(password=password, hash=hashed)
