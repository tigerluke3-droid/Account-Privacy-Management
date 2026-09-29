'''
This program simulates storing and managing user account information.
Login information is stored in a dictionary from a given file, with each
user's password encrypted and stored under their username. The program also
tracks the age of each password and determines whether it needs to be changed.

SOURCES;
Date and time;
https://www.w3schools.com/python/python_datetime.asp
https://docs.python.org/3/library/datetime.html
https://www.programiz.com/python-programming/datetime

Common Passwords;
https://securityjournalamericas.com/most-common-passwords/
'''
#Modules
import string
from datetime import datetime, timedelta

#Helper Functions
def normalize(text):
    '''
    This function removes the punctuation symbols and blank spaces in a string. It also sets the text to be lowercase.
    It returns the standardized result.

    Parameter:
        text: Whatever string we would want to be normalized
    Returns:
        result: returns the normalized string
    '''
    result = ""
    text = text.lower()
    for character in text:
        if character not in string.whitespace and character not in string.punctuation:
            result = result + character
    return result

def normalizeDate(text):
    '''
    This function normalizes the date for use by the datetime module.

    Parameter:
        text: The date
    Returns:
        result: The date in a formated way that is uniform for every account.
    '''        
    result = ""
    text = str(text)
    for character in text:
        if character not in string.ascii_uppercase or string.ascii_lowercase:
            result = result + character
        elif character in ",":
            result = result + "-"
        elif character in ":.":
            result = result + character
    return result

def generateAddress(firstName, lastName):
    '''
    This function generates the email address to be used for login. It uses  returns the completed email address.

    Parameters:
        firstName: User's inputed firstname
        lastName: User's inputed lastname
    Returns:
        an email address based off of the user's name (Ex: Jack Carver -> carver_j@denison.edu)
    '''
    
    firstName = normalize(firstName)
    lastName = normalize(lastName)

    return lastName + "_"  + firstName[0] + "@denison.edu"

def common_passwords(password): 
    """
    Checks to see if the user's password is on the list of the 100 most common passwords

    Parameters:
        Password: User inputed password.
    Returns:
        Orginal: returns a boolean granting if the password is orginal or not.
    """
    orginal = True
    passwordFile = open("Password_100.txt", "r")

    for word in passwordFile:
        word = word.strip() #Allows the code to read the .txt file line by line.

        if password == word:
            print("Your password is to common. (add some more numbers or special characters (@,$,etc.) to make it more unique) ")
            orginal = False

    if "password" in password:
        print("Please don't make your password include the word ""password"" (add some more numbers or special characters (@,$,etc.) to make it more unique) ")
        orginal = False

    passwordFile.close() #Common Passwords source add to write up

    return orginal

def valid_passowrd(password):
    """
    Checks to see if the user generated passowrd is valid in terms of following the criteria

    Parameters:
        password: The user generated password.
    Returns:
        Valid: returns a boolean granting if the password is valid or not.
    """
    #Inital values for my varaibles. _check variables helps to see if inputed password is valid. UserPassword varaible houses inputed password to be checked.
    upper_check = False
    lower_check = False
    digit_check = False
    valid = False #Determines if the over password is valid

    #Checks to see if password has 8 or more characters
    if not len(password) >= 8:
        print("Seems that your password is short. Make sure your password is 8 or more charcters long.")

    #Checks each character in the user generate password to see if it has at least one of the following: uppercase, lowercase, and a digit
    for char in password:
        if char == char.upper():
            upper_check = True
        if char == char.lower():
            lower_check = True
        if char.isdigit():
            digit_check = True

    #Generation of error message if requirments of password is not met. 
    if not upper_check == True:
        print("Seems that your password is missing an uppercase letter!")
    if not lower_check == True:
        print("Seems that your password is missing a lowercase letter!")
    if not digit_check == True:
        print("Seems that your password is missing a digit!")

    if upper_check == True and lower_check == True and digit_check == True:
        valid = True
    else: 
        valid = False

    return valid

#PART 1 ->
def accountsDictionary(fileName): 
     '''
     This function creates a dictionary to use throughout the program. It uses information from the given file.
    
    Parameter:
        fileName: .csv file that we want the function to open from and use it's contents.
     Returns:
        dictionary: A dictionary that has all of the dates and passwords off of every user from the .csv file.
     '''
     dictionary = {}

     infile = open(fileName, "r")
     for line in infile:
        halves = line.strip().split(',')
        if len(halves) == 2:
            shiftLetters, ShiftDigits = halves
            dictionary["shiftLetters"] = shiftLetters
            dictionary["shiftDigits"] = ShiftDigits
        if len(halves) == 3:
            name, password, date = halves
            name = removeElements(name)
            password = removeElements(password)
            date = removeElements(date)

            dictionary[name] = ((password, date))


     return dictionary

