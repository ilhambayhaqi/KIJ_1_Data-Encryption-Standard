import DES

plain = b'Never Gonna Give You Up'
key = b'rickroll'
iv = b'A' * 8

cipher = DES.new(key, DES.MODE_CBC, iv)
ciphertext = cipher.encrypt(plain, padding = True)
print(f'{ciphertext = }')

plaintext = cipher.decrypt(ciphertext, padding = True)
print(f'{plaintext = }')