# docs: Franka Control Interface (FCI) documentation source

[![Build Status][travis-status]][travis]

To build the documentation, first build the container, then execute:

    make html

## Local Build

To build the documentation locally, you need to have Python 3.10 or later installed, along with the dependencies specified in `requirements.txt`. You can install the dependencies using pip:

    pip install -r requirements.txt

To trigger the build for internal repos, first remove the existing checked-out sources in 'doc' and let them be re-imported by the Makefile:
```
rm -rf source/doc
make clean
make html REPOS=internal_upstream.repos
```

## License

The source code and generated documents are licensed under the [Apache 2.0 license][apache-2.0].

[apache-2.0]: https://www.apache.org/licenses/LICENSE-2.0.html
[travis-status]: https://travis-ci.org/frankarobotics/docs.svg?branch=master
[travis]: https://travis-ci.org/frankarobotics/docs
