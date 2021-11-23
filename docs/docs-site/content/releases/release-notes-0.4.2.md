---
title: "0.4.2"
date: 2019-03-13T18:28:08-07:00
draft: false
weight: -42
tags: ['skipIndexing']
---

### Cloudera Desktop v0.4.2, released May 21, 2010

Besides the list of key enhancements and bug fixes below, the most important
changes to highlight are:

* Internet Explorer 8 support.
* User groups and group-based permissions.
* Many new features and usability improvement for Beeswax.


ENHANCEMENTS

- Compatibility:

  * Basic support for Internet Explorer 8. Support for Chrome and Safari.

  * Support Python 2.6.

  * Support Ubuntu 10.04 (Lucid).

- Desktop Administration:

  * Support for using MySQL as the Django database.

  * Automatic log rotation.

- User Management:

  * Added group support. You can assign users to groups, and grant (or deny)
    access to use any Cloudera Desktop application based on group.

  * A new user access log.

  * The superuser may view the recent accesses of all users grouped by
    applications.

- Beeswax:

  * You can save a query with parameters, which will prompt for inputs when
    executed.

  * When creating new Hive tables for existing data files, the new import
    wizard can help defining the table columns by reading your data, as
    well as loading the data into the new table.

  * You can save the temporary results of a query as a new table, or simply as
    files in HDFS.

- The Cloudera Desktop SDK:

  * The ability to create a URL link to a specific view of an individual
    application. Various email notifications use this to link to their result
    pages.

- UI speed improvement.


KEY BUG FIXES

- Handle large number of Data Nodes.

- File upload under HTTPS now works.

- Job Browser filters by job status correctly.


KNOWN BUGS

- After a successful upload with Linux's flash player (which may warn you about
  hanging your computer), the upload screen does not clear. Click the red (x)
  button to clear it.

- Running on Internet Explorer 8 has a memory leak issue, which can cause
  instability with prolonged use.
