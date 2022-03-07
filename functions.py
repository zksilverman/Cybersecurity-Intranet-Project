"""
Final Lab Assignment
Zoe Silverman
CS 166 / Fall 2021

This file includes any methods and functions used by the program app.py
At the end of the file, it runs two functions, one to create a database used
by the flask program to hold usernames, passwords, and authorization levels.
The other function adds four users to the the database.
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


# function to return a timestamp with data and time
def get_date():
    """ Generate timestamp for data inserts """
    d = datetime.now()
    return d.strftime("%m/%d/%Y, %H:%M:%S")


# function to log a user into the flask web application. The function accepts two arguments, of a username and of a
# password to check if the user is or is not in the system. Then it will either return true and the authentication level
# if the user is in the system. If not, it will return false and the reason behind the failed login
def user_login(username, password):
    given_username = username
    given_password = password
    index = 0

    # read in entries from database intranet table login_information
    user_information = query_db()

    # create list of usernames
    username_list = []
    for user in user_information:
        username_list.append(user[0])
    # create list of passwords
    passwords_list = []
    for user in user_information:
        passwords_list.append(user[1])
    # create list of authorization levels
    authorization_list = []
    for user in user_information:
        authorization_list.append(user[3])

    # check for username in list
    if given_username not in username_list:
        return False, "Username not in system"
    elif given_username in username_list:
        index = username_list.index(given_username)
    # check for matching password at same index
    if not authenticate_password(given_password, passwords_list[index]):
        return False, "Username and password do not match"
    # if username and password are correct, return the authorization level
    return True, authorization_list[index]


# function add a user into the flask web application. the function accepts two arguments, of a username and of a
# password inputted by the user. It will return false if the username is already in the system of if the password
# does not meet requirements. If the username and password are both accepted, it will return true.
def add_user(username, password):
    # check to see if username is duplicated
    user_information = query_db()
    username_list = []
    for user in user_information:
        username_list.append(user[0])
    while username in username_list:
        return False, "This username is already in use. Please select a different username"

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
    encrypted_password = hash_and_salt_password(password)
    data_to_insert = [(username, encrypted_password, date_creation, authorization_level)]

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


# function which queries all the information from the intranet.db table. It will append all the information to a list
# and then returns the list when complete
def query_db():
    # create a blank list to hold all the information from the login_information table
    users = []
    # connect to the database
    try:
        conn = sqlite3.connect('intranet.db')
        c = conn.cursor()
        # append each row of information from the table to the list
        for row in c.execute("SELECT * FROM login_information"):
            users.append(row)
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()
    # return list of all database rows
    return users


# function which adds three users to the database with varying authorization levels. This allows for the admin to login
# to a variety of different accounts to test out the web application
def initial_username_inputs():
    # get date for insert
    date_creation = str(get_date())
    # compile data from first user
    data_to_insert_1 = [('jadams', hash_and_salt_password("hHGSD(f2412f*"), date_creation, '1')]
    # insert record into database
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

    # compile data for second record
    data_to_insert_2 = [('gwashington', hash_and_salt_password("*saf$aHH23saf$RGG"), date_creation, '2')]
    # insert second record into the database
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

    # compile data for third record
    data_to_insert_3 = [('jmadison', hash_and_salt_password("af*24h)(asdFF"), date_creation, '3')]
    # insert third record into the database
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


# function to check if password includes a number. the function accepts a password and if it includes a number, it
# returns true. If it does not include a number, it returns false
def check_number(password):
    for character in password:
        if character.isdigit():
            return True
    return False


# function to check if password includes a letter. The function accepts a password and if it includes a letter, it
# returns true. If it does not include a letter, it returns false
def check_letter(password):
    for character in password:
        if character.isalpha():
            return True
    return False


# function to check if password includes an uppercase letter. The function accepts a password and if it includes an
# uppercase letter, it returns true. If it does not include an uppercase letter, it returns false
def check_uppercase(password):
    uppercase_letters = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                         'Z', 'X', 'C', 'V', 'B', 'N', 'M']
    for character in password:
        if character in uppercase_letters:
            return True
    return False


# function to check if password includes a lowercase number. The function accepts a password and if it includes a
# lowercase number, it returns true. If it does not include a lowercase number, it returns false
def check_lowercase(password):
    lowercase_letters = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
                         'z', 'x', 'c', 'v', 'b', 'n', 'm']
    for character in password:
        if character in lowercase_letters:
            return True
    return False


# function to check if password includes a special character. The function accepts a password and if it includes a
# special character, it returns true. If it does not include a special character, it returns false
def check_special_character(password):
    special_character_string = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                                '-', '_', '+', '=', '<', '>', '?', ',']
    for character in password:
        if character in special_character_string:
            return True
    return False


# function that hashed and salts a password. The function accepts the password as an argument then adds a 40 character
# salt to the beginning of the password. Next the password is hashed through sha1. The salted and hashed password is
# returned by the function.
def hash_and_salt_password(password):
    # creation of a 40 character salt
    salt = os.urandom(40)
    password = password.encode('utf-8')
    # passes the password through sha1 algorithm
    hashed_password = hashlib.sha1(password).hexdigest()
    salted_hashed_password = str(salt) + str(hashed_password)
    #return salted and hashed password
    return salted_hashed_password


# function that authenticates password and determines if the inputted password from a user, matches the hashed and
# salted password in the database. The function either returns true or false depending of if the two passwords
# match.
def authenticate_password(input_password, hashed_password):
    # remove the salt
    password_hashed_length = len(hashed_password) - 40
    de_salted_password = hashed_password[password_hashed_length:]
    input_password_byte = input_password.encode('utf-8')
    # hash the inputted password through sha1 algorithm
    hashed_input_password = hashlib.sha1(input_password_byte).hexdigest()
    # compare the inputted password with the stored password
    if de_salted_password == hashed_input_password:
        # if the passwords match, then the login is authenticated
        return True
    else:
        # if the passwords do not match, it is an incorrect login attempt
        return False


# this function creates a randomly generated password for a user to select. It returns the generated password which
# matches all of the web applications criteria.
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
initial_username_inputs()  # Adds three initial usernames, passwords, and authorization levels to the database
