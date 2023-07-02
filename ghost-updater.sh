#!/bin/bash
date=$(date)
git pull origin master
rm -r docs
mkdir docs
cd docs
#touch .nojekyll
echo "https://abshiro-azhar.github.io" > CNAME
cd -
ECTO1_SOURCE=http://localhost:2368 ECTO1_TARGET=https://abshiro-azhar.github.io/ python3 ecto1.py
##########
cd docs
mkdir content 
mkdir content/images
docker cp dfc84b67c372:/var/lib/ghost/current/content/images content/images
cd -
cp googleba06e62f5a590fbc.html docs/.
##############
grep -lR "srcset" docs/ | xargs sed -i 's/srcset/thisisbuggedatm/g'
git add .
git commit -m "$date"
git config --global credential.helper store
git push -u origin master
