deploy_pypi:
	echo "Make sure to set JAPPER_DEV variable in utils.py to False"
	rm -rf src/japper.egg-info
	rm -rf build dist
	rm -rf src/japper_devtools/forge/linked_working_dir
	rm -rf src/japper_devtools/forge/tmp_preview.py
	python -m build
	python -m twine upload dist/*