# importing the necessary libraries
print("\nimporting libraries.\n")
import pymupdf
import os
import re
import shutil
import spacy
print("libraries imported!\n")

# making the directories

dir1 = "images/"
dir2 = "exceptions/"

if os.path.exists(dir1):
    shutil.rmtree(dir1)
    print("existing \"images\" directory deleted.")
os.makedirs(dir1)
print("new \"images\" directory created.\n")

if os.path.exists(dir2):
    shutil.rmtree(dir2)
    print("existing \"exceptions\" directory deleted.")
os.makedirs(dir2)
print("new \"exceptions\" directory created.\n\nstarting image extraction.\n")

for file in os.listdir("WCR_dir/"): # iterating through the WCR directory

    file_path = f"WCR_dir/{file}" # getting the WCR

    pdf_file = pymupdf.open(file_path)
    page_nums = len(pdf_file)
    
    image_list = [] # creating an empty image list
    name_list = [] # and name list

    for page in range(page_nums):
        page_content = pdf_file[page]
        for i in page_content.get_images(full = True):
            if i[2] >= 250 and i[3] >= 250: # setting minimum height and width for image to filter out miscellaneous and unwanted images
                if i[2] <= 2000 or i[3] <= 2000: # to avoid certain pages which entirely get extracted as an image
                    image_list.append(i) # extracting the images
                    image_bbox = page_content.get_image_bbox(i)
                    x0, y0, x1, y1 = image_bbox
                    text = page_content.get_textbox((60, y1, page_content.rect.width - 60, y1 + 30)) # getting the label present below the image
                    if "Figure" not in text:
                        text = page_content.get_textbox((60, y0 - 30, page_content.rect.width - 60, y0)) # getting the label present above
                    else:
                        text = text.replace("Figure", "") # \
                    text = text.replace("OzAlpha-1", "")  #  | removing frequently appearing words to avoid 
                    text = text.replace("Plumb Road", "") #  | obvious but inaccurate classification
                    text = text.replace("ZeroGen", "")    # /
                    if (len(text) > 250):
                        name_list.append(re.sub("[^a-zA-Z ]", "", text[len(text) - 250:])) # taking only the last 250 characters of the label
                    else:                                                                  # if the text is too long to be named (>255 characters)
                        name_list.append(re.sub("[^a-zA-Z ]", "", text))
                               


    for index, image in enumerate(image_list):
        xref = image[0]
        name = name_list[index]
        
        base_img = pdf_file.extract_image(xref)
        
        image_bytes = base_img["image"]
        image_ext = base_img["ext"]
        
        file_name = name + "." + image_ext
        
        if len(name) > 5 and " " in name and "Drilled Depth" not in name: # filtering out the exceptions with certain conditions
            with open(os.path.join("images/", file_name), "wb") as image_file: 
                image_file.write(image_bytes)
                image_file.close()
        else:
            with open(os.path.join("exceptions/", file_name), "wb") as image_file:
                image_file.write(image_bytes)
                image_file.close()
                
print("all images successfully extracted!\nstarting categorisation.\n")

# NLP and categorisation

nlp = spacy.load("en_core_web_lg")

items = os.listdir("images/")

corpus = [] # building the corpus of names
for i in range (len(items)):
    review = items[i].lower() # lowercasing
    review = review.replace(".jpeg", "").replace(".png", "") # removing extension
    corpus.append(review)

# list of categories
categories = [
    "location map",
    "geological map",
    "structural map",
    "seismic section",
    "log motive",
    "well construction diagram",
    "geotechnical order",
    "remote sensing image",
    "contour maps",
    "drilling plot",
    "stratigraphy and casing plot"
]

# creating "categories" directory
if os.path.exists("categories/"):
    shutil.rmtree("categories/")
    print("existing \"categories\" directory deleted.")
os.makedirs("categories/")
print("new \"categories\" directory created.\n")

# creating seperate directories for each category inside the "categories" directory
for dir in categories:
    dir = "categories/" + dir + "/"
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

# based on the category with highest similarity with the name, the image is categorised into that directory
for index, doc in enumerate (corpus):
    max = 0
    category = ""
    for i in categories:
        if (nlp(doc).similarity(nlp(i)) > max):
            max = nlp(doc).similarity(nlp(i))
            category = i
    shutil.copy("images/" + items[index], "categories/" + category + "/") 
    
print("images have been categorised successfully!\n")