#!/bin/bash

USERNAME="lavi324"
TOKEN="${GITHUB_PAT}"

git remote set-url origin https://$USERNAME:$TOKEN@github.com/$USERNAME/sport-tables-ai.git

git add .
git commit -m "Initial commit"
git push origin main
