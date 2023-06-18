# Main imports
import os
from datetime import datetime
from cryptography.fernet import Fernet

# Function to get user input, the input is file extension to use for further actions
def getFileExtensionInput(ext_arr):
  # First change the array to set to get rid of duplicates
  ext_set = set(ext_arr)
  # Then turn the set back to array
  ext_list = list(ext_set)

  # Turn the array into a string for print (readability)
  ext_list = ' | '.join(ext_list)

  print('Available file extensions in this directory:')
  print(ext_list)

  # Lets user input the extension to use
  # User can leave the input empty to use all extensions
  print('Choose an extension or leave empty to select all extensions..')
  ext_inpt = input()

  print('You chose "' + ext_inpt + '"!')

  # Returns the chosen extension as string
  return ext_inpt

# Function to select all files that have the chosen extension from above function
def selectFilesFromExtensions(ext, file_array):
  # Declare the clean array to store the files with chosen extension
  clean_array = []

  # For loop to check the file array for files containing correct extension
  # Appends the files to clean array
  for file in file_array:
    if file.endswith(ext):
      clean_array.append(file)

  # Returns the clean array
  return clean_array

# Function to let user choose either to use a single file or extensions
def useSingleFileOrExtensions():
  print('Do you want to use a single file or multiple files with extension?')
  print('--------------------------------')
  print('1. - Use one single file')
  print('2. - Use multiple files from extension')
  print('--------------------------------')

  action_inpt = input('Choose which action you want to use: ')

  # Changes the input to integer
  inpt_int = int(action_inpt)

  # If input is valid, returns the input
  if 1 <= inpt_int <= 2:
    return inpt_int
  else:
    print('Please provide an existing action!')
    exit()

# Function to get a single file from array
def getSingleFile(file_array):
  print('--------------------------------')
  print('Please input full file name (file name and extension)')
  file_inpt = input()

  # Loops the array and if the file name input matches a file returns the file
  for file in file_array:
    if file == file_inpt:
      return file
    
  print('Incorrect file name / file doesnt exist')
  exit()

# Function to read the metadata of a file
def readFileMetadata(file):
    stats = os.stat(file)

    # Changes the modify time from seconds to a readable format
    modified_mtime = datetime.fromtimestamp(stats.st_mtime).strftime('%d-%m-%Y %H:%M')

    # Gets the file size in bytes and converts it to string
    file_size = str(stats.st_size)

    # Prints out the file information
    print('File name: ' + file + ' | date modified: ' + modified_mtime + ' | file size: ' + file_size + ' bytes')

# Function that prepares the metadata reading
def readFileOrFilesMetada(file_array, extension_array):
  # Calls the file choice function and saves the input
  fileUsage = useSingleFileOrExtensions()

  # match/case from the input
  # Either uses single file or all files with provided extension
  match fileUsage:
    case 1:
      readFileMetadata(getSingleFile(file_array))
    case 2:
      extension = getFileExtensionInput(extension_array)
      clean_array = selectFilesFromExtensions(extension, file_array)
      # For loop that goes through the array and gets file stats using os library
      for file in clean_array:
        readFileMetadata(file)

# Function for key rewrite confirmation
# I put this in a function to clean the code a bit
def rewriteKey():
  print('Do you want to rewrite the key? Y/N')
  inpt = input()

  if inpt == 'Y' or inpt == 'y':
    return True
  elif inpt == 'N' or inpt == 'n':
    return False
  else:
    print('Please use Y or N')
    exit()

