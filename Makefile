deploy_pypi:
	echo "Make sure to set JAPPER_DEV variable in utils.py to False"
	rm -rf build dist
	python -m build
	python -m twine upload dist/*