# Open the file in read mode first to get existing stop words
with open(".\\stop_hinglish.txt", 'r') as f:
    stop_words = f.read().splitlines()

# Add new stop words to the list
new_stop_words = [
    "<media",
    "omitted>",
    "<media ",
    "to",
    "or",
    "hai",
    "omitted",
    "media",
    " ",
    "<media omitted>"
]

# Append new stop words to the existing list
stop_words.extend(new_stop_words)

# Write the updated list back to the file
with open(".\\stop_hinglish.txt", 'a') as f:
    for word in stop_words:
        f.write(word + '\n')  # Write each stop word on a new line
