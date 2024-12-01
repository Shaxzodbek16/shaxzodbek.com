#!/bin/bash
DIR_PATH="/var/www/shaxzodbek.com/shaxzodbek"
cd "$DIR_PATH" || exit
git add .
git commit -m "Daily auto-commit"
git push origin main
git push origin main

(crontab -l 2>/dev/null; echo "0 0 * * * /Users/shaxzodbek/Developer/shaxzodbek.com/backup.sh") | crontab -
