# Python Script used on PNG Images to scale them down to a more efficient size for web use.
# It will also convert the PNG image to a WEBP file.
# This script will iterate through the directory where it is located to find the images.
# There are several helpful errors and logs generated as well.

# Import necessary libraries
import os
from PIL import Image

# Optional: Use a notification library for desktop notifications
try:
    import notify2
    notify2.init("Image Compression Script")
except ImportError:
    notify2 = None  # Fallback to terminal notifications

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
            if file.lower().endswith(".png"):
                # Open the PNG image
                try:
                    img = Image.open(file)
                except Exception as e:
                    print(f"Failed to open {file}: {e}")
                    missed_log_file.write(f"{file}\n")
                    continue

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
                output_filename = f"{os.path.splitext(file)[0]}.webp"
                output_filepath = os.path.join("Compressed", output_filename)

                # Print a message indicating the file being processed
                print(f"Processing file: {file}")

                # Check if the output file already exists in the "Compressed" folder
                if os.path.exists(output_filepath):
                    # If it does, log the duplicate filename
                    duplicate_log_file.write(f"{output_filename}\n")
                else:
                    try:
                        # Save the image as a WEBP image with a compression quality of 75
                        img.save(output_filepath, "WEBP", quality=75)
                    except Exception as e:
                        # If the save fails, log the missed PNG filename
                        missed_log_file.write(f"{file}\n")
                        print(f"Failed to compress {file}: {e}")

# Check if there are any duplicate PNG filenames in the log
if os.path.getsize("Compressed/duplicate_names.txt") > 0:
    duplicate_message = "Error: Duplicate filenames found! Please check the duplicate_names.txt log in Compressed."
    if notify2:
        n = notify2.Notification("Image Compression Script", duplicate_message)
        n.show()
    else:
        print(duplicate_message)

# Check if there are any missed PNG files in the log
if os.path.getsize("Compressed/Missed PNGs.txt") > 0:
    missed_message = "Error: Missed PNG files! Please check the Missed PNGs.txt log in Compressed."
    if notify2:
        n = notify2.Notification("Image Compression Script", missed_message)
        n.show()
    else:
        print(missed_message)
