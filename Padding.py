def pad(byt_a, block_size):
	ln = len(byt_a)
	pad_size = 8 - ln % 8
	return byt_a + (pad_size.to_bytes(1, 'big') * pad_size)

def unpad(byt_a, block_size):
	ln = len(byt_a)
	assert ln % block_size == 0, 'Incorrect block size'
	pad_size = int(byt_a[-1])
	assert byt_a[-pad_size:] == pad_size.to_bytes(1, 'big') * pad_size, 'Incorrect padding'
	return byt_a[:-pad_size]