# structcheck
[![Upload Python Package](https://github.com/vincentBenet/structcheck/actions/workflows/python-publish.yml/badge.svg)](https://github.com/vincentBenet/structcheck/actions/workflows/python-publish.yml)
[![Python application](https://github.com/vincentBenet/structcheck/actions/workflows/python-app.yml/badge.svg)](https://github.com/vincentBenet/structcheck/actions/workflows/python-app.yml)
[![Pylint](https://github.com/vincentBenet/structcheck/actions/workflows/pylint.yml/badge.svg)](https://github.com/vincentBenet/structcheck/actions/workflows/pylint.yml)


## Installation
### Pip installation

	pip install structcheck
	

### Version check (linux)

	pip freeze | grep structcheck

### Check installation

	python -m structcheck --help

## Usage

### Shell command

#### No arguments

	python -m structcheck
	
A popup windows will ask you for directory and config file
	
#### Arguments

Path to scan:

	python -m structcheck -p "/path/to/scan"
	
A popup windows will ask you for config file

	python -m structcheck -p "/path/to/scan" -c "/path/to/config.json"

### Python usage

	import structcheck
	
	txt, reports, logs = structcheck.scan()  # Same as command 'python -m structcheck'
	
You can add arguments with:

	txt, reports, logs = structcheck.scan([
		"-p", "/path/to/scan",
		"-c", "/path/to/config.json",
	])