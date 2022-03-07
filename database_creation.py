"""


"""

# import necessary libraries
import sqlite3
from datetime import datetime
import os
import hashlib
import random


# function to create a database for usernames, passwords, and authorization levels
def create_db():
    """ Create table 'login_information' in 'intranet' database """
    try:
        conn = sqlite3.connect('intranet.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE login_information
                    (
                    username text,
                    password text,
                    date_creation text,
                    authorization_level
                    )''')
        conn.commit()
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def get_date():
    """ Generate timestamp for data inserts """
    d = datetime.now()
    return d.strftime("%m/%d/%Y, %H:%M:%S")


def add_user(username, password):
    # check to see if username is duplicated
    user_information = query_db()
    username_list = []
    for user in user_information:
        username_list.append(user[0])
    while username in username_list:
        return "This username is already in use. Please select a different username"

    # validation for password
    # longer than 8 character
    while len(password) < 8:
        return False, "Password needs to be more than 8 characters long"
    # shorter than 25 characters
    while len(password) > 25:
        return False, "Password needs to be less than 25 characters long"
    # includes a number
    while not check_number(password):
        return False, "Password needs to be include at least one number"
    # includes a character
    while not check_letter(password):
        return False, "Password needs to be include at least one letter"
    # includes an uppercase letter
    while not check_uppercase(password):
        return False, "Password needs to be include at least one uppercase letter"
    # includes a lowercase letter
    while not check_lowercase(password):
        return False, "Password needs to be include at least one lowercase letter"
    # includes a special character
    while not check_special_character(password):
        return False, "Password needs to be include at least one special character"

    date_creation = str(get_date())
    # give least privileged authorization level
    authorization_level = '3'
    # salt and hash password
    encrypted_password = hash_and_salt_password(new_password)
    data_to_insert = [(new_username, encrypted_password, date_creation, authorization_level)]

    try:
        conn = sqlite3.connect('intranet.db')
        c = conn.cursor()
        c.executemany("INSERT INTO login_information VALUES (?, ?, ?, ?)", data_to_insert)
        conn.commit()
    except sqlite3.IntegrityError:
        return False, "Error. Tried to add duplicate record!"
    else:
        return True, "Account successfully created"
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def query_db():
    """ Copies all records in the plants table """
    users = []
    try:
        conn = sqlite3.connect('intranet.db')
        c = conn.cursor()
        for row in c.execute("SELECT * FROM login_information"):
            users.append(row)
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()
    return users


def initial_username_inputs():
    """Starts out database with 3 users"""
    date_creation = str(get_date())

    data_to_insert_1 = [('jadams', hash_and_salt_password("hHGSD(f2412f*"), date_creation, '1')]

    try:
        conn = sqlite3.connect('intranet.db')
        c = conn.cursor()
        c.executemany("INSERT INTO login_information VALUES (?, ?, ?, ?)", data_to_insert_1)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error. Tried to add duplicate record!")
    else:
        print("Success")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

    data_to_insert_2 = [('gwashington', hash_and_salt_password("*saf$aHH23saf$RGG"), date_creation, '2')]
    try:
        conn = sqlite3.connect('intranet.db')
        c = conn.cursor()
        c.executemany("INSERT INTO login_information VALUES (?, ?, ?, ?)", data_to_insert_2)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error. Tried to add duplicate record!")
    else:
        print("Success")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

    data_to_insert_3 = [('jmadison', hash_and_salt_password("af*24h)(asdFF"), date_creation, '3')]
    try:
        conn = sqlite3.connect('intranet.db')
        c = conn.cursor()
        c.executemany("INSERT INTO login_information VALUES (?, ?, ?, ?)", data_to_insert_3)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error. Tried to add duplicate record!")
    else:
        print("Success")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


# function to check if password includes a number
# the function accepts a password
# if it includes a number, it returns true
# if it does not include a number, it returns false
def check_number(password):
    for character in password:
        if character.isdigit():
            return True
    return False


# function to check if password includes a letter
# the function accepts a password
# if it includes a letter, it returns true
# if it does not include a letter, it returns false
def check_letter(password):
    for character in password:
        if character.isalpha():
            return True
    return False


# function to check if password includes an uppercase letter
# the function accepts a password
# if it includes an uppercase letter, it returns true
# if it does not include an uppercase letter, it returns false
def check_uppercase(password):
    for character in password:
        if character.islower():
            return True
    return False


# function to check if password includes a lowercase number
# the function accepts a password
# if it includes a lowercase number, it returns true
# if it does not include a lowercase number, it returns false
def check_lowercase(password):
    for character in password:
        if character.isupper():
            return True
    return False


# function to check if password includes a special character
# the function accepts a password
# if it includes a special character, it returns true
# if it does not include a special character, it returns false
def check_special_character(password):
    special_character_string = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                                '-', '_', '+', '=', '<', '>', '?', ',']
    for character in password:
        if character in special_character_string:
            return True
    return False


def hash_and_salt_password(password):
    salt = os.urandom(40)
    password = password.encode('utf-8')
    hashed_password = hashlib.sha1(password).hexdigest()
    salted_hashed_password = str(salt) + str(hashed_password)
    return salted_hashed_password


def authenticate_password(input_password, hashed_password):
    password_hashed_length = len(hashed_password) - 40
    de_salted_password = hashed_password[password_hashed_length:]
    input_password_byte = input_password.encode('utf-8')
    hashed_input_password = hashlib.sha1(input_password_byte).hexdigest()
    if de_salted_password == hashed_input_password:
        return True
    else:
        return False


def password_generation():
    generated_password = ''
    capital_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                       'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    lowercase_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']
    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '<', '>', '?', ',']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for num in range(6):
        # add a capital letter
        capital_letter = random.choice(capital_letters)
        generated_password = generated_password + str(capital_letter)
        # add a lowercase letter
        lowercase_letter = random.choice(lowercase_letters)
        generated_password = generated_password + str(lowercase_letter)
        # add a number
        number = random.choice(numbers)
        generated_password = generated_password + str(number)
        # a special character
        special_character = random.choice(special_characters)
        generated_password = generated_password + str(special_character)
    return generated_password


create_db()  # Run create_db function first time to create the database
initial_username_inputs() # Adds three initial usernames, passwords, and authorization levels to the database
