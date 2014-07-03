

For the Self-Organizing Map to work, you need to have [PyMVPA installed][]. To get the *latest
version*, you need to install from source (running `sudo aptitude install python-mvpa2` is **not**
enough).

[PyMVPA installed]: http://www.pymvpa.org/installation.html#building-from-source

Here's a sample ipython script that does the actual work:

		%run import_from_hygxyz_csv.py  # or: from import_from_hygxyz_csv import import_from_csv
		stars = import_from_csv()
		%run create_som.py  						# or: from create_som import organize
		organize(stars)

