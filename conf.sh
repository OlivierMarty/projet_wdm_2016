#!/bin/bash

# xquery processor
function xquery {
  java -cp saxon.jar:tagsoup-1.2.jar net.sf.saxon.Query $@ \!indent=yes
}
function xquery_html {
  java -cp saxon.jar:tagsoup-1.2.jar net.sf.saxon.Query -x:org.ccil.cowan.tagsoup.Parser $@ \!indent=yes
}
