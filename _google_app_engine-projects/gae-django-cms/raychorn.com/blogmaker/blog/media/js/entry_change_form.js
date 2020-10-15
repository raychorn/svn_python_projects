// Copyright (c) 2006-2007, PreFab Software Inc.


$(document).ready(function(){
  // Get the entry ID from the URL
  // Note: The Add form doesn't have an entry ID
  var entryId = null;
  try {
    entryId = Number(document.location.href.match(/\/(\d+)\/$/)[1]);
	} catch (e) {}
	
	// Make the char fields longer
  $('input.vTextField').attr('size', '60');
    
  // Add links to the public entry and postTrackbacks page before the delete button
  $('a.deletelink')
    .before('<a href="/blogmaker/' + entryId + '/">View on site</a>&nbsp;&nbsp;&nbsp;&nbsp;')
    .before('<a href="/blogmaker/' + entryId + '/postTrackbacks">View trackbacks</a>&nbsp;&nbsp;&nbsp;&nbsp;');
});