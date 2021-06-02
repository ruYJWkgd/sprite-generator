import os
import sys
import re

regex_to_get_viewbox_size = re.compile('viewBox=\"([\d\s\.]*)\"')
regex_to_get_svg_contents = re.compile('<svg.*?>(.*)</svg>')
sprite_content = '<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">\n'

print("Enter the path to the folder containing the SVGs you want to create a sprite from")
folder_holding_svgs = input("Path: ").replace("'", '"').replace("\\", "").rstrip() # clean the input string to ensure it is in the correct format

# Move into that folder
os.chdir(folder_holding_svgs)

print("Creating sprite file...")
for each_svg_file in os.listdir(folder_holding_svgs):
  if each_svg_file.endswith("svg"):
    # Open the SVG
    file_object = open(each_svg_file, "r")

    # Read the contents
    text_from_file = file_object.read()

    # Make the SVG a single line of text
    text_from_file = text_from_file.replace("\n", "")

    # get the file name and extension
    svg_filename, svg_fileext = os.path.splitext(each_svg_file)
    
    # pull out the viewbox data
    viewbox_size = regex_to_get_viewbox_size.search(text_from_file).group(1)

    # Pull out the content between the opening and closing SVG tags
    svg_content = regex_to_get_svg_contents.search(text_from_file).group(1)

    # Put that content into the sprite_content
    sprite_content = sprite_content + "\t" + '<symbol id="' + svg_filename + '" viewBox="' + viewbox_size + '">' + svg_content + '</symbol>\n'

# Add the ending tag to the sprite file
sprite_content = sprite_content + '</svg>\n'

# Save the sprite file
with open('svg_sprite.svg', 'w') as f:
  f.write(sprite_content)

# Check to make sure the sprite file is now in the folder
if os.path.exists("svg_sprite.svg"):
  print("Sprite creation complete")
else:
  print("There was a problem creating the file")
