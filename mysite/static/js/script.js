var form = document.getElementById('chat-box');
var submit = document.getElementById('chat-submit');
var input = document.getElementById('chat-user');
var container = document.getElementById('dialogue-container');
var keywords = [];
var reply;
var final_transcript = ''; //final speech transcript made as global variable
var recognizing = false;
var ignore_onend;
var start_timestamp;

window.onload=function(){ //somehow we need to load first or not it will return an error (null)
	showInfo('info_start');
	start_button.style.display = 'inline-block';
	form = document.getElementById('chat-box');
	submit = document.getElementById('chat-submit');
    input = document.getElementById('chat-user');
    container = document.getElementById('dialogue-container');
    keywords = [];
    reply;
	//audioPlayer = document.getElementById('audio-player');
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        create_bubble_user();
	});
	//check_reminder(); //polling for any reminders
}

function create_bubble_user() {
	if (input.value!==null && input.value!==''){ 
		keywords = input.value.toLowerCase()
			.replace(/[^\w\s]|_/g, '')
			.replace(/\s+/g, ' ').split(' ');
		var div = document.createElement('DIV');
		var para = document.createElement('SPAN');
		var txt = document.createTextNode(input.value);
		div.setAttribute('class', 'dialogue dialogue-user');
		para.appendChild(txt);
		div.appendChild(para);
		container.appendChild(div);
		count_childs();

		chat_respond(input.value).then((json) => {
				reply = json['message']['text'];
				console.log("async test")
				console.log(reply)
			});

		setTimeout(function() {
			create_bubble_bot(reply);
		}, 500); // displays alert box after 500 milliseconds, after half a second.
		
		input.value = '';
	}
}

async function chat_respond(str){
	var message = {
			'text': str,
			'user': true, // message posted from client
			'chat_bot': false, // gets the text, and indicates that its from user
		};
	const response = await fetch("/get-response/", { // fetch response to get json string?
		body: JSON.stringify({'message': message['text']}), // message that you typed
		cache: 'no-cache', 
		credentials: 'same-origin', // indicates that it's not csrf attack?
		headers: {
			'user-agent': 'Mozilla/4.0 MDN Example', // specifying that browser should be this
			'content-type': 'application/json' // specifying this is JSON request
		},
		method: 'POST',
		mode: 'cors', 
		redirect: 'follow',
		referrer: 'no-referrer',
	});
	return response.json();
}

function create_bubble_bot(str) {
  var div = document.createElement('DIV');
  var para = document.createElement('SPAN');
  var txt = document.createTextNode(str);
  div.setAttribute('class', 'dialogue dialogue-bot');
  para.appendChild(txt);
  div.appendChild(para);
  container.appendChild(div);
  count_childs();
}

function count_childs() {
	var convolength = 7
	var children = container.children;
	if (children.length > convolength) {
		while (children.length > convolength) {
		container.removeChild(container.firstChild);
		}
	}
	if (children.length > 3) {
		var transparency = 1;
		for (var i = children.length - 4; i >= 0; i--) {
		transparency -= 0.15;
		children[i].style.opacity = transparency;
		}
	}
}

