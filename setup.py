# Brita 0.1 - a backlight adjuster for Linux
# Copyright (C) 2014 Przemysław Buczkowski <przemub@przemub.pl>
# This file is distributed under the MIT license.

from DistUtilsExtra.auto import setup
from os import rename

rename("brita.py", "brita")

setup(
	name         = "brita",
	version      = "0.1",
	description  = "backlight adjuster for Linux",
	author       = "Przemysław Buczkowski",
	author_email = "przemub@przemub.pl",
	url          = "https://github.com/przemub/brita/",
	scripts      = [ "brita" ]
	)

rename("brita", "brita.py")
