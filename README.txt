Hello and thank you for reviewing my project

I have included many comments with instructions in my actual python code file
However, I am including some more instructions here
Please note that when converting a whole folder of images at the same time, if on a weaker machine, the application may sometimes say "Not Responding"
THE PROGRAM HAS NOT CRASHED! It is simply processing the whole folder of images

Before attempting to run my python code, you must follow these instructions:
# 1. Install tesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki
# 2. Note the tesseract path from the installation. If installing for all users, the default path is below
# 3. pip install pytesseract
# 4. Set the tesseract path in the line below if it's different from your own personal path
 
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

Note this line above from my code, and make sure you change it to the install path of tesseract if it's different than your own. Otherwise the code will throw an error from tesseract not being set up correctly. Please let me know if you have any issues with this or anything else

When you run the code, you must select an image with the "Browse File" button before pressing the extract text buttons
Performing OCR on a single image will create the text file version of the image with the same name as the image in the same directory as the image

Alternatively, you may also select a whole folder by clicking the "Browse Directory" button. After clicking "Browse Directory," click on a folder and then click on the select folder button in your file explorer to open this folder
After selecting a folder and clicking the "Extract All Text" button, the contents of all the images within the folder will be appended to a text file named "batchConversion.txt" inside of the selected folder

Clicking "Extract Digits Only" will perform the same functionality but will only extract digits from the text and not regular characters

Along with my python code/research paper/powerpoint, I have included some example datasets from my input data. The dataset titled "dataset_with_results" is very large and already has the results of performing OCR inside this folder in a text file: "batchConversion.txt". Attempting to perform OCR again on this folder will throw an error because there is already a text file with results in this folder. 
This is a link to the competition page that I obtained this scanned receipts dataset from: ICDAR 2019 Robust Reading Challenge on Scanned Receipts OCR and Information Extraction https://rrc.cvc.uab.es/?ch=13&com=downloads
You must make an account to download the full dataset, however of course I am including the portion of input data I used from this dataset along with results under the "dataset_with_results" folder. There are 359 images of receipts in this dataset

The other folder named "smaller_dataset" does not have a results text file inside and is a good candidate for testing my code for yourself on a smaller folder of scanned receipts. My OCR application will overall work the best on scanned good quality images such as these. Although the pre-processing methods that I have implemented do well to reduce noise in images which have some amount of noise or images that are not scanned well too.

