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

# Application installation
# ========================
# The apps/ directory contains all the opensource apps. The standard build
# process installs all of them. You can use the `app_reg' tool for more
# fine-grain control.
#

export ROOT := $(realpath ..)
include $(ROOT)/Makefile.vars.priv

default: env-install

.PHONY: clean default distclean install

APPS := about \
	beeswax \
	filebrowser \
	help \
	jobbrowser \
	jobsub \
	proxy \
	useradmin

# <<<< SDK ONLY
APPS += hello \
	jframegallery
# END SDK ONLY >>>>

################################################
# Install all applications into the Desktop environment
################################################
EGG_INFO_TARGETS := $(APPS:%=.recursive-egg-info/%)
.recursive-egg-info/%:
	@$(MAKE) -C $* egg-info ext-eggs

.PHONY: env-install
env-install: $(EGG_INFO_TARGETS)
	$(APP_REG) --install $(APPS)


################################################
# Distribution
################################################
INSTALL_BDIST_TARGETS := $(APPS:%=.recursive-install-bdist/%)
.recursive-install-bdist/%: %
	INSTALL_DIR=$(INSTALL_DIR)/apps/$< \
		INSTALL_CONF_DIR=$(INSTALL_DIR)/desktop/conf \
		$(MAKE) -C $< install-bdist

.PHONY: install
install: install-source-parts $(INSTALL_BDIST_TARGETS)

#
# install-source-parts:
#     Installs the non-app parts into the INSTALL_DIR
#
SOURCE_PARTS = Makefile

.PHONY: install-source-parts
install-source-parts:
	mkdir -p $(INSTALL_DIR)/apps
	tar cf - $(SOURCE_PARTS) | tar -C $(INSTALL_DIR)/apps -xf -


################################################
# Clean all the apps
################################################
CLEAN_TARGETS := $(APPS:%=.recursive-clean/%)
DISTCLEAN_TARGETS := $(APPS:%=.recursive-distclean/%)

clean: $(CLEAN_TARGETS)
.recursive-clean/%:
	@$(MAKE) -C $* clean
	@$(APP_REG) --remove $* ||:

distclean: $(DISTCLEAN_TARGETS)
.recursive-distclean/%:
	@$(MAKE) -C $* distclean
	@$(APP_REG) --remove $* ||:
