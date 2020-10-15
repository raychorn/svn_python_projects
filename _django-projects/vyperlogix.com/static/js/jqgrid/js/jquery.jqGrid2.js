// we make it simple as possible
function jqGridInclude()
{
    var pathtojsfiles = "js/"; // need to be ajusted
    // if you do not want some module to be included
    // set include to false.
    // by default all modules are included.
    var minver = false;
    var modules = [
        { include: true, incfile:'grid.locale-en.js',minfile: 'min/grid.locale-en-min.js'}, // jqGrid translation
        { include: true, incfile:'grid.base.js',minfile: 'min/grid.base-min.js'}, // jqGrid base
        { include: false, incfile:'grid.common.js',minfile: 'min/grid.inlinedit-min.js' }, // jqGrid common for editing
        { include: false, incfile:'grid.formedit.js',minfile: 'min/grid.formedit-min.js' }, // jqGrid Form editing
        { include: false, incfile:'grid.inlinedit.js',minfile: 'min/grid.inlinedit-min.js' }, // jqGrid inline editing
        { include: false, incfile:'grid.celledit.js',minfile: 'min/grid.inlinedit-min.js' }, // jqGrid cell editing
        { include: false, incfile:'grid.subgrid.js',minfile: 'min/grid.subgrid-min.js'}, //jqGrid subgrid
        { include: false, incfile:'grid.treegrid.js',minfile: 'min/grid.subgrid-min.js'}, //jqGrid treegrid
        { include: false, incfile:'grid.custom.js',minfile: 'min/grid.custom-min.js'}, //jqGrid custom 
        { include: false, incfile:'grid.postext.js',minfile: 'min/grid.postext-min.js'}, //jqGrid postext
        { include: false, incfile:'grid.tbltogrid.js',minfile: 'min/grid.tbltogrid-min.js'}, //jqGrid custom 
        { include: false, incfile:'grid.setcolumns.js',minfile: 'min/grid.setcolumns-min.js'} //jqGrid postext
    ];
    var filename;
    for(var i=0;i<modules.length; i++)
    {
        if(modules[i].include === true) {
        	if (minver !== true) {
        		filename = pathtojsfiles+modules[i].incfile;
        	} else {
        		filename = pathtojsfiles+modules[i].minfile;
        	}
       		//try { IncludeJavaScript(filename); } catch(e) { alert(e)};
       		$.ajax({url:filename,async:false,dataType: 'script', cache: true});
        }
    }
    function IncludeJavaScript(jsFile)
    {   	
        var oHead = document.getElementsByTagName('head')[0];
        var oScript = document.createElement('script');
        oScript.type = 'text/javascript';
        oScript.encoding = 'UTF-8';
        oScript.src = jsFile;
        oHead.appendChild(oScript);        
    }
};
jqGridInclude();