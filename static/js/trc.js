$(document).ready(function() {
	// search and show/hide terms in a list
	$("#listsrc").on('keyup',function(){
		let val=$(this).val().toLowerCase().trim();
		let items=$('.item');
		items.parent().show();
		if(val!=='') { items.not('[data-content*="' + val + '"]').hide(); }
		// update panel counts
		let sections = $(".sections")
		sections.each(function() {
			let section = $(this);
			section.show();
			let cnt = section.find(".list-group > a").is(':visible').length;
			let sort = section.find(".accordion-header").attr('data-sort');
			section.find(".accordion-header > button > strong").text(sort + ' (' + cnt + ')');
			if(cnt===0) { section.hide(); }
		});
	});
});
