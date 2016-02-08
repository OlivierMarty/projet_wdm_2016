#!/bin/bash

# xquery processor
xquery="java -cp saxon.jar:tagsoup-1.2.jar net.sf.saxon.Query"
xquery_html="java -cp saxon.jar:tagsoup-1.2.jar net.sf.saxon.Query -x:org.ccil.cowan.tagsoup.Parser"
