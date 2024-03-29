Welcome to the repository for Hue
=================================

.. note::
    This is the development-oriented readme. If you want to write notes for
    end users, please put them in ``dist/README``.

Hue is both a web UI for Hadoop and a framework to create interactive web
applications.  It features a FileBrowser for accessing HDFS, JobSub and
JobBrowser applications for submitting and viewing MapReduce jobs, a Beeswax
application for interacting with Hive.  On top of that, the web frontend
is mostly built from declarative widgets that require no JavaScript and are
easy to learn.


File Layout
===========
The "core" stuff is in ``desktop/core/``, whereas installable apps live in
``apps/``.  Please place third-party dependencies in the app's ext-py/
directory.

The typical directory structure for inside an application includes:

  src/
    for Python code

  conf/
    for configuration (``.ini``) files to be installed

  static/
    for static HTML and js resources

  templates/
    for data to be put through a template engine

  docs/
    for helpful notes

The python code is structured simply as
``module/package.py``,
where module may be "filebrowser" or "jobsub".  Because it is unlikely that
there are going to be huge conflicts, we're going without a deep nested
hierarchy.


URL Layout
==========
``core/src/desktop/urls.py`` contains the current layout for top-level URLs.
For the URLs within your application, you should make your own ``urls.py``
which will be automatically rooted at ``/yourappname/`` in the global
namespace.  See ``apps/hello/src/hello/urls.py`` for an example.


Development Prerequisites
===========================
1. On your host system, you need to have the python "virtualenv" package
   installed.

2. Also, you'll need these library development packages installed on your
   system:

    Debian:
      * gcc
      * libldap2-dev
      * libmysqlclient-dev
      * libsasl2-dev
      * libsqlite3-dev
      * libssl-dev
      * libxml2-dev
      * libxslt-dev
      * python-dev
      * python-setuptools

    CentOS:
      * cyrus-sasl-devel
      * gcc
      * libxml2-devel
      * libxslt-devel
      * mysql
      * mysql-devel
      * openldap-devel
      * openssl
      * python-devel
      * python-setuptools
      * sqlite-devel
      * python-simplejson (for the crepo tool)

    MacOS (mac port):
      * liblxml
      * libxml2
      * libxslt
      * mysql5-devel
      * simplejson (easy_install)
      * sqlite3

3. You need to have crepo installed, and preferably on your path. If it is not
   on your path, set the environment variable ``CREPO`` to point to ``crepo.py``
   from that distribution. You can clone crepo from
   http://github.com/cloudera/crepo.git somewhere else on your system.


Getting Started
===============
To build and get the core server running (without any helper daemons)::

    $ export HADOOP_HOME=<path-to-hadoop-home>
    $ git clone http://github.com/cloudera/hue.git
    $ cd hue
    $ make apps
    $ build/env/bin/desktop runserver_plus

Now Hue should be running on http://localhost:8000.


Setting up Hadoop
=================
In order to start up a pseudodistributed cluster with the plugins enabled,
run::

    $ ./tools/scripts/configure-hadoop.sh all

After doing so, running ``jps`` should show all the daemons running (NN, JT,
TT, DN) and you should be able to see the web UI on http://localhost:50030/ and
http://localhost:50070/.


FAQ
===
1: What does "Exception: no app!" mean?
    Your template has an error in it.  Check for messages from the server that
    look like::

        INFO:root:Processing exception: Unclosed tag 'if'. Looking for one of: else, endif

2: What do I do if I get "There was an error launching ..."?
    Turn on debugging by issuing ``dbug.cookie()`` in a Firebug console.


Django Conventions
==================
If you need to name your urls
(http://docs.djangoproject.com/en/dev/topics/http/urls/#naming-url-patterns)
because there's ambiguity in the view, be sure to prefix the name
with the application name.  The url name namespace is global.  So
``jobsub.list`` is fine, but ``list`` is not.

Hue is using Django 1.1, which supports the notion of URL namespaces:
http://docs.djangoproject.com/en/dev/topics/http/urls/#url-namespaces.
We have yet to move over our URLs to this construct. Brownie points for the
developer who takes this on.


Using and Installing Thrift
===========================
Right now, we check in the generated thrift code.
To generate the code, you'll need the thrift binary.
Compile it like so::

    $ git clone http://github.com/dreiss/thrift.git
    $ cd thrift
    $ ./bootstrap.sh
    $ ./configure --with-py=no --with-java=no --with-perl=no --prefix=$HOME/pub

We exclude python, java, and perl because they don't like
to install in prefix.  If you look around at configure's --help,
there are environment variables that determine where those
runtime bindings are installed.
::

    $ make && make install

When preparing ``.thrift`` files, you can use she-bangs to generate
the python bindings like so::

    #!/usr/bin/env thrift -r --gen py:new_style -o ../../../

.. note::
    This file is in reStructuredText. You may run
    ``rst2html README.rst > README.html`` to produce a HTML.
