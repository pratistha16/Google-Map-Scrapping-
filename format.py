import re
import pandas as pd

# Define the input file path and output file path
input_file_path = r'D:\Tuna Technology\GoogleMapsScrapping\dairies_in_butwal.txt'
output_file_path = r'D:\Tuna Technology\GoogleMapsScrapping\formatted_dairydata_butwal.xlsx'

# Read the raw text data from the input file
with open(input_file_path, 'r', encoding='utf-8') as file:
    text_data = file.read()

# Regular expression pattern to capture each dairy or farm’s details
pattern = re.compile(
    r'(?P<Name>.+?)\n'                     # Name
    r'(?P<Rating>\d+\.\d+\(\d+\))?\n?'     # Rating, optional and ignored
    r'(?P<Type>डेरी फार्म|डेरी स्टोर|पशुधन उत्पादन|दूध वितरण सेवा|एशियाई किराना स्टोर|आइसक्रिम|बेकरी|खेती|डेरी आपूर्तिकर्ता)\s*·\s*'
    r'(?P<Location>[^\n]+)?\n'              # Location
    r'(बन्द छ ⋅ (?P<Opening_Hours>[^\n]+)\s*⋅ खुल्छ)?\s*'   # Opening hours
    r'(?P<Contact_Number>\d{3,}-\d{3,}|\d{10})?',  # Contact Number (last known element)
    re.MULTILINE
)

# Initialize a list to store extracted data
data = []

# Extract data based on the regular expression pattern
for match in pattern.finditer(text_data):
    # Extract each named group and handle missing data
    name = match.group('Name').strip() if match.group('Name') else ''
    dairy_type = match.group('Type').strip() if match.group('Type') else ''
    location = match.group('Location').strip() if match.group('Location') else ''
    opening_hours = match.group('Opening_Hours').strip() if match.group('Opening_Hours') else ''
    contact_number = match.group('Contact_Number').strip() if match.group('Contact_Number') else ''
    
    # Append the extracted details as a dictionary
    data.append({
        "Name": name,
        "Type": dairy_type,
        "Location": location,
        "Opening Hours": opening_hours,
        "Contact Number": contact_number,
    })

# Convert data to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel(output_file_path, index=False)

print(f"Data saved to {output_file_path}")
