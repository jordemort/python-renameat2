wheel:
	python3 setup.py bdist_wheel

clean:
	rm -rf __pycache__ build dist docs/_build renameat2/_renameat2.* renameat2/__pycache__ renameat2/*.o
#	#git clean -fdx
