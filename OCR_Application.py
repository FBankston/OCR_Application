# File Imports
from tkinter import *
from tkinter import filedialog
from cv2 import *
import pytesseract
import numpy as np
import os

# Follow these steps to get tesseract working in python
# 1. Install (64 bit) resp. tesseract using installer available at: https://github.com/UB-Mannheim/tesseract/wiki
# 2. Note the tesseract path from the installation. If installing for all users, the default path is below
# 3. pip install pytesseract
# 4. Set the tesseract path in the line below if it's different from your own personal path
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Global variable file name/folder name that is used in multiple places
# These variables are used to update the file explorer label but more importantly store the path to the file/folder
fileName = ""
folderName = ""

# Function for opening the file explorer window
def browseFiles():
    global fileName

    # Open the file explorer and save the file the user chooses under fileName
    fileName = filedialog.askopenfilename(initialdir="C:/", title="Select a File")

    # Change label contents after picking a filename
    label_file_explorer.configure(text="File Opened: " + fileName)


# Function for performing OCR and extracting text from a single image
def convertFile():
    global fileName
    # Using the fileName variable that was assigned in browseFiles function to read our image
    myImage = cv2.imread(fileName)

    # Begin Preprocessing the image
    # Make the image larger
    myImage = cv2.resize(myImage, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    # Convert to grayscale
    myImage = cv2.cvtColor(myImage, cv2.COLOR_BGR2GRAY)
    # Split RBG channels and save them in an array
    rgb_planes = cv2.split(myImage)
    result_planes = []
    # Split into multiple RGB planes to process separately
    for plane in rgb_planes:
        # Apply dilation
        dilated_image = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        # Apply a median blur
        background_image = cv2.medianBlur(dilated_image, 21)
        diff_img = 255 - cv2.absdiff(plane, background_image)
        # Append all of the results to the same plane
        result_planes.append(diff_img)
    # Merge the channels back together after operations in the for loop
    myImage = cv2.merge(result_planes)

    # Apply dilation and erosion in order to remove some of the noise in the image
    kernel = np.ones((1, 1), np.uint8)
    # Increases some of the white region in the image
    myImage = cv2.dilate(myImage, kernel, iterations=1)
    # Erodes away some of the boundaries of foreground object
    myImage = cv2.erode(myImage, kernel, iterations=1)

    # Apply threshold to grayscale image to convert to black and white using OTSU threshold
    myImage = cv2.threshold(myImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # End Preprocessing the image

    # Setting custom OCR settings
    # The r parameter is simply choosing with tesseract engine to use
    # The psm parameter means "page segmentation mode
    # This parameter will be left as six for assuming a single block of text but there are 14 different options
    custom_config = r'--oem 3 --psm 6'
    outputText = pytesseract.image_to_string(myImage, config=custom_config)

    # Create a text file with the same name as the image and WRITE its contents to the file
    # We use the [0:-4] in order to remove the .jpg or .png file extension from the outputted text file
    file = open(fileName[0:-4] + ".txt", "w+")
    file.write(outputText)
    file.close()
    # After closing the file we print to the user that the process is complete along with the text file's name
    # The text file's name will of course be the same name as the image and in the same place
    print(' \nText extraction completed and saved under ' + fileName + '.txt')


# Function for selecting a whole folder of images
# Click on a folder and then click "select folder" to select this folder
def browseFolder():
    global folderName
    # Open the file explorer and save the folder the user chooses under folderName
    folderName = filedialog.askdirectory(initialdir="C:/", title="Select a Folder")

    # Change label contents after picking a folder
    label_file_explorer.configure(text="Folder Opened: " + folderName)


# Function for performing OCR and extracting text from a whole folder of images automatically
# The extracted text will all be appended to the text file "batchConversion.txt" in the same folder
def convertFolder():
    # We need the folderName and fileName variables because we will be operating on multiple files within a folder
    global fileName
    global folderName
    # os.chdir is to change the final output to match the folderName
    os.chdir(folderName)
    # File counter to count the amount of files being operated on to output to the user
    fileCounter = 1

    # For every file in the folder, perform this process:
    for fileName in os.listdir(folderName):
        myImage = cv2.imread(fileName)

        # Begin Preprocessing the image
        # Make the image larger
        myImage = cv2.resize(myImage, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        # Convert to grayscale
        myImage = cv2.cvtColor(myImage, cv2.COLOR_BGR2GRAY)
        # Split RBG channels and save them in an array
        rgb_planes = cv2.split(myImage)
        result_planes = []
        # Split into multiple RGB planes to process separately
        for plane in rgb_planes:
            # Apply dilation
            dilated_image = cv2.dilate(plane, np.ones((7, 7), np.uint8))
            background_image = cv2.medianBlur(dilated_image, 21)
            # Apply median blur
            diff_img = 255 - cv2.absdiff(plane, background_image)
            # Append all of the results to the same plane
            result_planes.append(diff_img)
        # Merge the channels back together after operations in the for loop
        myImage = cv2.merge(result_planes)

        kernel = np.ones((1, 1), np.uint8)
        # Apply dilation to increase some of the white region in the image
        myImage = cv2.dilate(myImage, kernel, iterations=1)
        # Erode away some of the background of the foreground object
        myImage = cv2.erode(myImage, kernel, iterations=1)

        # Apply Otsu threshold for binarization to get the image in black and white
        myImage = cv2.threshold(myImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # End Preprocessing the image

        # Setting custom OCR settings
        # The r parameter is simply choosing with tesseract engine to use
        # The psm parameter means "page segmentation mode
        # This parameter will be left as six for assuming a single block of text but there are 14 different options
        custom_config = r'--oem 3 --psm 6'
        outputText = pytesseract.image_to_string(myImage, config=custom_config)

        # Create a text file with the same name as the image and APPEND its contents to the file
        file = open("batchConversion.txt", "a+")
        file.write(outputText)
        file.write('\n' + '\n' + '\n' + '\n' + '\n')
        file.close()

        # Print to the user each time we have appended an image's text to the file along with the counter
        print('File # ' + str(fileCounter) + ' appended to text')
        # Increase the counter by one for each file inputted
        fileCounter += 1

    # After exiting the for loop we can print that the text extraction is complete
    print('Text extraction completed and saved under "batchConversion.txt" file \n')


def convertFile_Digits():
    global fileName
    myImage = cv2.imread(fileName)

    # Begin Preprocessing the image
    # Make the image larger
    myImage = cv2.resize(myImage, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    # Convert to grayscale
    myImage = cv2.cvtColor(myImage, cv2.COLOR_BGR2GRAY)
    # Split RBG channels and save them in an array
    rgb_planes = cv2.split(myImage)
    result_planes = []
    # Split into multiple RGB planes to process separately
    for plane in rgb_planes:
        dilated_image = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        # Apply dilation
        background_image = cv2.medianBlur(dilated_image, 21)
        # Apply median blur
        diff_img = 255 - cv2.absdiff(plane, background_image)
        result_planes.append(diff_img)
    # Merge the channels back together after operations in the for loop
    myImage = cv2.merge(result_planes)

    # Apply dilation and erosion in order to remove some of the noise noise in the image
    kernel = np.ones((1, 1), np.uint8)
    # Increases some of the white region in the image
    myImage = cv2.dilate(myImage, kernel, iterations=1)
    # Erodes away some of the boundaries of foreground object
    myImage = cv2.erode(myImage, kernel, iterations=1)

    # Apply threshold to grayscale image to convert to black and white using OTSU threshold
    myImage = cv2.threshold(myImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # End Preprocessing the image

    # Set outputbase digits parameter in order to only extract digits from the text
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    outputText = pytesseract.image_to_string(myImage, config=custom_config)

    # Create a text file with the same name as the image and WRITE its contents to the file
    # We use the [0:-4] in order to remove the .jpg or .png file extension from the outputted text file
    file = open(fileName[0:-4] + ".txt", "w+")
    file.write(outputText)
    file.close()
    # After closing the file we print to the user that the process is complete along with the text file's name
    # The text file's name will of course be the same name as the image and in the same place
    print('Digit extraction completed and saved under ' + fileName + '.txt')


def convertFolder_Digits():
    global fileName
    global folderName
    # To keep track of the folder so we can save the batchConversion.txt file in that same folder
    os.chdir(folderName)
    # We will keep track of the file counter to output to the user after each successful processed file
    fileCounter = 1

    for fileName in os.listdir(folderName):
        myImage = cv2.imread(fileName)

        # Begin Preprocessing the image
        myImage = cv2.resize(myImage, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        myImage = cv2.cvtColor(myImage, cv2.COLOR_BGR2GRAY)
        rgb_planes = cv2.split(myImage)
        result_planes = []
        # Split into multiple RGB planes to process separately
        for plane in rgb_planes:
            # Apply dilation
            dilated_image = cv2.dilate(plane, np.ones((7, 7), np.uint8))
            # Apply median blur
            background_image = cv2.medianBlur(dilated_image, 21)
            diff_img = 255 - cv2.absdiff(plane, background_image)
            result_planes.append(diff_img)
            # Merge the channels back together after operations in the for loop
        myImage = cv2.merge(result_planes)

        # Apply dilation and erosion to remove some noise
        kernel = np.ones((1, 1), np.uint8)
        # Dilate to increase some of the white region in the image
        myImage = cv2.dilate(myImage, kernel, iterations=1)
        # Erode away some of this boundary from the foreground object
        myImage = cv2.erode(myImage, kernel, iterations=1)

        # Apply Otsu thresholding for a binarized image that's black and white
        myImage = cv2.threshold(myImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # End Preprocessing the image

        # Set outputbase digits parameter in order to only extract digits from the text
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        outputText = pytesseract.image_to_string(myImage, config=custom_config)

        # Create a text file with the same name as the image and APPEND its contents to the file
        file = open("batchConversion.txt", "a+")
        file.write(outputText)
        file.write('\n' + '\n' + '\n' + '\n' + '\n')
        file.close()

        # print the file counter after each successful OCR processing and appending
        print('File # ' + str(fileCounter) + ' appended to text')
        # Increment the file counter each time while in the loop
        fileCounter += 1

    # After exiting the for loop we can print that that the process is complete and image's text appended to a text file
    print('Digit extraction completed and saved under "batchConversion.txt" file \n')


# Create the Tkinter root window GUI
window = Tk()

# Setting the title of the window here
window.title('OCR Application')

# Setting the size of the window
window.geometry("700x400")

# Setting the background color of the window
window.config(background="green")

# Begin button creation here
# This is the label that displays the filepath
label_file_explorer = Label(window,
                            text=" Start by clicking 'Browse File' for a single file "
                                 "or 'Browse Directory' for a whole folder of images",
                            width=100, height=4,
                            fg="blue")

# Button for single file browser
button_explore = Button(window,
                        text="Browse File",
                        command=browseFiles)

# Perform OCR on a single image
button_convert = Button(window,
                        text="Extract All Text",
                        command=convertFile)

# Perform OCR on a single image but only extract digits
button_convert_digits = Button(window,
                        text="Extract Digits Only",
                        command=convertFile_Digits)

# Button for folder browser
button_exploreBatch = Button(window,
                        text="Browse Directory",
                        command=browseFolder)

# Perform OCR on a whole folder
button_convertBatch = Button(window,
                        text="Extract All Text",
                        command=convertFolder)

# Perform OCR on a whole folder but only extract digits
button_convertBatch_Digits = Button(window,
                        text="Extract Digits Only",
                        command=convertFolder_Digits)

# Exit the program button
button_exit = Button(window,
                     text="Exit",
                     command=exit)


# We choose the grid method for placing the buttons in their respective positions
# This is the label that displays the filepath
label_file_explorer.grid(column=1, row=1)

# The First parameter in pady is the padding on top and the second parameter is padding on the bottom
# Button for single file browser
button_explore.grid(column=1, row=2, pady=(50, 10))

# Perform OCR on a single image
button_convert.grid(column=1, row=4)

# Perform OCR on a single image but only extract digits
button_convert_digits.grid(column=1, row=6)

# Button for folder browser
button_exploreBatch.grid(column=1, row=8, pady=(50, 10))

# Perform OCR on a whole folder
button_convertBatch.grid(column=1, row=10)

# Perform OCR on a whole folder but only extract digits
button_convertBatch_Digits.grid(column=1, row=12)

# Exit the program button
button_exit.grid(column=1, row=14, padx=10, pady=30)

# Keep the application open until the user chooses to exit
window.mainloop()
