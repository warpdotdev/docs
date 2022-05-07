#!/bin/bash
# A bash script to set up the honkit branch
echo "Note: Please commit or stash any changes before running"
current_git_branch=$(git symbolic-ref --short HEAD)
git checkout honkit &&
git pull &&
git rebase $current_git_branch &&
npx honkit serve
