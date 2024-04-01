#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import random

seed = random.randint(0, 10 ** 6) 
def get_random_number():
    global seed 
    seed = int(str(seed * seed).zfill(12)[3:9])
    return seed


def encrypt(message):
    key = b''
    for i in range(8):
        key += (get_random_number() % (2 ** 16)).to_bytes(2, 'big')
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(message, AES.block_size))
    return ciphertext.hex()

print("Thanks for using our encryption service! To get the encrypted flag, type 1. To encrypt a message, type 2.")
while True:
    print("What would you like to do (1 - get encrypted flag, 2 - encrypt a message)?")
    user_input = 2
    if(user_input == 1):
        break
    print("What is your message?")
    message = input()
    print(encrypt(message.encode()))


flag = open('/src/flag.txt', 'r').read()
print("Here is the encrypted flag:", encrypt(flag.encode()))






'''

les essaie de chiffrement renvoie ces résultat 

a0268ab81f3007ae4ab1e094f28f08a9
b94a678a4066431f3d1c5adfb6a50415
172e029430547117b36342d94610f3ea
8c27e02f48f4e3152e3ec199b1718287
c8c787aad4da7b690f928095acef81ae
6f7ca3110e316a2f89df7a75ba985be3
2e2447554a0348d6c8accd49fccb1da4
667589582ab2559f8266ed59645b69af
50f7cde02271bc682379f694e1b8b9ad
a774595254d98c6908df31b2250295b3
a17e148501251dd71c7df6db2c3eb46c
bbedf5813dbbb48ed36a9dcca880fea2
f6415c39fdd832e8ffbb8aa550af6f9b
7a2895803471859d14d67bb71bbc371c
b1b9b8d0ac06f5fd6e9236a4f220152b
89b2943ffbd359e79abface85252c906
4aa3ecc8d763317991d9f5b4c5f902d6
c6e949769961409275df4774aae0b362
467f7cb2c6f7657e4cf279ddaf7e152f
ef06c3bb5702c2e1a395bf242808df93
e157a6f81d3b64c2d863bf32f5a0b631
e173a52ca76d13dce582ae2d588273c2
1602ec58fac77e5be47a8a7c7fc00157
9606b34cf5bdb3ac55aaaf94c4cb960a
bdc10f0b1f9c295160a5cad695afc47c
ae943ae41c3958d68f776ce51b1936dc
46ec998e8303f35c9dd4723cf42981f9
756e77caf209952c1fb31533fac30b03
a348fd6f1b417f89b854250ed65ef41e
4061473510103e10e98d2ead61f20232
576f079106bf774f1c67c075d9c5fb2b
ee074fa17e54a3d3dfc4b7da6fd0c4de
409a37ec47b9d23e346034531db074d8
1840bfd8c0a7d7aa8b8727a44f9a1af8
7c2003c348f656d5d6463c2912024f42
'''