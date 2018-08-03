(function (window) {
	'use strict';

	// Your starting point. Enjoy the ride!

	$('.todo-list').on('click','.task_update', function(){
		console.log($(this).val());
		$(this).parents('li').addClass('temp');
		$.ajax({
			'type': 'POST',
			'url': '/ajax/task_update',
			'data': {id: $(this).val()},
			success: function(res){
				if(res.status.status == 'view'){
					$('.temp').removeClass("completed temp").addClass('view')
				}
				if(res.status.status == 'completed'){
					$('.temp').removeClass("view temp").addClass('completed')
				}
					
				console.log(res.status.status)
			},
			error: function(err){
				console.log(err)
			}
		});
	});

})(window);
