# Organize_Photo-Backups


### Libraries and versions
Created using Python 3.12.1

##### Setup
Used 2 libraries requiring setup using pip:
1. pip install --upgrade pip
1. pip install pillow
1. pip install tqdm

### Why:
1. Photo backup storage can get out of hand quickly and hinder usage of applications such as gmail or apple services when ample space runs out. 
1. With the large sets of data they can be difficult to download and organize as they are often organized in an a random order based on file size or most recent backups.
1. Creating a way to quickly organize large groups of videos and photos quickly based on timestamp meta data to sort them easily in groups will minimize the search for 
1. Creating a personal photo album structure for an external device using the Python pillow library.


### Goal:

1. Sort, label, and rename large groups of photos and videos on an external storage device
1. Create Year and Month folders
1. Move files to folders, keeping the previous naming structure.
1. Setup for adding and testing additional future file types included

### TODO:
1. Currently supports only .jpg and .png file types
1. .mp4 file types will be implemented