function startButton(event) {
	if (recognizing) {
	  recognition.stop();
	  return;
	}
	final_transcript = '';
	recognition.lang = 'en-GB';
	recognition.start();
	ignore_onend = false;
	final_span.innerHTML = '';
	interim_span.innerHTML = '';
	start_img.src = '/static/img/mic-slash.gif'; //mic slash image shown (usually for short while). Noticable when Chrome asks user for permission to use mic
	showInfo('info_allow');
	//showButtons('none');
	start_timestamp = event.timeStamp;
  }
  
  if (!('webkitSpeechRecognition' in window)) { //checks if webkitspeechreg object exists
	  upgrade(); //if it does not, check user to upgrade browser
  } else {
	  var recognition = new webkitSpeechRecognition();
	  recognition.continuous = true; //if false, speech recognition will stop when user stops talking
	  recognition.interimResults = true; //shows interim results, if false, results from are final
  
	  recognition.onstart = function() { //recognition.start() that is called by pressing mic button calls this onstart event ahndler
		  recognizing = true;
		  showInfo('info_speak_now');
		  start_img.src = '/static/img/mic-animate.gif';
	  };
  
	  recognition.onerror = function(event) {
		  if (event.error == 'no-speech') {
			start_img.src = '/static/img/mic.gif';
			showInfo('info_no_speech');
			ignore_onend = true;
		  }
		  if (event.error == 'audio-capture') {
			start_img.src = '/static/img/mic.gif';
			showInfo('info_no_microphone');
			ignore_onend = true;
		  }
		  if (event.error == 'not-allowed') {
			if (event.timeStamp - start_timestamp < 100) {
			  showInfo('info_blocked');
			} else {
			  showInfo('info_denied');
			}
			ignore_onend = true;
		  }
	  };

	  recognition.onspeechend = function() {
	  	console.log('Speech has stopped being detected');
	  };
  
	  recognition.onend = function() {
		  recognizing = false;
		  create_bubble_user_speech(final_transcript); //upon end of recogniton, send final transcript to server
		  if (ignore_onend) {
			return;
		  }
		  start_img.src = '/static/img/mic.gif';
		  /*
		  if (!final_transcript) {
			showInfo('info_start');
			return;
		  }
		  */
		  showInfo('info_start');
		  final_span.innerHTML = '';
		  interim_span.innerHTML = '';
	  };
  
	  recognition.onresult = function(event) { // for each set of results, it calls this event handler
		  var interim_transcript = '';
		  for (var i = event.resultIndex; i < event.results.length; ++i) { //appends any new final text
		  	clearTimeout(speechtimeout);
		  	setSpeechTimeout();
			if (event.results[i].isFinal) {
			  final_transcript += event.results[i][0].transcript;
			} else {
			  interim_transcript += event.results[i][0].transcript;
			}
		  }
		  final_transcript = capitalize(final_transcript);
		  final_span.innerHTML = linebreak(final_transcript); //results might include \n, so linebreak converts these to HTML tags. Then sets string as innerHTML of span elements
		  interim_span.innerHTML = linebreak(interim_transcript);
	  };
  }

var speechtimeout;

function setSpeechTimeout () {
	speechtimeout = setTimeout(function() {recognition.stop(); }, 7000); // stop recogntion after 5 seconds
}
  
function create_bubble_user_speech(str) {
	if (str != '') {
		var div = document.createElement('DIV');
		var para = document.createElement('SPAN');
		var txt = document.createTextNode(str);
		div.setAttribute('class', 'dialogue dialogue-user');
		para.appendChild(txt);
		div.appendChild(para);
		container.appendChild(div);
		count_childs();

		chat_respond(str).then((json) => {
				reply = json['message']['text'];
				console.log("speech input/receive test")
				console.log(reply)
			});

		setTimeout(function() {
			create_bubble_bot(reply);
			//audioPlayer.setAttribute('src',audiosource);
			//audioPlayer.load();
			//audioPlayer.play();
		}, 500); // displays alert box after 500 milliseconds, after half a second.
		
		//str = '';
	}
}

function showInfo(s) { // info, tells what info to show
	if (s) {
	  for (var child = info.firstChild; child; child = child.nextSibling) {
		if (child.style) {
		  child.style.display = child.id == s ? 'inline' : 'none';
		}
	  }
	  info.style.visibility = 'visible';
	} else {
	  info.style.visibility = 'hidden';
	}
}
// info text, tell user to update browser that support web speech API
function upgrade() {
	start_button.style.visibility = 'hidden';
	showInfo('info_upgrade');
}
// linebreak function
var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
	return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}
// capitalize function
var first_char = /\S/;
function capitalize(s) {
	return s.replace(first_char, function(m) { return m.toUpperCase(); });
}
