var ROOT = "http://vaspberry.duckdns.org/"
var LIMIT = 10;
var OPACITY_TOLERANCE = 25;
var OPACITY_MIN = .005;
var FONTSIZE_SCALER = 500;
var FONTSIZE_MAX = 1.2;

var incrementors = {};

function isColorHex(h) {
	var a = parseInt(h,16);
	return (a.toString(16) === h.toLowerCase() && h.length == 6);
}

function htmlEntities(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function loadHash(){
	var hash = window.location.hash;

	if(hash && hash != '#all' && isColorHex(hash.split("#")[1])){
		$('.message').hide();
		$('.message.info').html('<a class="x-button" href="#all">Showing all messages from ' + hash + '</a>');
		$('.message.info').show();
		$('.user.message').filter('[data-color="'+hash+'"]').show();
		window.scrollTo(0,0)
	}else if(hash == '#about'){
		$('.message').hide();
		$('.message.info').html('<a class="x-button" href="#all">Back</a>');
		$('.message.info').show();
		$('.message.about').show();
	}else if(hash == "#community-guidelines"){
		$('.message').hide();
		$('.message.info').html('<a class="x-button" href="#all">Back</a>');
		$('.message.info').show();
		$('.message.community-guidelines').show();
	}else if(hash == '#all'){
		$('.message').hide();
		$('.message.info').html('Showing all messages.');
		$('.message.info').show();
		$('.user.message').show();
	}else {
		window.location.hash = "#all";
	}
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

function update(url, responseType, updateObj) {
	return new Promise(function(resolve, reject){
	    var xhr = new XMLHttpRequest();
	    xhr.open('PATCH', url);
	    xhr.setRequestHeader('Content-type','application/json');
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

	    xhr.send(JSON.stringify(updateObj));
	});
}

function getMessagesURL(page){
	return encodeURI(ROOT + "messages?_sort=date_sent&_order=DESC&_page=" + page + "&_limit=" + LIMIT);
}

function loadMessagePage(page) {
	return load(getMessagesURL(page), 'json')
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

function calculateOpacity(visibility){
	return Math.max((Math.min(visibility, 0)) ? 1 - (Math.abs(visibility)/OPACITY_TOLERANCE) : 1, OPACITY_MIN);
}

function calculateFontsize(visibility){
	return Math.min((Math.min(visibility, 0)) ? 1 : 1 + visibility/FONTSIZE_SCALER, FONTSIZE_MAX);
}

function addToPage(messages){
	for(messageIndex in messages){
		var message = messages[messageIndex];
		var date = dateFormat(new Date(0).setUTCSeconds(message['date_sent']), "dddd, mmmm dS, yyyy, h:MM:ss TT");
		var color = '#' + message['color'].toString(16);
		var opacity = calculateOpacity(message['seen']);
		var fontsize = calculateFontsize(message['seen']);
		incrementors[message['id']] = makeIncrementor(message['id']);
		var messageDiv = $([
							'<div class="message user" ',
							'style="color:' + color + ';',
							'border-bottom: 3px solid '+ color+';" ',
							'data-color="' + color + '"',
							'data-id="' + message['id'] + '">',

								htmlEntities(message['message']),

								'<div class="hover-box">',
									'<a href="'+ color+'" style="color: '+ color + ';"><p>Color: ' + color + '</p></a>',
									'<p class="visibility">Visibility: '+ message['seen'] + '</p>',
									'<p>' + date +  '</p>',
								'</div>',
							
								'<div class="vote-buttons">',
									'<div class="vote-button downvote" onclick="incrementors[' + message['id'] + '].decrement()">',
									'</div>',
									'<div class="vote-button upvote" onclick="incrementors[' + message['id'] + '].increment()">',
									'</div>',
								'</div>',

							'</div>',
						].join(''));
		$('#messages-area').append(messageDiv);
		updateMessageView(message);
	}
}

function updateMessageView(response){
		var opacity = calculateOpacity(response['seen']);
		var fontsize = calculateFontsize(response['seen']);
		$('[data-id=' + response['id'] + '] .hover-box>.visibility').text('Visibility: ' + response['seen']);
		$('[data-id=' + response['id'] + ']')
		.data('opacity', opacity)
		.data('fontsize', fontsize)
		.css('opacity', opacity)
		.css('font-size', fontsize + 'em');
	}

function getMessageURL(id){
	return encodeURI(ROOT + "messages/" + id);
}

function loadMessage(id){
	return load(getMessageURL(id), 'json')
}


function makeIncrementor(id){
	function getMessage(id, callback){
		loadMessage(id).then(function(response){
			callback(response.response);
		}).catch(function(err){
	        console.log("Error: " + err);
	    });

	}

	function updateMessage(id, obj, callback){
		update(getMessageURL(id), 'json', obj).then(function(response){
			callback(response.response);
		}).catch(function(err){
	        console.debug("Error: " + err);
	    });
	}

	function changeVisibility(id, deltaVal){
		getMessage(id, function(response){
			updateMessage(id, {'seen': response['seen'] + deltaVal}, updateMessageView);
		});
	}

	return {
		increment: function(){
			changeVisibility(id, 1);
		},
		decrement: function(){
			changeVisibility(id, -1);
		}
	}
}



function init() {
    loadAllMessages();
}

$(init);

