import os

current_path = os.path.dirname(__file__)
# Navigate up one directory to "Submission 2" and then to "static/images/harnverhalt"
target_path = os.path.normpath(os.path.join(current_path, "..", "static", "images", "harnverhalt"))

print(target_path)