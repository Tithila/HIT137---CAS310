#----------------------------------chapter 1, question 2 begins here-------------------------------#
#---------------------------------------------start here ------------------------------------------#
#                                       Generated Number Script

import time

current_time = int(time.time())

generated_number = (current_time % 100) + 50

if generated_number % 2 == 0:
    generated_number += 10

print(generated_number) 

#-------------------------------------ends here ----------------------------------------------------#

#--------------------------------------------starts here --------------------------------------------#
#              This program generates rgb indexes, add generated number, and get new image

from PIL import Image
import numpy as np

# Load an image
p_img = Image.open('chapter1.jpg')

#p_img.show() 

img_rgb  = p_img.convert('RGB')
rgb_img_array = np.array(img_rgb)
print (rgb_img_array)

#img_arry = np.arry(img)
#print (rgb_img_array)

r,g,b = rgb_img_array[0,0]
print(f" image indexes are Red: {r}, Green {g}, Blue {b}")   # generated_number

n_rgb_img_array = rgb_img_array + [generated_number]
print (n_rgb_img_array)

n_rgb_img_array = np.clip(n_rgb_img_array, 0, 245)

chapter1out = Image.fromarray(n_rgb_img_array.astype('uint8'))

chapter1out.save('chapter1out.jpg')
chapter1out.show()

#----------------------------------------end here-----------------------------------------------#

#--------------------------------------------starts here-----------------------------------------#
#   Generating all red pixel values in new image and sum it up!

from PIL import Image

new_image = Image.open('chapter1out.jpg')

new_image = new_image.convert('RGB')

new_image_array = np.array(new_image)

red_index = new_image_array[:,:,0]
sum_red_index = np.sum(red_index)

print(f"Sum of all red index value in chapter1out.png: {sum_red_index}")

#----------------------------------------------ends here -----------------------------------------#
#----------------------------------chapter 1, question 2 ends here-------------------------------#


#-----------------------------------chapter2, question 2 begins here -----------------------------#
#--------------------------------------starts here -------------------------------------------------#
#     String conversion (both even numbers and uppercase alphabets/letters) into ASCII code

def chamber_of_string(c_strings):
    numbers = ''
    letters = ''

    numbers = ''.join([char for char in c_strings if char.isdigit()])
    letters = ''.join([char for char in c_strings if char.isalpha()])

    # Converting even numbers in the number substring to ASCII code decimal values
    Con_EvenNum = [ord(num) if int(num) % 2 == 0 else num for num in numbers]

    # Converting uppercase letters in the letter substring to ASCII code decimal values
    Con_letters = [ord(letter) if letter.isupper() else letter for letter in letters]

    return Con_EvenNum, Con_letters


c_strings = "uxVIC2358642GHjuyivxz8642QYUZdzksdfjhlifj23339i5thkfewjf3AWSSuyh345"
print("This is the object string:", c_strings)

Enum, Uletters = chamber_of_string(c_strings)

print("These are the converted even nums:", Enum)
print("These are the converted uppercase alphabets:", Uletters)

#---------------------------------------ends here---------------------------------------------------#
#-------------------------------------chapter2, question 2 ends here -------------------------------#