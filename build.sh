#!/usr/bin/env bash
set -e

export PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/playwright

pip install -r requirements.txt
playwright install

#ls $PLAYWRIGHT_BROWSERS_PATH

# Store/pull Playwright cache with build cache
#if [[ ! -d $PLAYWRIGHT_BROWSERS_PATH ]]; then 
#  echo "...Copying Playwright Cache from Build Cache" 
#  cp -R $XDG_CACHE_HOME/playwright/ $PLAYWRIGHT_BROWSERS_PATH
#else 
#  echo "...Storing Playwright Cache in Build Cache" 
#  cp -R $PLAYWRIGHT_BROWSERS_PATH $XDG_CACHE_HOME
#fi