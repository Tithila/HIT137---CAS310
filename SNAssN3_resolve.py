# This program is to
# 1. highlight the errors in the original code
# 2. state the reason of the error using commented key (#)
# 3. resolve the error in other to make the code run successfully.

global_variable = 100

# Error found 1
#my_dict = {'key1': 'valueg", 'ke12: ' : 'value2', 'key3' : 'value3'}

# 'valueg" - This is a typographical error. It should be value1 with single quote ''
# 'ke12: ' - This is a typographical error. Also, wrong reference and '' not in right indent
# or position, and it should be before double colon (:) separating key from value
# In dictionary, key and value are important factors or elements.

# Correction 1
my_dict = {'key1': 'value1', 'key2' : 'value2', 'key3' : 'value3'}

def process_numbers():
    global global_variable
    local_variable = 5
    numbers = [1, 2, 3, 4, 5]

    while local_variable > 0:
        if local_variable % 2 == 0:
            numbers.remove(local_variable)
        local_variable -= 1

    return numbers


my_set = {1, 2, 3, 4, 5, 5, 4, 3, 2, 1}

# Error found 2
#result = process_numbers(numbers = my_set)
# (numbers = my_set): This is an unexpected argument. It is an incorrect
# form of calling function.
# This is as a result of reports discrepancies between declared parameters and actual arguments,
# as well as incorrect arguments, for example, duplicate named arguments, or
# and an incorrect argument order.
# The function is not supposed to take arguments but numbers = my_set was passed into it.

# Correction 2
result = process_numbers()

def modify_dict():
    local_variable = 10
    my_dict['key4'] = local_variable

# Error found 3
#modify_dict(5): Unexpected argument as a result of incorrect call of function.
# The function modify_dict() takes in 0 or no positional
# arguments but 1 was passed (i.e, 5 was passed into the function)

# Correction 3
modify_dict()


def update_global():
    global global_variable
    global_variable += 10


for i in range(5):
    print(i)

    # Error found 4
#    i += 1 : This may not be necessary in the for loop because i automatically iterates

# within the range given. Although, the code can run successfully without removing. But best
# practice for loop (range function) must be followed duly.

if my_set is not None and my_dict['key4'] == 10:
    print("Condition met!")

if 5 not in my_dict:
    print("5 not found in the dictionary!")

print(global_variable)
print(my_dict)
print(my_set)