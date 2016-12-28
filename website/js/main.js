var ROOT = "http://vaspberry.duckdns.org:3000/"
var LIMIT = 10;


function isColorHex(h) {
	var a = parseInt(h,16);
	return (a.toString(16) === h.toLowerCase() && h.length == 6);
}

function loadHash(){
	var hash = window.location.hash;

	if(hash && hash != '#all' && isColorHex(hash.split("#")[1])){
		$('.message').hide();
		$('.message').filter('[data-color="'+hash+'"]').show();
	}else if(hash == '#all'){
		$('.message').show();
	}else {
		window.location.hash = "#all";
		
	}
}

function messageURL(page){
	return encodeURI(ROOT + "messages?_sort=date_sent&_order=DESC&_page=" + page + "&_limit=" + LIMIT);
}

function load(url, responseType) {
	return new Promise(function(resolve, reject){
	    var xhr = new XMLHttpRequest();
	    xhr.open('GET', url);
	    xhr.responseType = responseType;
	    xhr.onload = function() {
	      if(xhr.status == 200){
	          resolve(this);
	      }else{
	          reject(Error(xhr.statusText));
	      }
	    };
	    // Handle network errors
	    xhr.onerror = function() {
	      reject(Error("Network Error"));
	    };

	    xhr.send();
	}); 
}

function loadMessagePage(page) {
	return load(messageURL(page), 'json')
}

function loadAllMessages(){
	var currentPage = 1;
	loadMessagePage(currentPage)
    .then(function(response){
    	addToPage(response.response);
    	
    	var numPagesLeft = Math.ceil((response.getResponseHeader("X-Total-Count") - LIMIT)/LIMIT);
    	var pageNums = [];
    	while(numPagesLeft--){
    		pageNums.push(++currentPage);
    	}
    	
    	return pageNums.map(loadMessagePage).reduce(function(sequence, messagePromise) {
    		return messagePromise.then(function(){
    			return messagePromise;
    		})
    		.then(function(response){
    			addToPage(response.response);
    		});

    	}, Promise.resolve());

    }).then(function(){
    	console.log("Finished loading messages.");
    	loadHash();
    	window.onhashchange = loadHash;
    }).catch(function(err){
        console.log("Error: " + err);
    });


}

function addToPage(messages){
	for(messageIndex in messages){
		var message = messages[messageIndex];
		var date = dateFormat(new Date(0).setUTCSeconds(message['date_sent']), "dddd, mmmm dS, yyyy, h:MM:ss TT");
		var color = '#' + message['color'].toString(16);
		var messageDiv = [
							'<p class="message" ',
							'style="color:' + color + '; border-bottom: 3px solid '+ color+';" ',
							'data-color="' + color + '"',
							'data-id="' + message['id'] + '">',
							message['message'],
							'</p>',
							'<div class="hover-box">',
							'<p>' + date +  '</p>',
							'<p style="color: '+ color + ';">' + color + '</p>',
							'<p>Visibility: '+ message['seen'] + '</p>',
							'</div>',
							];
		$('#messages-area').append(messageDiv.join(''));
	}
}

function init() {
    loadAllMessages();
}

$(init);

