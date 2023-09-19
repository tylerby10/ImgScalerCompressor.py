# Python Script used on PNG Images to scale them down to a more efficient size for web use.
# It will also convert the PNG image to a webp file.
# This script will iterate through the directory where it is located to find the images.
# There are several helpful errors and logs generated as well.

# Import necessary libraries
import os
import ctypes
from PIL import Image

# Disable the maximum image pixel limit in Pillow (PIL)
Image.MAX_IMAGE_PIXELS = None

# Check if the "Compressed" folder exists; if not, create it
if not os.path.exists("Compressed"):
    os.makedirs("Compressed")

# Get a list of all files in the current directory
files = os.listdir()

# Open log files for writing
with open("Compressed/duplicate_names.txt", "w") as duplicate_log_file:
    with open("Compressed/Missed PNGs.txt", "w") as missed_log_file:
        # Loop through all files in the current directory
        for file in files:
            # Check if the file is a PNG image (case-insensitive)
            if file.endswith(".png") or file.endswith(".PNG"):
                # Open the PNG image
                img = Image.open(file)

                # Get the size of the image
                width, height = img.size

                # Determine the longest dimension
                longest_dimension = max(width, height)

                # Check if the image is larger than 800px on the longest dimension
                if longest_dimension > 800:
                    # If it is, resize the image to 800px on the longest dimension
                    if width >= height:
                        new_height = int(800 * height / width)
                        img = img.resize((800, new_height), Image.ANTIALIAS)
                    else:
                        new_width = int(800 * width / height)
                        img = img.resize((new_width, 800), Image.ANTIALIAS)

                # Create the output filename with a .webp extension
                output_filename = "{}.webp".format(os.path.splitext(file)[0])

                # Print a message indicating the file being processed
                print("Processing file: {}".format(file))

                # Check if the output file already exists in the "Compressed" folder
                if os.path.exists(os.path.join("Compressed", output_filename)):
                    # If it does, log the duplicate filename
                    duplicate_log_file.write("{}\n".format(output_filename))
                else:
                    try:
                        # Save the image as a WEBP image with a compression quality of 75
                        img.save(os.path.join("Compressed", output_filename), "WEBP", quality=75)
                    except Exception as e:
                        # If the save fails, log the missed PNG filename
                        missed_log_file.write("{}\n".format(file))
                        print("Failed to compress {}: {}".format(file, e))

# Check if there are any duplicate PNG filenames in the log
if os.path.getsize("Compressed/duplicate_names.txt") > 0:
    # If duplicates exist, display an error dialog
    ctypes.windll.user32.MessageBoxW(0, "Error: Duplicate filenames! Please check the txt log in Compressed.", "Error", 0x40 | 0x1)

# Check if there are any missed PNG files in the log
if os.path.getsize("Compressed/Missed PNGs.txt") > 0:
    # If misses exist, display an error dialog
    ctypes.windll.user32.MessageBoxW(0, "Error: Missed PNG! Please check the txt log in Compressed.", "Error", 0x40 | 0x1)
