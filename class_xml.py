import urllib.request
from bs4 import BeautifulSoup
from subprocess import run, PIPE
import dicttoxml
import json

class XML:
  def __init__(self, **kwargs):
    """Provide one of the following parameters
      str=<a>...</a>
      url=http:// or file://
      data=BeautifulSoup object
    Optional parameters : lang=xml,html,json
    """

    # fetch data
    if 'data' in kwargs:
      self.data = kwargs['data']
    else:
      if 'str' in kwargs:
        source = kwargs['str']
      elif 'url' in kwargs:
        source = urllib.request.urlopen(kwargs['url']).read()
      else:
        raise ValueError('XML : either str, url, or data must be provided')

      # parse data
      lang = kwargs.get('lang', 'xml')
      if lang == 'json':
        source = dicttoxml.dicttoxml(json.loads(source.decode()), attr_type=False, custom_root='json')
        parser = "lxml-xml"
      elif lang == "xml":
        parser = "lxml-xml"
      elif lang == "html":
        parser = "lxml"
      else:
        raise NotImplementedError('lang='+lang+" not supported")
      self.data = BeautifulSoup(source, parser)

  def xquery(self, query):
    """A binding with Saxon (at least for the moment)
    returns a list of XML objects
    """
    process = run(["java", "-cp", "saxon.jar:tagsoup-1.2.jar",
      "net.sf.saxon.Query", "!omit-xml-declaration=yes", "-qs:" + query, "-s:-"],
      stdout=PIPE, input=str(self.data).encode(), check=True)
    return [XML(data=obj) for obj in XML(str=b"<xquery>" + process.stdout + b"</xquery>").data.xquery.children]
 
  def __str__(self):
    return self.data.prettify()