def appendDictionaryToFile(dictionary, fileName):
    '''
    This function writes the information in a dictionary to a given file. 

    Parameter:
        dictionary: Where all of the account information is saved.
        fileName: The file where dictionary's information will be saved at.
    '''
    updateFile = open(fileName, "w")
    n = 0

    for key in dictionary:

        if len(dictionary[key]) == 1:
            updateFile.write(f"{dictionary[key]},")
        else:
            if n == 0:
                updateFile.write(f"\n")
            messyValue = str(dictionary[key])
            cleanValue = messyValue.replace("(", "").replace(")", "").replace("'", "").replace(" ", "")
            
            updateFile.write(f"{key}, {cleanValue}\n")
            n = n+1

    updateFile.close()

def createAccount(accounts, shiftLetters, shiftDigits):
    '''
    Asks the user to input their First and Last name, which geneates a username, and input a valid password.

    Parameters:
        accounts: A dictionary where user's account information is located and saved via keys.
        shiftLetters: The amount of tmes a letter should be siffted during encryption/decryption.
        shiftDigits: The amount of times a digit should be siffted during encryption/decryption.
    Returns:
        username: the username generated from inputed information.
    '''
    #Creating a username (email) based off user's first and last name
    firstName = input ("Please enter your first name: ")
    lastName = input ("Please enter your last name: ")

    baseUsername = generateAddress(firstName, lastName) 

    parts = baseUsername.split("@")
    namePart = parts[0]
    domainPart = parts [1]

    username = baseUsername
    addNumber = 1

    while username in accounts:
        username = namePart + str(addNumber) + "@" + domainPart
        addNumber = addNumber + 1  
    
    #Two check points that will allow the rest of the createAccount fucntion to continue.
    result_1 = False
    result_2 = False

    #The following while loop will keep going until all of these conditions are met
    while not result_1 == True or not result_2 == True:
        userPassword = input ("\n" + "Please enter a password (should contain at least one lowercase letter, one uppercase letter, one digit, and is at least 8 characters long): ")
        userPassword = userPassword.strip() #ensures there are no spaces in the front or back of the inputed password
        result_1 = valid_passowrd(userPassword)
        if result_1 == True:
            result_2 = common_passwords(userPassword)

    #If all conditions are met the inputed passowrd will be housed in AccountInfo in a way that a .csv file can read.
    print("Password is valid!")
    encrypted = encrypt(userPassword, shiftLetters, shiftDigits)

    #Allows the user generated username and password to be added to the library of the .csv file login database.
    accounts[username] = encrypted
    
    return username 
    
# PART 2 ->
def encrypt(plain, shiftLetters, shiftDigits):
    '''
    Encrypts the user's orginal inputed password using an encryption method called Caeser Cipher.

    Parameters:
        plain: The orignal inputed password to be encrypted.
        shiftLetters: number of positions to shift letters.
        shiftDigits: Number of positions to shift digits.
    
    Returns:
        encrypt_pass: The encrypted version of the user's password to be utilized in other functions.
    '''
    #Allowing a blank string canvas for shifted characters to be saved in as the new encrypted password
    encrypt_pass = ""

    #Goes through each character and shifts each upper/lowercase letter alongside a number based on the shifLetters & shiftDigits parameter.
    for char in plain:
        if char.isupper(): 
            encrypt_pass = encrypt_pass + chr((ord(char) - ord('A') + shiftLetters) % 26 + ord('A')) #Want to insure when the uppercase letter shifts it doesn't venture out to lowercase, numbers or special characters.
        elif char.islower():
            encrypt_pass = encrypt_pass + chr((ord(char) - ord('a') + shiftLetters) % 26 + ord('a')) #Want to insure when the lowercase letter shifts it doesn't venture out to uppercase, numbers or special characters.
        elif char.isdigit(): 
            encrypt_pass= encrypt_pass + chr((ord(char) - ord('0') + shiftDigits) % 10 + ord('0')) #Want to insure when the digits shifts it doesn't venture out to lowercase, uppercase or special characters.
        else:
            encrypt_pass = encrypt_pass + chr(ord(char)) #Just adds whatever character the char index is on in that certain iteration

    return encrypt_pass

def decrypt(encoded, shiftLetters, shiftDigits):
    '''
    decrypts the encrypted passowrd back to the orginal user inputed password.

    Parameters:
        encoded: The encrypted password.
        shiftLetters: number of positions to shift letters.
        shiftDigits: Number of positions to shift digits.
    
    Returns:
        decrypt_pass: The decrypted version of the password (Goes back to how the user inputed password looked like).
    '''
    #Allowing a blank string canvas for shifted characters to be saved in as the decrypted password
    decrypt_pass = ""

    for char in encoded:
        if char.isupper(): 
            decrypt_pass = decrypt_pass + chr((ord(char) - ord('A') - shiftLetters) % 26 + ord('A')) 
        elif char.islower():
            decrypt_pass = decrypt_pass + chr((ord(char) - ord('a') - shiftLetters) % 26 + ord('a'))
        elif char.isdigit(): 
            decrypt_pass= decrypt_pass + chr((ord(char) - ord('0') - shiftDigits) % 10 + ord('0')) 
        else:
            decrypt_pass = decrypt_pass + chr(ord(char))

    return decrypt_pass

