import base64, random, struct, os
from PIL import Image
from Crypto.Cipher import AES
from pbkdf2 import PBKDF2

myfile = "aqua.png"
passphrase = "useless"
file_to_encrypt = "encryptme"
salt = "nosaltpls"
encoded_passphrase = (str((base64.b64encode(bytes(passphrase, 'utf-8')))).split("'"))[1]
im = Image.open(myfile,'r')
pix_val = list(im.getdata())

print("Image name : "+myfile)
print("passphrase : "+passphrase)
print("encoded passphrase : "+ encoded_passphrase)

list_img = []
for i in pix_val:
	newlist = []
	tup_to_list = list(i)
	newlist = tup_to_list[:-1]
	list_img += newlist
	print(tup_to_list)

print(len(list_img))

new_list = []
for elem in list_img:
	new_list.append((elem+9)//10*10)

print(new_list)

new_pass  = ""

print(type(encoded_passphrase))

for val in encoded_passphrase:
	print(new_list[ord(val)])
	new_pass += str(new_list[ord(val)])

print(new_pass)

iv = os.urandom(16)
print("IV : ",iv)
key = PBKDF2(passphrase,new_pass).read(16)
print("key :",key)
cipher = AES.new(key, AES.MODE_CBC, iv)
filesize = os.path.getsize(file_to_encrypt)
print("filesize :",filesize)

with open(file_to_encrypt, 'rb') as infile:
	with open("encrypted.txt", 'wb') as outfile:
		outfile.write(struct.pack('<Q', filesize))
		outfile.write(iv)

		while True:
			chunk = infile.read(64*1024)
			if len(chunk) == 0:
				break
			elif len(chunk) % 16 != 0:
				chunk += b' ' * (16 - len(chunk) % 16)

				outfile.write(cipher.encrypt(chunk))
