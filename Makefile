# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python3 -msphinx
SPHINXPROJ    = research-interface
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean html import-repos generate-js

# Generate compatibility data JavaScript file
generate-js:
	@chmod +x $(SOURCEDIR)/_static/generate_compatibility_js.py
	@$(SOURCEDIR)/_static/generate_compatibility_js.py

# Import VCS repositories for documentation
import-repos:
	@echo "Importing VCS repositories..."
	@rm -rf $(SOURCEDIR)/doc
	@mkdir -p $(SOURCEDIR)/doc
	@vcs import --input rolling.repos $(SOURCEDIR)/doc
	@echo "Copying prepared franka_ros2 documentation..."
	@rm -rf $(SOURCEDIR)/doc/franka_ros2
	@cp -r franka_ros2 $(SOURCEDIR)/doc/

# Clean build directory and doc imports
clean:
	rm -rf $(BUILDDIR)/*
	rm -rf $(SOURCEDIR)/doc
	rm -rf $(SOURCEDIR)/franka_ros2
	rm -rf $(SOURCEDIR)/libfranka

# Custom html target that first imports repos, generates JS, clones franka_ros2 and libfranka, then builds
html: generate-js
	@echo "Importing documentation repositories..."
	@if [ ! -d "$(SOURCEDIR)/franka_ros2" ] || [ ! -d "$(SOURCEDIR)/libfranka" ]; then \
		cd $(SOURCEDIR) && vcs import --input ../upstream.repos .; \
	fi
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