def passwordCreation():
    '''
    This function allows the user to input a password for their new email. It requires that they have
    one lowercase letter, one uppercase letter, one digit, and at least 8 characters in the password.
    This function returns the complete password.
    '''
    
    print("To finish creating your denison.edu email account, please enter a password.")
    print("You need to include: one lowercase letter, one uppercase letter, one digit, and " + 
        "please ensure that your password is at least 8 characters.")
    print(" Additionally, please do not input a password that is included in the top " +
        "100 password list.")

    passwordComplete = False

    password = ""
    while passwordComplete is False:

        lengthEqualOrPlus = False
        lowercaseLetter = False
        uppercaseLetter = False
        digitsLetter = False
        notTop100Password = False

        password = input("Please input a secure password. ")
        for character in password:
            if character in string.ascii_lowercase:
                    lowercaseLetter = True
            if character in string.ascii_uppercase:
                    uppercaseLetter = True
            if character in string.digits:
                    digitsLetter = True
            if len(password) >= 8:
                lengthEqualOrPlus = True
            if common_passwords(password):                                                 
                notTop100Password = True
            #if unvalid password = this is a function to check if it has "password" or "12345..."

        if lengthEqualOrPlus and lowercaseLetter and uppercaseLetter and digitsLetter is True:
            print("Valid password input. Thank you.")
            passwordComplete = True
        
        if lengthEqualOrPlus is False:                                                  #Messages for invalid inputs.
             print("Invalid input. Please input a password that is at least eight characters long.")
        if lowercaseLetter is False:
             print("Invalid input, please include at least one lowercase letter.")
        if uppercaseLetter is False:
             print("Invalid input, please include at least one uppercase letter.")
        if digitsLetter is False:
             print("Invalid input, please include at least number.")
        if notTop100Password is False:
              print("Invalid input, please do not use a commonly used password.")

    return password

def changePassword(username, accounts):     
    '''
    Prompts the user to change their username if it has been over 6 months since they created their account
    Uses a dictionary called accounts.

    This function will be called when the user attempts to log on with a password created 6 months ago.

    Store information in a tuple in the dictionary. (encrypted password, time created)
    '''
    if sixMonths(username, accounts) == True:              

        print("Password created more than six months ago, please enter a new password.")
        newPass = passwordCreation()
        encryptedPass = encrypt(newPass, 1, 7)            
        updatedDate = datetime.today()
        normalDate = normalizeDate(updatedDate)
        accounts[username] = (encryptedPass, normalDate)
    else:                                                   
        print("Login successful!")

def sixMonths(username, accounts):            
    '''
    This function checks if 6 months have passed since password creation. It returns true if it has been over 6 months since
    password creation.

    This function assumes 30 days in a month.

    '''
    current = datetime.today()
    normalCurrent = normalizeDate(current)
    yearsC, monthsC, daysC = integerDate(normalCurrent)
    
    passwordDate = accounts[username][1]
    normalPassDate = normalizeDate(passwordDate)

    yearsP, monthsP, daysP = integerDate(normalPassDate)

    passwordTime = datetime(yearsP, monthsP, daysP)
    currentTime = datetime(yearsC, monthsC, daysC)
    length = currentTime - passwordTime

    if length > timedelta(180):
        return True
    else:
        return False
          
def integerDate(date):
    '''
    This function turns a given date into integers representing years, months, and days respectively.

    IMPORTANT-> Dates must be normalized prior to adding.
    '''
    years = date[:4]
    months = date[5:7]
    days = date[8:10]

    return int(years), int(months), int(days)

def loginUpdated(accounts):
    '''
    Updated login function using the created dictionary.

    Parameter:
        accounts: The dictionary that holds user's account infromation to be found, via keys.
    '''
    username = input("Please enter your username. ")
    password = input("Please enter your password. ")

    try:

        decryptedPass = decrypt(accounts[username][0], 1, 7)       
        decryptedPass = removeElements(decryptedPass)

        if decryptedPass == password:
            print("Access Granted")
            changePassword(username, accounts)
        else:
            print("Access Denied!")

    except KeyError:
        print("Access Denied!")

def removeElements(text):
    '''
    This function removes text elements to allow for text to be processed.
    '''
    text = text.replace("\n", "")
    text = text.replace("\t", "")
    text = text.replace("\x1f", "")
    return text

#Main fununction
def main():
    """
    How the program is meant to function.
    """
    accounts = accountsDictionary("encrypted2.csv") 
    loginUpdated(accounts) #Note: for the timer to work properly, dates must be entered in YYYY/MM/DD format
    appendDictionaryToFile(accounts, "encrypted2.csv") 

    return

main()