# 2. Clean the raw data file:
#    - Remove comment lines
#    - Remove empty lines
#    - Remove extra commas
#    - Extract essential columns: patient_id, visit_date, age, education_level, walking_speed
#    - Save the file as `ms_data.csv`

#!/bin/bash

# Input and output file paths
input_file="/Users/avantikasharma/09-second-exam-AvantikaSharma3357/ms_data_dirty.csv"
output_file="/Users/avantikasharma/09-second-exam-AvantikaSharma3357/ms_data.csv"

# Temporary file to store cleaned data
clean_file=$(mktemp)

# Remove comment lines, empty lines, and extra commas
grep -v '^#' "$input_file" | grep -v '^$' | sed 's/,,*/,/g' > "$clean_file"

# Extract header
header=$(head -n 1 "$clean_file")
echo "Header found: $header"

# Get column indices for the desired fields
columns=$(echo "$header" | tr ',' '\n' | nl -v 1)
echo "Columns with indices:"
echo "$columns"

patient_id_col=$(echo "$columns" | grep -i 'patient_id' | awk '{print $1}')
visit_date_col=$(echo "$columns" | grep -i 'visit_date' | awk '{print $1}')
age_col=$(echo "$columns" | grep -i 'age' | awk '{print $1}')
education_level_col=$(echo "$columns" | grep -i 'education_level' | awk '{print $1}')
walking_speed_col=$(echo "$columns" | grep -i 'walking_speed' | awk '{print $1}')

# Extract the required columns and save to the output file
awk -F',' -v p="$patient_id_col" -v v="$visit_date_col" -v a="$age_col" -v e="$education_level_col" -v w="$walking_speed_col" \
'NR==1 {print $p, $v, $a, $e, $w}
NR>1 {print $p, $v, $a, $e, $w}' OFS=',' "$clean_file" > "$output_file"

echo "Cleaned data saved to $output_file"


## 3. Create a file, `insurance.lst` listing unique labels for a new variable, `insurance_type`, one per line (your choice of labels). 
# Create insurance.lst with unique labels for `insurance_type`
insurance_file="insurance.lst"

# Add a header row and three unique insurance types
echo "insurance_type" > "$insurance_file"
echo "Private" >> "$insurance_file"
echo "Medicaid" >> "$insurance_file"
echo "Uninsured" >> "$insurance_file"

echo "File created: $insurance_file"

## 4. Generate a summary of the processed data:
processed_file="/Users/avantikasharma/09-second-exam-AvantikaSharma3357/ms_data.csv"

# Count the total number of visits (rows, not including the header)
total_visits=$(tail -n +2 "$processed_file" | wc -l)
echo "Total number of visits: $total_visits"

# Display the first few records 
echo "First few records:"
head -n 6 "$processed_file"
