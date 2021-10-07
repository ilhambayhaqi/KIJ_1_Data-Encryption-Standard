from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 8

MODE_ECB = 0
MODE_CBC = 1
MODE_CFB = 2

PC_1 = [57, 49, 41, 33, 25, 17,  9,
		 1, 58, 50, 42, 34, 26, 18,
		10,  2, 59, 51, 43, 35, 27,
		19, 11,  3, 60, 52, 44, 36,
		63, 55, 47, 39, 31, 23, 15,
		 7, 62, 54, 46, 38, 30, 22,
		14,  6, 61, 53, 45, 37, 29,
		21, 13,  5, 28, 20, 12,  4]

PC_2 = [14, 17, 11, 24,  1,  5,  3, 28,
		15,  6, 21, 10, 23, 19, 12,  4,
		26,  8, 16,  7, 27, 20, 13,  2,
		41, 52, 31, 37, 47, 55, 30, 40,
		51, 45, 33, 48, 44, 49, 39, 56,
		34, 53, 46, 42, 50, 36, 29, 32]

SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

IP = [58, 50, 42, 34, 26, 18, 10, 2,
	  60, 52, 44, 36, 28, 20, 12, 4,
	  62, 54, 46, 38, 30, 22, 14, 6,
	  64, 56, 48, 40, 32, 24, 16, 8,
	  57, 49, 41, 33, 25, 17,  9, 1,
	  59, 51, 43, 35, 27, 19, 11, 3,
	  61, 53, 45, 37, 29, 21, 13, 5,
	  63, 55, 47, 39, 31, 23, 15, 7]

EXP = [32,  1,  2,  3,  4,  5,
	    4,  5,  6,  7,  8,  9,
	    8,  9, 10, 11, 12, 13,
	   12, 13, 14, 15, 16, 17,
	   16, 17, 18, 19, 20, 21,
	   20, 21, 22, 23, 24, 25,
	   24, 25, 26, 27, 28, 29,
	   28, 29, 30, 31, 32,  1]

