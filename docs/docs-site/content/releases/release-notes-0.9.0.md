---
title: "0.9.0"
date: 2019-03-13T18:28:08-07:00
draft: false
weight: -90
tags: ['skipIndexing']
---

### Hue v0.9.0, released June 29, 2010


Hue 0.9 is the first open source release of Hue, previously known as
Cloudera Desktop.  The UI look and feel has greatly improved across different
supported browsers (Firefox, Safari, Chrome and IE8).  Hue has also made it
much easier to write, build, distribute and install an SDK application.


KNOWN BUGS

- After a successful upload with Linux's flash player (which may warn you about
  hanging your computer), the upload screen does not clear. Click the red (x)
  button to clear it.

- Running on Internet Explorer 8 has a memory leak issue, which can cause
  instability with prolonged use.

- FileBrowser upload does not work well with big files (larger than 200MB).
