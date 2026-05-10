$(document).ready(function() {
	// search and show/hide terms in a list
	$("#listsrc").on('keyup',function(){
		let val=$(this).val().toLowerCase().trim();
		let items=$('.item');
		items.removeClass('notseen');
		if(val!=='') { items.not('[data-content*="' + val + '"]').addClass('notseen'); }
		// update accordian panel counts
		let sections = $(".sections")
		sections.each(function() {
			let section = $(this);
			let cnt = section.find(".list-group > a").not('.notseen').length;
			section.find(".cnt").text(cnt);
		});
	});
	$("#related").on('change',function(){
		let path=$(this).val();
		window.location.replace(path);
		return false;
	});
});