SUBS = [
		[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
		 [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

		[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
		 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
		 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

		[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
		 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

		[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
		 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],  

		[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
		 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]], 

		[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
		 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
		 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]], 

		[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
		 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
		 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
		   
		[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
		 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
		 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
		 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
	   ]

P = [16,  7, 20, 21, 29, 12, 28, 17,
	  1, 15, 23, 26,  5, 18, 31, 10,
	  2,  8, 24, 14, 32, 27,  3,  9,
	 19, 13, 30,  6, 22, 11,  4, 25]

IIP = [40,  8, 48, 16, 56, 24, 64, 32,
	   39,  7, 47, 15, 55, 23, 63, 31,
	   38,  6, 46, 14, 54, 22, 62, 30,
	   37,  5, 45, 13, 53, 21, 61, 29,
	   36,  4, 44, 12, 52, 20, 60, 28,
	   35,  3, 43, 11, 51, 19, 59, 27,
	   34,  2, 42, 10, 50, 18, 58, 26,
	   33,  1, 41,  9, 49, 17, 57, 25]

def new(key: bytes, mode: int, iv: bytes = None):
	assert len(key) == BLOCK_SIZE, 'KEY must be 8 bytes long'
	if type(key) == str:
		key = key.encode('utf-8')

	if mode == MODE_ECB:
		return ECB_MODE(key)
	elif mode == MODE_CBC:	
		assert len(iv) == BLOCK_SIZE, 'IV must be 8 bytes long'
		iv = iv.encode('utf-8') if type(iv) == str else iv
		return CBC_MODE(key, iv)

def to_bit(byt):
	bitstring = bin(bytes_to_long(byt))[2:].rjust(len(byt) * 8, '0')
	return [int(i) for i in bitstring]

def to_bytes(bit_a):
	bitstring = ''.join([str(i) for i in bit_a])
	return long_to_bytes(int(bitstring, 2))

def perm(bit_a, perm_table):
	return [bit_a[i - 1] for i in perm_table]

def SHIFT_left(bit_a, SHIFT):
	return bit_a[SHIFT:] + bit_a[:SHIFT]

def generateSubKeys(key):
	k_plus = perm(key, PC_1)
	c, d = [k_plus[:len(k_plus) // 2]], [k_plus[len(k_plus) // 2:]]
	
	for i in range(16):
		c.append(SHIFT_left(c[i], SHIFT[i]))
		d.append(SHIFT_left(d[i], SHIFT[i]))

	k = [perm(i + j, PC_2) for i, j in zip(c,d)]
	return k[1:]

def subs(bit_a, idx):
	row = (bit_a[0] << 1) + bit_a[-1]
	col = to_bytes(bit_a[1:-1])[0]
	return [int(i) for i in bin(SUBS[idx][row][col])[2:].rjust(4, '0')]

def feistel_round(bit_a, subKey):
	bit_exp = perm(bit_a, EXP) # Expansion
	bit_xor = [bit_exp[i] ^ subKey[i] for i in range(len(subKey))]

	bit_sub = []
	for i in range(8):
		chunk = bit_xor[i * 6: (i + 1) * 6]
		bit_sub += subs(chunk, i)

	return perm(bit_sub, P)

def feistel(bit_a, subKeys, encrypt):
	Li, Ri = bit_a[:len(bit_a) // 2], bit_a[len(bit_a) // 2 : ]

	for i in range(16):
		idx = i if encrypt == True else (15 - i)
		temp = Ri
		F = feistel_round(Ri, subKeys[idx])
		Ri = [F[j] ^ Li[j] for j in range(len(Li))]
		Li = temp

	return perm(Ri + Li, IIP)

class ECB_MODE():
	def __init__(self, key):
		self.key = to_bit(key)
		self.subKeys = generateSubKeys(self.key)

	def encrypt(self, plain: bytes, padding=False):
		if(type(plain) == str):
			plain = plain.encode('utf-8')
		if padding == True:
			plain = pad(plain, 8)
		else:
			assert len(plain) % 8 == 0, 'Plaintext length must be multiple of 8 bytes or use padding=True'

		enc = b''
		for i in range(0,len(plain) // 8):
			chunk = plain[i * BLOCK_SIZE : (i + 1) * BLOCK_SIZE]
			bit_chunk = perm(to_bit(chunk), IP)
			enc_chunk = feistel(bit_chunk, self.subKeys, True)
			enc += to_bytes(enc_chunk)
		return enc

	def decrypt(self, enc: bytes, padding=False):
		assert len(enc) % 8 == 0, 'Ciphertext is invalid'
		plain = b''
		for i in range(0,len(enc) // 8):
			chunk = enc[i * BLOCK_SIZE : (i + 1) * BLOCK_SIZE]
			bit_chunk = perm(to_bit(chunk), IP)
			plain_chunk = feistel(bit_chunk, self.subKeys, False)
			plain += to_bytes(plain_chunk)

		return unpad(plain,8) if padding else plain

class CBC_MODE():
	def __init__(self, key, iv):
		self.key = to_bit(key)
		self.iv = to_bit(iv)
		self.subKeys = generateSubKeys(self.key)

	def encrypt(self, plain: bytes, padding=False):
		if(type(plain) == str):
			plain = plain.encode('utf-8')
		if padding == True:
			plain = pad(plain, 8)
		else:
			assert len(plain) % 8 == 0, 'Plaintext length must be multiple of 8 bytes or use padding=True'

		enc = b''
		for i in range(0,len(plain) // 8):
			chunk = to_bit(plain[i * BLOCK_SIZE : (i + 1) * BLOCK_SIZE])
			if i == 0:
				chunk = [chunk[j] ^ self.iv[j] for j in range(len(chunk))]
			else:
				chunk = [chunk[j] ^ enc_chunk[j] for j in range(len(chunk))]

			bit_chunk = perm(chunk, IP)
			enc_chunk = feistel(bit_chunk, self.subKeys, True)
			enc += to_bytes(enc_chunk)
		return enc

	def decrypt(self, enc: bytes, padding=False):
		assert len(enc) % 8 == 0, 'Ciphertext is invalid'
		plain = b''
		for i in range(0,len(enc) // 8):
			chunk = to_bit(enc[i * BLOCK_SIZE : (i + 1) * BLOCK_SIZE])
			bit_chunk = perm(chunk, IP)
			plain_chunk = feistel(bit_chunk, self.subKeys, False)

			if i == 0:
				plain_chunk = [plain_chunk[j] ^ self.iv[j] for j in range(len(plain_chunk))]
			else:
				plain_chunk = [plain_chunk[j] ^ temp[j] for j in range(len(plain_chunk))]

			temp = chunk
			plain += to_bytes(plain_chunk)

		return unpad(plain,8) if padding else plain
		