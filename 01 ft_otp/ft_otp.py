import hashlib
import argparse
import time
import string
from cryptography.fernet import Fernet

def generate_otp(key):
    """ Génère un mot de passe OTP basé sur la clé spécifiée """
    current_time = round(time.time() / 30) * 30
    current_time = int(current_time)
    key = str(key)
    key = key.encode()
    current_time = str(current_time)
    current_time = current_time.encode()
    message = key + current_time
    hash = hashlib.sha256(message)
    hex_digest = hash.hexdigest()
    otp = hex_digest[:6]
    otp = int(otp, 16)
    otp = otp % (10 ** 6)
    otp = str(otp)
    otp = otp.zfill(6)
    print(otp)

def save_key(key):
    """ Sauvegarde la clé dans un fichier chiffré """
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted_key = cipher.encrypt(key)
    with open("ft_otp.key", 'wb') as f:
        f.write(encrypted_key)
    print("Key saved to", "ft_otp.key")

def load_key(filename):
    """ Charge la clé à partir d'un fichier chiffré """
    with open(filename, 'rb') as f:
        encrypted_key = f.read()
    return encrypted_key

def main():
    parser = argparse.ArgumentParser(description="One-Time Password (OTP) Generator")
    parser.add_argument("-g", metavar="KEYFILE_UNCYPHERED", help="Path to the file where the key is stored.")
    parser.add_argument("-k", metavar="KEYFILE_CYPHERED", help="Generate and print a new OTP based on the key in the specified file")

    args = parser.parse_args()

    if args.g:
        keyfile = args.g
        try:
            with open(keyfile, 'r') as f:
                key = f.read()
                key = key.lower()
                key = key.replace("\n", "")
            if len(key) == 64:
                key = int(key, 16)
                print(key)
                save_key(key)
            else:
                print("Error: key must be 64 hexadecimal characters")
        except FileNotFoundError:
            print("Error: key file not found")

    elif args.k:
        keyfile = args.k
        try:
            key = load_key(keyfile)
            generate_otp(key)
        except FileNotFoundError:
            print("Error: key file not found")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()