#!/bin/bash

echo "Creating README.md files in all folders..."

# Template content generator
generate_readme() {
  local folder_name="$1"
  cat <<EOF
# ${folder_name}

## Purpose
Describe what this component does and why it exists.

## Responsibilities
- Responsibility 1
- Responsibility 2
- Responsibility 3

## How to Run (Local)
Provide commands or instructions for local development.

## How It Connects to the Platform
- **Upstream:** Who sends data into this component?
- **Downstream:** Who consumes the output?

## Folder Structure
Explain important files or submodules here.

## Configuration
List environment variables or configuration files required.

## Notes
Add any useful onboarding, debugging, or architectural notes.
EOF
}

# Loop through all directories (recursively)
find . -type d | while read -r dir; do
  readme_path="$dir/README.md"

  # Skip writing a README in root (unless you want one)
  if [[ "$dir" == "." ]]; then
    continue
  fi

  # Extract folder name (replace ./apps/api with just "api")
  folder_name=$(basename "$dir")

  echo "Creating $readme_path"
  generate_readme "$folder_name" > "$readme_path"
done

echo "All README.md files created!"