# Function to generate encryption/dencryption key
def generateEncryptionKey():
  # Uses cryptography libraries method Fernet
  key = Fernet.generate_key()

  # Lets user provide the directory where to save the key file
  print('!IMPORTANT! Where to save the key? (Provide a full path!)')
  print('If you want to save the key in the same directory, leave input empty (NOT RECOMMENDED)')
  dir_path_inpt = input()

  # Lets user provide the key file
  print('Provide the key file name without extension!')
  key_file_inpt = input()
  key_file_name = key_file_inpt + '.key'

  # Joins the directory path and file name together
  full_key_path = os.path.join(dir_path_inpt, key_file_name)

  # Checks if the key already exists
  # If the key file doesnt exist, it proceeds with saving the key
  if os.path.isfile(full_key_path) == False:
    with open(full_key_path, 'wb') as filekey:
      filekey.write(key)
  # If the key file exists, it lets user decide to rewrite the key or not
  else:
    print('Key already exists!')
    if rewriteKey() == True:
      with open(full_key_path, 'wb') as filekey:
        filekey.write(key)

# Funcion to let user provide the location of the existing key file
# I also used this to clean up the code a bit
def keyFileLocation():
  # Lets user provide the directory where the key is located
  print('Provide the full path of the directory where the key is saved..')
  dir_path_inpt = input()

  # Lets user provide the key name
  print('Provide the key file name without extension!')
  key_file_inpt = input()
  key_file_name = key_file_inpt + '.key'

  # Joins the directory path and file name together
  full_key_path = os.path.join(dir_path_inpt, key_file_name)

  # Then returns the full key path
  return full_key_path

# Function that encrypts the provided file
def encryptFile(file, fernet):
  with open(file, 'rb') as fails:
    original = fails.read()

  encrypted = fernet.encrypt(original)

  with open(file, 'wb') as encrypted_file:
    encrypted_file.write(encrypted)

# Function to encrypt the files
def encryptFiles(file_array, extension_array):
  with open(keyFileLocation(), 'rb') as filekey:
    key = filekey.read()

  fernet = Fernet(key)

  fileUsage = useSingleFileOrExtensions()

  match fileUsage:
    case 1:
      encryptFile(getSingleFile(file_array), fernet)
    case 2:
      extension = getFileExtensionInput(extension_array)
      clean_array = selectFilesFromExtensions(extension, file_array)

      for file in clean_array:
        encryptFile(file, fernet)

def decryptFile(file, fernet):
  with open(file, 'rb') as enc_file:
    encrypted = enc_file.read()
  
  decrypted = fernet.decrypt(encrypted)

  with open(file, 'wb') as dec_file:
    dec_file.write(decrypted)

def decryptFiles(file_array, extension_array):
  with open(keyFileLocation(), 'rb') as filekey:
    key = filekey.read()

  fernet = Fernet(key)

  fileUsage = useSingleFileOrExtensions()

  match fileUsage:
    case 1:
      decryptFile(getSingleFile(file_array), fernet)
    case 2:
      extension = getFileExtensionInput(extension_array)
      clean_array = selectFilesFromExtensions(extension, file_array)

      for file in clean_array:
        decryptFile(file, fernet)

def chooseMainAction():
  print('Available options/actions:')
  print('--------------------------------')
  print('1. - Read file metadata')
  print('2. - Generate Fernet key')
  print('3. - Encrypt files')
  print('4. - Decrypt files')
  print('--------------------------------')

  action_inpt = input('Choose which action you want to use: ')

  inpt_int = int(action_inpt)

  if 1 <= inpt_int <= 4:
    return inpt_int
  else:
    print('Please provide an existing action!')
    exit()

def mainFileFunction():
  file_array = []
  extension_array = []

  for file in os.listdir(os.getcwd()):
    temp, ext = os.path.splitext(file)
    extension_array.append(ext)
    if file != 'miniFileToolkit.py':
      file_array.append(file)

  actionNum = chooseMainAction()

  match actionNum:
    case 1:
      readFileOrFilesMetada(file_array, extension_array)
    case 2:
      generateEncryptionKey()
    case 3:
      encryptFiles(file_array, extension_array)
    case 4:
      decryptFiles(file_array, extension_array)
    case _:
      print("Error with match/case..")
      exit()

mainFileFunction()