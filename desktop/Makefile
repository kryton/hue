#
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# <<<< DEV ONLY
#
# This Makefile essentially lists the applications, and delegates build targets
# through to them.
#
# The interesting bit is done by the recursive_app_make_target macro (see below).
# In essence, the important targets are:
#
#   install-binary-apps
#      installs built applications into the install dir, without
#      installing them into a virtual environment.
#
#   env-install
#      installs all of the applications into the virtual environment
#
#   clean
#      cleans up
#
# END DEV ONLY >>>>

export ROOT := $(realpath ..)
DESKTOP_ROOT := $(realpath .)
include $(ROOT)/Makefile.vars.priv

APPS := core \
	libs/hadoop

.PHONY: default
default:: desktop syncdb

###################################
# Configuration
###################################


# <<<< DEV ONLY
CONF_INI := $(patsubst $(CONF_DIR)/%.ini.tmpl,$(CONF_DIR)/%.ini,\
              $(wildcard $(CONF_DIR)/*.ini.tmpl))

# Template ini to rewrite
$(CONF_DIR)/%.ini:: $(CONF_DIR)/%.ini.tmpl
	@echo "--- Rewriting $@"
	sed -e 's:$$HADOOP_HOME:$(HADOOP_HOME):' $< > $@

# Pattern rule for desktop config file
.PHONY: conf
conf: $(CONF_INI)

default:: conf
# END DEV ONLY >>>>

###################################
# Build apps
###################################

# <<<< DEV ONLY
include $(DESKTOP_ROOT)/devtools.mk
# END DEV ONLY >>>>

.PHONY: syncdb
syncdb: $(DESKTOP_DB)

$(DESKTOP_DB): $(BLD_DIR_BIN)/desktop
	@echo "--- Regenerating database at $@"
	@if [ -n "$(DESKTOP_DEBUG)" ]; then \
	  echo 'Removing old database (DESKTOP_DEBUG is set)' ; \
	  rm -f $@ ; \
	fi
	@echo "--- Syncing/updating database at $@"
	@$(BLD_DIR_BIN)/desktop syncdb --noinput
	@$(BLD_DIR_BIN)/desktop migrate

# Targets that simply recurse into all of the applications
ENV_INSTALL_TARGETS := $(APPS:%=.recursive-env-install/%)
.recursive-env-install/%: %
	$(MAKE) -C $< env-install

CLEAN_TARGETS := $(APPS:%=.recursive-clean/%)
.recursive-clean/%: %
	$(MAKE) -C $< clean

DISTCLEAN_TARGETS := $(APPS:%=.recursive-distclean/%)
.recursive-distclean/%: %
	$(MAKE) -C $< distclean

.PHONY: env-install
env-install: $(ENV_INSTALL_TARGETS)

.PHONY: clean
clean: $(CLEAN_TARGETS)
	@rm -f $(BLD_DIR)/.devtools

.PHONY: distclean
distclean: clean $(DISTCLEAN_TARGETS)


#
# desktop target
#
.PHONY: desktop
# <<<< DEV ONLY
desktop: $(BLD_DIR)/.devtools
# END DEV ONLY >>>>
desktop: env-install


###################################
# Distribution
###################################

INSTALL_BDIST_TARGETS := $(APPS:%=.recursive-install-bdist/%)
.recursive-install-bdist/%: %
	INSTALL_DIR=$(INSTALL_DIR)/desktop/$< \
		INSTALL_CONF_DIR=$(INSTALL_DIR)/desktop/conf \
		$(MAKE) -C $< install-bdist

.PHONY: install
install: install-source-parts $(INSTALL_BDIST_TARGETS)

#
# install-source-parts:
#     Installs the non-app parts (eg makefiles, conf) into
#     the INSTALL_DIR
#
# We should move all of the libs/* into some kind of container
# python app, or into core.
# TODO(todd) deal with these JS dependencies
#
SOURCE_PARTS = \
  $(wildcard *.mk) Makefile \
  conf \
  libs/fancyupload \
  libs/mootools-color \
  libs/mootools-slick \
  libs/mootools-touch \
  libs/protovis

.PHONY: install-source-parts
install-source-parts:
	@mkdir -p $(INSTALL_DIR)/desktop
	@tar cf - $(SOURCE_PARTS) | tar -C $(INSTALL_DIR)/desktop -xf -
