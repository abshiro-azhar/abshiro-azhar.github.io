#!/bin/bash
date=$(date)
git pull origin master
rm -r docs
mkdir docs
cd docs
touch .nojekyll
echo "https://abshiro-azhar.github.io/ghost-blog/" > CNAME
cd -
ECTO1_SOURCE=http://localhost:2368 ECTO1_TARGET=https://abshiro-azhar.github.io/ghost-blog/ python3 ecto1.py
cd docs
mkdir content 
docker cp dfc84b67c372:/var/lib/ghost/content/images/. content/images
cd -
grep -lR "srcset" docs/ | xargs sed -i 's/srcset/thisisbuggedatm/g'
git add .
git commit -m "$date"
git config --global credential.helper store
git push -u origin master