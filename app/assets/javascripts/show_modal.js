function activatePhotoBtns(){
	$('.photo-div').hover(function(){
		$(this).find('.photo-btns').show(100);
		$(this).find('.photo-top-btns').show(100);
	}, function(){
		$(this).find('.photo-btns').hide(100);
		$(this).find('.photo-top-btns').hide(100);
	});

	$('.delete-btn').click(function(e){
		e.stopPropagation();
		var id = $(this).attr('data-id');
		$.ajax({
			url:'/delete_photo/'+id,
			type:'post',
			success:function(data){
				$('#'+id+'-photo-div').remove();
			}
		});
	});
	$('.request-btn').click(function(e){
		e.stopPropagation();
		var id = $(this).attr('data-id');
		$.ajax({
			url:'/request_photo/'+id,
			type:'post',
			success:function(data){
				console.log('here');
				$('#'+id+'-photo-div').toggleClass('selected');
			}
		});
	});
}
function showModalPhoto(photo){
	if(photo.is_photo){
		var img = $('<img id = "modal-photo" src = "'+photo.compressed_path+'"></img>');
		$('#modal-title-link').attr('href', photo.compressed_path);
		$('#modal-title-link').text(photo.compressed_path);
		$('#modal-body').html(photo);
	}	
	else{

	}
}

function activateShowModal(){
	$('.photo-div').click(function(){

		$.ajax({
			url:'/photos/show/'+$(this).attr('data-id'),
			type:'get',
			success:function(data){
				console.log(data);
				$('#modal-body').html(data);
				$('#show-modal').modal('show');
			}
		});
		// if($(this).attr('data-type') == 'false'){
		// 	//video
		// 	showModalVideo($(this).attr('data-id'));
		// 	src = $(this).attr('data-redirect')
		// 	var vid = $('<video src="'+src+'" controls></video>');
		// 	$(vid).attr('id', 'modal-photo');
		// 	$('#modal-body').html(vid);
		// 	$('#show-modal').modal('show');
		// 	$('#modal-title-link').attr('href', src);
		// 	$('#modal-title-link').text(src);
		// 	$('#cut-link').attr('href', '/cut_video?id='+$(this).attr('data-id'));
		// }else{
		// 	showModalPhoto($(this).attr('data-id'));
		// 	// src = $(this).attr('data-redirect')
		// 	// var photo = $('<img src="'+src+'"></img>');
		// 	// $('#modal-title-link').attr('href', src);
		// 	// $('#modal-title-link').text(src);
		// 	// $(photo).attr('id', 'modal-photo');
		// 	$('#modal-body').html(photo);
		// 	$('#show-modal').modal('show');
		// }
	});
}

$(document).ready(function(){
	activatePhotoBtns();
	activateShowModal();
})