python_version = 3
python_lookup_name = python$(python_version)
python = $(shell which $(python_lookup_name))

version := $(shell \
	$(python) -c \
	'from kiwi_boxed_plugin.version import __version__; print(__version__)'\
)

tox:
	tox "-n 5"

build: clean
	# create setup.py variant for rpm build.
	# delete module versions from setup.py for building an rpm
	# the dependencies to the python module rpm packages is
	# managed in the spec file
	sed -ie "s@>=[0-9.]*'@'@g" setup.py
	# build the sdist source tarball
	$(python) setup.py sdist
	# restore original setup.py backed up from sed
	mv setup.pye setup.py
	# provide rpm source tarball
	mv dist/kiwi_boxed_plugin-${version}.tar.gz \
		dist/python-kiwi_boxed_plugin.tar.gz
	# update rpm changelog using reference file
	helper/update_changelog.py \
		--since package/python-kiwi_boxed_plugin.changes \
	> dist/python-kiwi_boxed_plugin.changes
	helper/update_changelog.py \
		--file package/python-kiwi_boxed_plugin.changes \
	>> dist/python-kiwi_boxed_plugin.changes
	# update package version in spec file
	cat package/python-kiwi_boxed_plugin-spec-template |\
		sed -e s'@%%VERSION@${version}@' \
	> dist/python-kiwi_boxed_plugin.spec
	# provide rpm rpmlintrc
	cp package/python-kiwi_boxed_plugin-rpmlintrc dist

clean:
	$(python) setup.py clean
	rm -rf doc/build
	rm -rf dist/*
