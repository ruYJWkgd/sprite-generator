import os
import sys
import re

regex_to_get_viewbox_size = re.compile('viewBox=\"([\d\s\.]*)\"')
regex_to_get_svg_contents = re.compile('<svg.*?>(.*)</svg>')
regex_to_get_style_contents = re.compile('<style>(.*)</style>')
regex_to_get_style_class_name = re.compile('\.([a-zA-Z0-9_\s\-]*?){')
regex_to_get_style_class_style = re.compile('{(.*?)}')
sprite_content = '<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0">\n'

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
    # Replace bad characters in the filename with good characters
    svg_filename = svg_filename.replace('&', 'and')

    # pull out the viewbox data
    if regex_to_get_viewbox_size.search(text_from_file):
      viewbox_size = regex_to_get_viewbox_size.search(text_from_file).group(1)

    # Pull out the content between the opening and closing SVG tags
    if regex_to_get_svg_contents.search(text_from_file):
      svg_content = regex_to_get_svg_contents.search(text_from_file).group(1)

    # Pull out the content between the opening and closing style tags
    if regex_to_get_style_contents.search(text_from_file):
      style_content = regex_to_get_style_contents.search(text_from_file).group(1)

    # Find the classes in a style tag
    if regex_to_get_style_class_name.search(text_from_file) and regex_to_get_style_class_style.search(text_from_file):
      class_names_list = regex_to_get_style_class_name.findall(style_content)
      class_styles_list = regex_to_get_style_class_style.findall(style_content)

      # Replace those classes with the actual style
      for index in range(len(class_names_list)):
        svg_content = svg_content.replace('class="' + class_names_list[index] + '"', 'style="' + class_styles_list[index] + '"')

    # Remove the style tag section (since we don't need it anymore)
    svg_content = re.sub("<style>.*</style>", "", svg_content)

    # Put that content into the sprite_content
    sprite_content = sprite_content + "\t" + '<symbol id="' + svg_filename.lower() + '" viewBox="' + viewbox_size + '">' + svg_content + '</symbol>\n'

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
