def encrypt_caesar(plaintext: str):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """

    ciphertext: str = ''
    for i in plaintext:
        if ('a' <= i <= 'z') or ('A' <= i <= 'Z'):
            code: int = ord(i) + 3
            if (ord('Z') < code < ord('a')) or (ord('z') < code):
                code -= 26
            ciphertext += chr(code)
        else:
            ciphertext += i

    return ciphertext


def decrypt_caesar(ciphertext: str):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """

    plaintext: str = ''
    for i in ciphertext:
        if ('a' <= i <= 'z') or ('A' <= i <= 'Z'):
            code: int = ord(i) - 3
            if (ord('Z') < code < ord('a')) or (ord('A') > code):
                code += 26
            plaintext += chr(code)
        else:
            plaintext += i

    return plaintext
