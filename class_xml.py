import urllib.request
from bs4 import BeautifulSoup
from subprocess import run, PIPE

class XML:
  def __init__(self, **kwargs):
    """Provide either parameter str= or url=
    Optional parameters : lang=xml,html,json
    """

    # fetch data
    if 'str' in kwargs:
      source = kwargs['str']
    elif 'url' in kwargs:
      source = urllib.request.urlopen(kwargs['url']).read()
    else:
      raise ValueError('XML : either str or url must be provided')

    # parse data
    lang = kwargs.get('lang', 'xml')
    if lang == "xml":
      parser = "lxml-xml"
    elif lang == "html":
      parser = "lxml"
    else:
      raise NotImplementedError('lang != xml & lang != html') # TODO json
    self.data = BeautifulSoup(source, parser)

  def xquery(self, query):
    """A binding with Saxon (at least for the moment)
    returns a XML object containing all results embedded in a <xquery> root
    """
    process = run(["java", "-cp", "saxon.jar:tagsoup-1.2.jar",
      "net.sf.saxon.Query", "!omit-xml-declaration=yes", "-qs:" + query, "-s:-"],
      stdout=PIPE, input=str(self.data).encode(), check=True)
    return XML(str=b"<xquery>" + process.stdout + b"</xquery>")
 
  def __str__(self):
    return self.data.prettify()


#print(str(XML(str="<a>te<i>sa<i>l</i>ut</i>t</a>").xquery("//*:i")))

