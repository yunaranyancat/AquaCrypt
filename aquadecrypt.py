import base64, random, struct, os
from PIL import Image
from Crypto.Cipher import AES
from pbkdf2 import PBKDF2

myfile = "aqua.png"
passphrase = "useless"
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
	print(newlist)

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

iv = b'r^O\xbf\xe1j\xac\xdf9^\x1c\xed\xab]\xdf\xc2'
key = PBKDF2(passphrase,new_pass).read(16)


with open("encrypted.txt", 'rb') as infile:
		origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
		iv = infile.read(16)
		decipher = AES.new(key, AES.MODE_CBC, iv)

		with open("decrypted.txt", 'wb') as outfile:
			while True:
				chunk = infile.read(24*1024)
				if len(chunk) == 0:
					break
				outfile.write(decipher.decrypt(chunk))

			outfile.truncate(origsize)
