from django.template import Context, loader

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

def head(url):
    toks = url.split('/')
    url = '/'.join(toks[0:-1 if (toks[-1] == '') else len(toks)])
    html='''
<link href="{{ url }}/css/flexigrid/flexigrid.css" rel="stylesheet" type="text/css" />
<script src="{{ url }}/lib/jquery/jquery.js" type="text/javascript"></script>
<script src="{{ url }}/flexigrid.pack.js" type="text/javascript"></script>
    '''
    tplate = loader.get_template_from_string(html)
    content = tplate.render(Context({'url': url}))
    return content

def head_list(url):
    return [item for item in head(url).split('\n') if (len(item.strip()) > 0)]

def script_content(name,width=700):
    '''
    name is the name of the DOM object
    width is usually something like 700
    '''
    from vyperlogix import misc
    width = 700 if (not str(width).isdigit()) else width
    name = 'table_grid' if (not misc.isString(name)) else name
    t = '''<table id="{{ name }}" width="{{ width }}" align="left"></table>'''
    tplate = loader.get_template_from_string(t)
    content = tplate.render(Context({'name': name, 'width': width}))
    return content

def script_head(name,url,title,colModel,searchitems,sortname,sortorder,dataType='json',usepager=True,useRp=True,rp=10,showTableToggleBtn=False,width=700,height=450):
    '''
    name is the name of the DOM object
    url is something like http://127.0.0.1:8888/grid/
    dataType is something like json
    colModel is something like this:
      {display: 'ISO', name : 'iso', width : 40, sortable : true, align: 'left'},
      {display: 'Name', name : 'name', width : 180, sortable : true, align: 'left'},
      {display: 'Printable Name', name : 'printable_name', width : 120, sortable : true, align: 'left'},
      {display: 'ISO3', name : 'iso3', width : 130, sortable : true, align: 'left', hide: true},
      {display: 'Numcode', name : 'numcode', width : 120, sortable : true, align: 'left'},
    searchitems is something like this:
      {display: 'Name', name : 'name'},
      {display: 'ISO', name : 'iso'}
    sortorder is either asc or desc
    usepager is either True or False as a bool
    title is something that makes sense as a title
    useRp is either True or False as a bool
    rp is a number of items per page
    showTableToggleBtn is either True of False as a bool
    width is usually something like 700
    height is usually something like 500
    '''
    from vyperlogix import misc
    name = 'table_grid' if (not misc.isString(name)) else name
    sortorder = 'asc' if (sortorder not in ['asc','desc']) else sortorder
    usepager = 'true' if (usepager not in ['true','false']) else usepager
    useRp = 'true' if (useRp not in ['true','false']) else useRp
    rp = 15 if (not str(rp).isdigit()) else rp
    showTableToggleBtn = 'true' if (sortorder not in ['true','false']) else showTableToggleBtn
    width = 700 if (not str(width).isdigit()) else width
    height = 450 if (not str(height).isdigit()) else height
    js = '''
<script type="text/javascript">
  $("#{{ name }}").flexigrid
    (
    {
    url: '{{ url }}',
    dataType: '{{ dataType }}',
    colModel : [ {{ colModel }} ],
    searchitems : [ {{ searchitems }} ],
    sortname: "{{ sortname }}",
    sortorder: "{{ sortorder }}",
    usepager: {{ usepager }},
    title: '{{ title }}',
    useRp: {{ useRp }},
    rp: {{ rp }},
    showTableToggleBtn: {{ showTableToggleBtn }},
    width: {{ width }},
    height: {{ height }}
    }
  );
</script>
    '''
    tplate = loader.get_template_from_string(js)
    content = tplate.render(Context({'name': name, 'url': url, 'dataType': dataType, 'colModel': colModel, 'searchitems':searchitems, 'sortname':sortname, 'sortorder':sortorder, 'usepager':usepager, 'title':title, 'useRp':useRp, 'rp':rp, 'showTableToggleBtn': showTableToggleBtn, 'width': width, 'height': height}))
    return content

def script(name,url,title,colModel,searchitems,sortname,sortorder,dataType='json',usepager=True,useRp=True,rp=10,showTableToggleBtn=False,width=700,height=450):
    '''
    name is the name of the DOM object
    url is something like http://127.0.0.1:8888/grid/
    dataType is something like json
    colModel is something like this:
      {display: 'ISO', name : 'iso', width : 40, sortable : true, align: 'left'},
      {display: 'Name', name : 'name', width : 180, sortable : true, align: 'left'},
      {display: 'Printable Name', name : 'printable_name', width : 120, sortable : true, align: 'left'},
      {display: 'ISO3', name : 'iso3', width : 130, sortable : true, align: 'left', hide: true},
      {display: 'Numcode', name : 'numcode', width : 120, sortable : true, align: 'left'},
    searchitems is something like this:
      {display: 'Name', name : 'name'},
      {display: 'ISO', name : 'iso'}
    sortorder is either asc or desc
    usepager is either True or False as a bool
    title is something that makes sense as a title
    useRp is either True or False as a bool
    rp is a number of items per page
    showTableToggleBtn is either True of False as a bool
    width is usually something like 700
    height is usually something like 500
    '''
    js = '''
{{ SCRIPT_CONTENT }}
{{ SCRIPT_HEAD }}
    '''
    tplate = loader.get_template_from_string(js)
    content = tplate.render(Context({'name': name, 'url': url, 'dataType': dataType, 'colModel': colModel, 'searchitems':searchitems, 'sortname':sortname, 'sortorder':sortorder, 'usepager':usepager, 'title':title, 'useRp':useRp, 'rp':rp, 'showTableToggleBtn': showTableToggleBtn, 'width': width, 'height': height, 'SCRIPT_CONTENT':script_content(name,width=width), 'SCRIPT_HEAD':script_head(name,url,title,colModel,searchitems,sortname,sortorder,dataType=dataType,usepager=usepager,useRp=useRp,rp=rp,showTableToggleBtn=showTableToggleBtn,width=width,height=height)}))
    return ''.join(content.split('\n'))
