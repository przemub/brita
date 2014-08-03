#!/bin/sh

chmod +x brita.py
python3 setup.py build_i18n
rm po/brita.pot

if (($? > 0)); then
	echo "Building locales failed"
	exit 1
fi

bold=`tput bold`
normal=`tput sgr0`

echo "Build successful."
echo "${bold}usage:${normal} ./brita.py --help"

