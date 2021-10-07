# KIJ_Data-Encryption-Standard

## Tugas 1 - Data Encryption Standard

- Nama : Muhammad Ilham Bayhaqi
- NRP : 05111840000069

## Penggunaan

Untuk contoh penggunaannya sebagai berikut.

```python
import DES

cipher = DES.new(b'privkey-', DES.MODE_ECB)
plaintext = 'some messages'.encode('utf-8')
encrypted_text = DES.encrypt(plaintext, padding=True)

print(encrypted_text)
```

Output yang dihasilkan sebagai berikut.

```
b'T\xb3}\xe6tI\x11U\xa9\x10\xb4\xb4\n)\x82\xc8'
```

## Mode Operasi Penyandian

Terdapat 2 mode operasi penyandian block sebagai berikut.

- Electronic Code Block (ECB) 

```
DES.new(key, DES.MODE_ECB)
```

- Cipher Block Chaining (CBC)

```
DES.new(key, DES.MODE_CBC, iv)
```

Keterangan :

- **key** merupakan secret key yang digunakan dalam DES cipher. Key harus memiliki panjang 8 bytes. Bit paritas akan diabaikan.
- **iv** merupakan initial vector yang digunakan dalam enkripsi dan dekripsi. Initial vector harus memiliki panjang 8 bytes.