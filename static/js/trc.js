$(document).ready(function() {
	// search and show/hide terms in a list
	$("#listsrc").on('keyup',function(){
		let val=$(this).val().toLowerCase().trim();
		let items=$('.item');
		items.removeClass('hidden');
		if(val!=='') { items.not('[data-content*="' + val + '"]').addClass('hidden'); }
		// update panel counts
		let sections = $(".sections")
		sections.each(function() {
			let section = $(this);
			section.removeClass('hidden');
			let cnt = section.find(".list-group > a").not('.hidden').length;
			let sort = section.find(".accordion-header").attr('data-sort');
			section.find(".accordion-header > button > strong").text(sort + ' (' + cnt + ')');
			if(cnt===0) { section.addClass('hidden'); }
		});
	});
	$("#related").on('change',function(){
		let path=$(this).val();
		window.location.replace(path);
		return false;
	});
});
