import DES

cip = DES.new(b'abcdefgh', DES.MODE_ECB)
enc = cip.encrypt(b'Helloooo')
mes = cip.decrypt(enc)

print(enc, mes)