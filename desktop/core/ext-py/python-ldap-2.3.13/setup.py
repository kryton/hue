"""
setup.py - Setup package with the help Python's DistUtils

See http://www.python-ldap.org/ for details.

$Id: setup.py,v 1.65 2009/10/21 17:32:11 stroeder Exp $
"""

has_setuptools = False
try:
	from setuptools import setup, Extension
	has_setuptools = True
except ImportError:
	from distutils.core import setup, Extension

from ConfigParser import ConfigParser
import sys,os,string,time

##################################################################
# Weird Hack to grab release version of python-ldap from local dir
##################################################################
exec_startdir = os.path.dirname(os.path.abspath(sys.argv[0]))
package_init_file_name = reduce(os.path.join,[exec_startdir,'Lib','ldap','__init__.py'])
f = open(package_init_file_name,'r')
s = f.readline()
while s:
	s = string.strip(s)
	if s[0:11]=='__version__':
		version = eval(string.split(s,'=')[1])
		break
	s = f.readline()
f.close()

#-- A class describing the features and requirements of OpenLDAP 2.0
class OpenLDAP2:
	library_dirs = []
	include_dirs = []
	extra_compile_args = []
	extra_link_args = []
	extra_objects = []
	libs = ['ldap', 'lber']
	defines = [ ]
	extra_files = []

LDAP_CLASS = OpenLDAP2

#-- Read the [_ldap] section of setup.cfg
cfg = ConfigParser()
cfg.read('setup.cfg')
if cfg.has_section('_ldap'):
	for name in dir(LDAP_CLASS):
		if cfg.has_option('_ldap', name):
			print name + ': ' + cfg.get('_ldap', name)
			setattr(LDAP_CLASS, name, string.split(cfg.get('_ldap', name)))

for i in range(len(LDAP_CLASS.defines)):
	LDAP_CLASS.defines[i]=((LDAP_CLASS.defines[i],None))

for i in range(len(LDAP_CLASS.extra_files)):
	destdir, origfiles = string.split(LDAP_CLASS.extra_files[i], ':')
	origfileslist = string.split(origfiles, ',')
	LDAP_CLASS.extra_files[i]=(destdir, origfileslist)

#-- Let distutils/setuptools do the rest
name = 'python-ldap'

# Python 2.3.6+ and setuptools are needed to build eggs, so
# let's handle setuptools' additional  keyword arguments to
# setup() in a fashion that doesn't break compatibility  to
# distutils. This still allows 'normal' builds where either
# Python > 2.3.5 or setuptools (or both ;o) are not available.
kwargs = dict()
if has_setuptools:
	kwargs = dict(
			include_package_data = True,
			install_requires = ['setuptools'],
			zip_safe = False)

setup(
	#-- Package description
	name = name,
	version = version,
	description = 'Various LDAP-related Python modules',
	author = 'David Leonard, Michael Stroeder, et al.',
	author_email = 'python-ldap-dev@lists.sourceforge.net',
	url = 'http://www.python-ldap.org/',
	#-- C extension modules
	ext_modules = [
		Extension(
		'_ldap',
		[
			'Modules/LDAPObject.c',
			'Modules/ldapcontrol.c',
			'Modules/common.c',
			'Modules/constants.c',
			'Modules/errors.c',
			'Modules/functions.c',
			'Modules/schema.c',
			'Modules/ldapmodule.c',
			'Modules/message.c',
			'Modules/version.c',
			'Modules/options.c',
			'Modules/berval.c',
		],
		libraries = LDAP_CLASS.libs,
		include_dirs = ['Modules'] + LDAP_CLASS.include_dirs,
		library_dirs = LDAP_CLASS.library_dirs,
		extra_compile_args = LDAP_CLASS.extra_compile_args,
		extra_link_args = LDAP_CLASS.extra_link_args,
		extra_objects = LDAP_CLASS.extra_objects,
		runtime_library_dirs = (not sys.platform.startswith("win"))*LDAP_CLASS.library_dirs,
		define_macros = LDAP_CLASS.defines + \
			('ldap_r' in LDAP_CLASS.libs or 'oldap_r' in LDAP_CLASS.libs)*[('HAVE_LIBLDAP_R',None)] + \
			('sasl' in LDAP_CLASS.libs or 'sasl2' in LDAP_CLASS.libs or 'libsasl' in LDAP_CLASS.libs)*[('HAVE_SASL',None)] + \
			('ssl' in LDAP_CLASS.libs and 'crypto' in LDAP_CLASS.libs)*[('HAVE_TLS',None)] + \
			[('LDAPMODULE_VERSION', version)]
		),
	],
	#-- Python "stand alone" modules 
	py_modules = [
		'ldapurl',
		'ldif',
		'dsml',
  		'ldap',
  		'ldap.async',
  		'ldap.controls',
  		'ldap.cidict',
  		'ldap.dn',
  		'ldap.filter',
  		'ldap.functions',
  		'ldap.ldapobject',
  		'ldap.modlist',
  		'ldap.resiter',
  		'ldap.sasl',
  		'ldap.schema',
  		'ldap.schema.models',
  		'ldap.schema.subentry',
  		'ldap.schema.tokenizer',
	],
	package_dir = {'': 'Lib',},
	data_files = LDAP_CLASS.extra_files,
	**kwargs
)
