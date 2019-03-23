import base64, random, struct, os
from PIL import Image
from Crypto.Cipher import AES
from pbkdf2 import PBKDF2

# GLOBAL DECLARATION (for now, keep it that way)
myfile = "aqua.png"
passphrase = "useless"
salt = "nosaltpls"

def process_image(image="aqua.png",passphrase="useless",salt="nosaltpls"):
    encoded_passphrase = (str((base64.b64encode(bytes(passphrase, 'utf-8')))).split("'"))[1]
    im = Image.open(image,'r')
    pix_val = list(im.getdata())

    #debug
    print("Image name : "+image)
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

    new_pass  = ""
    for val in encoded_passphrase:
    	print(new_list[ord(val)])
    	new_pass += str(new_list[ord(val)])

    return new_pass

#print(new_pass)

file_to_encrypt = "encryptme"

def encrypt(file_to_encrypt,image="aqua.png",passphrase="useless",salt="nosaltpls"):
    new_pass = process_image(image,passphrase,salt)
    iv = os.urandom(16)
    print("IV : ",iv," [Please keep this somewhere safe]")
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


# NOTICE : NEED TO USE IMAGE TO DECRYPT!! BELOW CODE IS NOT COMPLETE
# idea : extract some value in the image to forge the IV (convert int to hex?)
def decrypt(iv,key): # should be def decrypt(iv,key,image): or something like that
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
