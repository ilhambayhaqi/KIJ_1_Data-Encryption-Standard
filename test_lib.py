from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import DES

plain = b'Never Gonna Give You Up'
key = b'rickroll'
iv = b'A' * 8

cipher = DES.new(key, DES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(plain, 8))
print(f'{ciphertext = }')

cipher = DES.new(key, DES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext),8)
print(f'{plaintext = }')