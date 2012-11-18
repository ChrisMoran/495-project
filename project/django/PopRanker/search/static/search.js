function goodVote(elem, query, link) {
    $.post('/vote/', {
	'query' : query,
	'url' : link,
	'vote' : 1
    });
    elem.parent().html("Thank you for voting!");
}

function badVote(elem, query, link) {
    $.post('/vote/', {
	'query' : query,
	'url' : link,
	'vote' : 0
    });
    elem.parent().html("Thank you for voting!");
} 

function handleAjax() {
	
	$.get("searchajax", { query: "harry potter" },
		   function(data){
			 alert("Data Loaded: " + data);
		   });

}
