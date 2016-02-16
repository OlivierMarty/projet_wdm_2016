#!/usr/bin/env python2

from json2xml.json2xml import Json2xml

print '<?xml version="1.0" encoding="UTF-8"?>'
print "<json>"
print Json2xml.fromjsonfile('/dev/stdin').json2xml()
print "</json>"
