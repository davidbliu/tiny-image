$(document).ready(function(){
	$('#hash-log-btn').click(function(){
		console.log('btn clicked');
		$.ajax({
			url:'/get_hash_log',
			type:'get',
			success:function(data){
				alert(data);
			}
		});
	});

	$('#run-compressor-btn').click(function(){
		console.log('laskjfdlksjlfjlfsdkjlsjfkldj')
		$.ajax({
			url:'/run_compressor',
			type:'POST',
			success:function(data){
				console.log('running compressor');
			}
		})
	})
});
console.log('alskdfjsl');