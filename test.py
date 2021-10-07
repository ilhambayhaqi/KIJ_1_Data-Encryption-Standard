# from Crypto.Cipher import DES
# from Crypto.Util.Padding import pad, unpad
import DES

cip = DES.new(b'abcdefgh', DES.MODE_CBC, b'A' * 8)
enc = cip.encrypt(b'HellooooAAAA', padding=True)
print(enc)

# cip = DES.new(b'abcdefgh', DES.MODE_CBC, b'A' * 8)
mes = cip.decrypt(enc)
mes = cip.decrypt(enc, padding = True)
print(mes)