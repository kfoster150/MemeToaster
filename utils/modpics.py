# This is a quick and dirty script for copying all of the pictures from input folders
# to the db folder while changing their names to categoryN.ext

import os, re, shutil

inputImageDir = './data/images/input'
outputImageDir = './data/images/db'
categories = os.listdir(inputImageDir)
categories.sort()

for category in categories:
    categoryPath = os.path.join(inputImageDir, category)
    images = os.listdir(categoryPath)

    count = 1
    for image in images:    
        oldPath = os.path.join(inputImageDir, category, image)
        extension = re.search("\.[a-zA-Z]{3,4}$", image)[0]
        newName = category + str(count) + extension
        newPath = os.path.join(outputImageDir, newName)
        shutil.copy(oldPath, newPath)
        print(newName)
        count += 1
