import html

# Input string
input_string = "EUW: KC Yiken &lt;br&gt;KR: YIK"

# Decode HTML entities
decoded_string = html.unescape(input_string)

# Split the string by "<br>" (or a space)
parts = decoded_string.split("<br>")

# Initialize the dictionary
result = {}

# Iterate through each part and split by ":"
for part in parts:
    key, value = part.split(":")
    result[key.strip()] = value.strip()

print(result)