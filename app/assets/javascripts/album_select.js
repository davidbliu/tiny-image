function activateAlbumSelect(){
	$('#album-select').change(function(){
		selected = $("#album-select option:selected").text();
		if(selected == 'All Albums'){
			url = addParameter(window.location.href, 'album', 'all');
			url = removeURLParameter(url, 'page');
			window.location = url;
		}
		else{
			url = addParameter(window.location.href, 'album', selected);
			url = removeURLParameter(url, 'page');
			window.location = url;
		}
	});
}

function insertParam(key, value)
{
	key = encodeURI(key); value = encodeURI(value);
	var kvp = document.location.search.substr(1).split('&');
	var i=kvp.length; var x; while(i--) 
	{
		x = kvp[i].split('=');
		if (x[0]==key)
		{
			x[1] = value;
			kvp[i] = x.join('=');
			break;
		}
	}
	if(i<0) {kvp[kvp.length] = [key,value].join('=');}
	document.location.search = kvp.join('&'); 
}

$(document).ready(function(){
	activateAlbumSelect();
});