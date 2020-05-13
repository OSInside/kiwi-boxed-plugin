python_version = 3
python_lookup_name = python$(python_version)
python = $(shell which $(python_lookup_name))
docdir = /usr/share/doc/packages

version := $(shell \
	$(python) -c \
	'from kiwi_boxed_plugin.version import __version__; print(__version__)'\
)

tox:
	tox "-n 5"

install:
	# apart from all python source we also need to install
	# the manual page and the plugin configuration
	# see setup.py for details when this target is called
	install -d -m 755 ${buildroot}usr/share/man/man8
	for man in doc/build/man/*.8; do \
		test -e $$man && gzip -f $$man || true ;\
	done
	for man in doc/build/man/*.8.gz; do \
		install -m 644 $$man ${buildroot}usr/share/man/man8 ;\
	done
	# box configuration
	install -d -m 755 ${buildroot}etc
	install -m 644 kiwi_boxed_plugin.yml ${buildroot}etc/kiwi_boxed_plugin.yml

install_package_docs:
	install -d -m 755 ${buildroot}${docdir}/python-kiwi_boxed_plugin
	install -m 644 LICENSE \
		${buildroot}${docdir}/python-kiwi_boxed_plugin/LICENSE
	install -m 644 README.rst \
		${buildroot}${docdir}/python-kiwi_boxed_plugin/README

build: clean tox
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

pypi: clean tox
	$(python) setup.py sdist upload

clean:
	$(python) setup.py clean
	rm -rf doc/build
	rm -rf dist/*
