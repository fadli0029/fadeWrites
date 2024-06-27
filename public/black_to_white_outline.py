from PIL import Image

# Load the image
img = Image.open('me.png').convert('RGBA')

# Convert to RGBA if not already in that mode
data = img.getdata()

# Create a new image with the same mode and size
new_data = []
for item in data:
    # Change all black (also shades of black)
    if item[0] < 50 and item[1] < 50 and item[2] < 50:  # RGB values less than 50 (black)
        new_data.append((255, 255, 255, item[3]))  # Change to white and keep alpha channel
    else:
        new_data.append(item)

# Update image data
img.putdata(new_data)

# Save the modified image
img.save('me_white.png')
