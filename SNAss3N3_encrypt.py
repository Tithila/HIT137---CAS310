# This program reads the decrypted programme

# First stage: read the decrypted code written in a .txt file

with open ('tedep.txt','r') as file:
    decrpt_txt = file.read()
#    print (decrpt_txt)
    print("decrypted Code is \n ", decrpt_txt)

# Second stage: passing the decrypted text file into encrypted code to decrypt the real code

def encrypt (text, key):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + key
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord ('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

key = 13
#encrypted_code = encrypt(original_code, key)
encrypted_code = encrypt(decrpt_txt, key)
#print (encrypted_code)
print ("Encrypted Code is \n ", encrypted_code)

