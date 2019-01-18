def encrypt_vigenere(plaintext: str, keyword: str):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """

    ciphertext = ''
    for num, i in enumerate(plaintext):
        if ('a' <= i <= 'z') or ('A' <= i <= 'Z'):
            shift = ord(keyword[num % len(keyword)])
            if 'a' <= i <= 'z':
                shift -= ord('a')
                code = shift + ord(i)
                if code > ord('z'):
                    code -= 26
            else:
                shift -= ord('A')
                code = shift + ord(i)
                if code > ord('Z'):
                    code -= 26
            ciphertext += chr(code)
        else:
            ciphertext += i

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """

    plaintext = ''
    for num, i in enumerate(ciphertext):
        if ('a' <= i <= 'z') or ('A' <= i <= 'Z'):
            shift = ord(keyword[num % len(keyword)])
            if 'a' <= i <= 'z':
                shift -= ord('a')
                code = ord(i) - shift
                if code < ord('a'):
                    code += 26
            else:
                shift -= ord('A')
                code = ord(i) - shift
                if code < ord('A'):
                    code += 26
            plaintext += chr(code)
        else:
            plaintext += i

    return plaintext