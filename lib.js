
/* <script id="searcher" data-search="bananas" src="lib.js?search=bananas"></script> */

// $.ajax({
//     dataType(returnType) method(functionType) url(functionName) contentType(paramType) data(params)

//     dataType: xml, html, script, json, jsonp, text
//     method: GET, POST
//     url: test.php, test.html, test.js ? search = value,
//     contentType: application/x-www-form-urlencoded, multipart/form-data
//     data: {search: value}

//   })  .done(function() {
//     alert( "success" );
//   })
//   .fail(function() {
//     alert( "error" );
//   })
//   .always(function() {
//     alert( "complete" );
//   });
var script_tag = document.getElementById('searcher')
var search_term = script_tag.getAttribute("data-search");
var query = script_tag.src.replace(/^[^\?]+\??/,''); 
 var vars = query.split("&");
 var args = {};
 for (var i=0; i<vars.length; i++) {
     var pair = vars[i].split("=");
     args[pair[0]] = decodeURI(pair[1]).replace(/\+/g, ' ');   
 }
var search_term = args['search'];
