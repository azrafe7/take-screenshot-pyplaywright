#!/usr/bin/env bash
set -e

export PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/ms-playwright

pip install -r requirements.txt
playwright install

echo ms-playwright
ls /opt/render/project/ms-playwright -R | grep ":$" | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/'
echo 
echo cache ms-playwright
ls /opt/render/.cache/ms-playwright -R | grep ":$" | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/'
echo
echo chrome ms-playwright
ls /opt/render/.cache/ms-playwright/chromium-1140/chrome-linux/chrome/*.*

#ls /opt/render/project/playwright

#ls $PLAYWRIGHT_BROWSERS_PATH

# Store/pull Playwright cache with build cache
#if [[ ! -d $PLAYWRIGHT_BROWSERS_PATH ]]; then 
#  echo "...Copying Playwright Cache from Build Cache" 
#  cp -R $XDG_CACHE_HOME/playwright/ $PLAYWRIGHT_BROWSERS_PATH
#else 
#  echo "...Storing Playwright Cache in Build Cache" 
#  cp -R $PLAYWRIGHT_BROWSERS_PATH $XDG_CACHE_HOME
#fi