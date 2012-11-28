$(document).ready(function() {

  $("#querybox").val(getParameter("query"));

});

/* From StackOverflow
 *
 * Takes in the name of a parameter and parses the URL
 * returning the value associated with that parameter
 */
function getParameter(paramName) {
  var searchString = window.location.search.substring(1),
      i, val, params = searchString.split("&");

  for (i=0;i<params.length;i++) {
    val = params[i].split("=");
    if (val[0] == paramName) {
      return decodeURIComponent(val[1].replace(/\+/g," "));
    }
  }

  return null;

}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    crossDomain : false,
    beforeSend : function(xhr, settings) {
	xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    }
});

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
