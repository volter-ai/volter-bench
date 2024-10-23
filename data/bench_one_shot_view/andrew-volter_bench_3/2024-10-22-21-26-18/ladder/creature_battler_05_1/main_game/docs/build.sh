#!/bin/bash


# Read the game_name property from volter.json
game_name=$(sed -n 's/.*"game_name": *"\([^"]*\)".*/\1/p' volter.json)

# Read the include property from volter.json and clean up the file names
include=$(sed -n '/^[[:space:]]*"include": *\[/,/^[[:space:]]*\]/p' volter.json |
         sed '1d;$d' |
         sed 's/^[[:space:]]*"//;s/"[[:space:]]*,\?$//' |
         tr '\n' ' ' |
         sed 's/"//g')

# Use a more robust method to split the include string into an array and trim spaces
IFS=$'\n' read -d '' -ra files_and_directories < <(echo "$include" | sed 's/[[:space:]]*,[[:space:]]*/\n/g' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

# Print the files and directories for debugging
echo "Files and directories to be zipped:"
printf '%s\n' "${files_and_directories[@]}"

# Check if files exist before zipping
existing_files=()
for file in "${files_and_directories[@]}"; do
    if [ -e "$file" ]; then
        existing_files+=("$file")
    else
        echo "Warning: $file does not exist and will not be included in the zip"
    fi
done

# Create zip file with existing files
if [ ${#existing_files[@]} -gt 0 ]; then
    zip -r "${game_name}.zip" "${existing_files[@]}"
    echo "Zip file '${game_name}.zip' created with existing files and directories."
else
    echo "Error: No files found to zip"
    exit 1
fi

# Specify your S3 bucket name
s3_bucket="volter-builds"

# Upload the ZIP file to the specified S3 bucket
aws s3 cp "${game_name}.zip" "s3://$s3_bucket/"

if [ $? -eq 0 ]; then
    echo "Successfully uploaded '${game_name}.zip' to 's3://$s3_bucket/'."
else
    echo "Failed to upload '${game_name}.zip' to S3."
    exit 1
fi

rm "${game_name}.zip"
