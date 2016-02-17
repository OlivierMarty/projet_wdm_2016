import urllib.request
import xml.etree.cElementTree as ET
from subprocess import run, PIPE

class XML:
  def __init__(self, **kwargs):
    """Provide either parameter str= or url=
    Optional parameters : lang=xml,html,json
    """

    # language : xml, html, or json
    lang = kwargs.get('lang', 'xml')
    if lang != 'xml':
      raise NotImplementedError('lang!=xml') # TODO html, json

    # fetch data
    if 'str' in kwargs:
      source = kwargs['str']
    elif 'url' in kwargs:
      source = urllib.request.urlopen(kwargs['url']).read()
    else:
      raise ValueError('XML : either str or url must be provided')

    # parse data
    self.data = ET.fromstring(source)

  def xquery(self, query):
    """A binding with Saxon (at least for the moment)
    returns a XML object containing all results embedded in a <xquery> root
    """
    process = run(["java", "-cp", "saxon.jar:tagsoup-1.2.jar",
      "net.sf.saxon.Query", "!omit-xml-declaration=yes", "-qs:" + query, "-s:-"],
      stdout=PIPE, input=ET.tostring(self.data), check=True)
    return XML(str=b"<xquery>" + process.stdout + b"</xquery>")
 
  def __str__(self):
    return ET.tostring(self.data).decode()



#print(str(XML(str="<a>te<i>sa<i>l</i>ut</i>t</a>").xquery("//*:i")))

