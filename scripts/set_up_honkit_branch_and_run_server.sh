#!/bin/bash
# A bash script to set up the honkit branch
echo "Note: Please commit or stash any changes before running; also make sure that you've rebased on main."
current_git_branch=$(git symbolic-ref --short HEAD)
git checkout honkit &&
git rebase $current_git_branch &&
npx honkit serve
