#!/bin/bash
echo -e "正在构建..."
# Build the project.
hugo -d docs
# Go To Public folder
cd docs
# Add changes to git.
git add .

# Commit changes.
msg="rebuilding site `date` "

echo -e "\033[0;32m$msg\033[0m"

if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"
# Push source and build repos.
git push 
# Come Back up to the Project Root
cd ..