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
	
#### Arguments
	python -m structcheck "/path/to/scan" "/path/to/config.json"

### Python usage

	import structcheck
	
	txt, reports, logs = structcheck.main()  # Same as command 'python -m structcheck'
	
	txt, reports, logs = structcheck.scan(path_root, path_conf, path_report, path_data, display=True)  # See source or documentation code for more infos on arguments
	
	txt, reports, logs = structcheck.report(path_root, path_conf, path_report, path_data, reports, logs)  # Generate the report txt from reports and logs (you can add custom errors into 'reports' variable and re-generate 'txt' variable.

