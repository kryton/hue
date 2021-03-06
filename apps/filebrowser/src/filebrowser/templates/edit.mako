## Licensed to Cloudera, Inc. under one
## or more contributor license agreements.  See the NOTICE file
## distributed with this work for additional information
## regarding copyright ownership.  Cloudera, Inc. licenses this file
## to you under the Apache License, Version 2.0 (the
## "License"); you may not use this file except in compliance
## with the License.  You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
<%namespace name="edit" file="editor_components.mako" />
<%!
  from django.template.defaultfilters import urlencode
  from filebrowser.views import truncate
%>
<%
  path_enc = urlencode(path)
  dirname_enc = urlencode(dirname)
%>
<html>
<head><title>${truncate(filename)} :: File Editor</title></head>
<body>
<div class="toolbar">
  <div class="fe-path">${truncate(path, 91)}</div>
  <div class="fe-buttons ccs-button_bar">
    <a class="fe-viewLocation ccs-art_button" data-icon-styles="{'width': 16, 'height': 16}" href="${url('filebrowser.views.view', path=dirname_enc)}" target="FileBrowser">View Location</a>
  </div>
</div>
% if form.errors:
  <div class="alert_popup">
    % for field in form:
      % if len(field.errors):
       ${str(field.errors) | n}
      % endif
    % endfor
  </div>
% endif
<form class="no_overflow fe-editForm" method="post" action="${url('filebrowser.views.save_file')}">
    ${edit.render_field(form["path"],hidden=True, notitle=True)}
    <h2 class="ccs-hidden">${form["contents"].label_tag() | n}</h2>
    <div class="fe-divResize">${str(form["contents"]) | n}</div>
    <input class="ccs-hidden" type="submit" name="save" value="saveAs">
    <input class="ccs-hidden" type="submit" name="save" value="save">
</form>
</body>
</html>

