server:
	cd arewefast && python app.py

migrate:
	cd arewefast && python manage.py db migrate && python manage.py db upgrade

test:
	python -m unittest discover

authors:
	echo "# Authors\n\nA huge thanks to all of our contributors:\n" > AUTHORS.md
	git log --raw | grep "^Author: " | cut -d ' ' -f2- | cut -d '<' -f1 | sed 's/^/* /' | sort | uniq >> AUTHORS.md
