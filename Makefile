buildroot = /
python_version = 3
python_lookup_name = python$(python_version)
python = $(shell which $(python_lookup_name))
docdir = /usr/share/doc/packages
sc_disable = SC1091,SC2086,SC2317

version := $(shell \
	$(python) -c \
	'from kiwi_boxed_plugin.version import __version__; print(__version__)'\
)

install:
	# install plugin manual page and license/readme
	# NOTE: this file is not handled through pip because on system level
	install -d -m 755 ${buildroot}usr/share/man/man8
	gzip -f doc/build/man/kiwi::system::boxbuild.8
	install -m 644 doc/build/man/kiwi::system::boxbuild.8.gz \
		${buildroot}usr/share/man/man8
	install -d -m 755 ${buildroot}${docdir}/python-kiwi_boxed_plugin
	install -m 644 LICENSE \
		${buildroot}${docdir}/python-kiwi_boxed_plugin/LICENSE
	install -m 644 README.rst \
		${buildroot}${docdir}/python-kiwi_boxed_plugin/README

setup:
	poetry install --all-extras

docs: setup
	poetry run make -C doc man

check: setup
	# shell code checks
	bash -c 'shellcheck -e ${sc_disable} boxes/images.sh -s bash'
	# python flake tests
	poetry run flake8 --statistics -j auto --count kiwi_boxed_plugin
	poetry run flake8 --statistics -j auto --count test/unit

test: setup
	# python static code checks
	poetry run mypy kiwi_boxed_plugin
	# unit tests
	poetry run bash -c 'pushd test/unit && pytest -n 5 \
		--doctest-modules --no-cov-on-fail --cov=kiwi_boxed_plugin \
		--cov-report=term-missing --cov-fail-under=100 \
		--cov-config .coveragerc'

build: clean check test
	# build the sdist source tarball
	poetry build --format=sdist
	# provide rpm source tarball
	mv dist/kiwi_boxed_plugin-${version}.tar.gz \
		dist/python-kiwi-boxed-plugin.tar.gz
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

prepare_for_pypi: clean setup
	# sdist tarball, the actual publishing happens via the
	# ci-publish-to-pypi.yml github action
	poetry build --format=sdist

clean:
	rm -rf dist
	rm -rf doc/build
	rm -rf doc/dist
