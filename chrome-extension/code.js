var current_session_contributions = 0;

// ask the db for the url of a mystery number
function askforatarget() {
	document.getElementById("upload-button").disabled = true;
	document.getElementById("upload-button").innerText = "Contributing...";
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() { 
	if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
	    getnumber(xmlHttp.responseText);
	}
	xmlHttp.open("GET", "http://kayali.io:1513/", true); // true for asynchronous 
	xmlHttp.send(null);
}

// get the number from adam's website
function getnumber(url) {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() { 
		if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
			if(xmlHttp.responseText.includes("rate-limited")) {
				// we've been rate limited :(
				wearelimited();
			} else {
				// we got a number! Let's share the goodness :D
		    		transmitnumber(url, xmlHttp.responseText);
			} 
		}
	}
	xmlHttp.open("GET", url, true); // true for asynchronous 
	xmlHttp.send(null);
}

// send it back to the database
function transmitnumber(url, number) {
	var xhr = new XMLHttpRequest();
	xhr.open('POST', 'http://kayali.io:1513/', true);
	xhr.onload = function () {
		current_session_contributions += 1
	};
        var index = url.split("?")[1]
        xhr.send(index + "," + number);
	console.log("Told db about the contents of " + index + " which where: '" + number + "'");

	// we're greedy: try to get another number
	askforatarget();
}

function wearelimited() {
	updatestatus();
	document.getElementById("upload-button").disabled = false;
	document.getElementById("upload-button").innerText = "Contribute";
	var contribution_text;
	if (current_session_contributions == 0)
		contribution_text = "We've been rate limited. Try again in about 6 hours.";
	else
		contribution_text = "You contributed " + current_session_contributions + " numbers. Nice!";
	document.getElementById("contribution-status").innerText = contribution_text;
	current_session_contributions = 0;
}

function updatestatus() {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() { 
	if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
	    document.getElementById("status-here").innerText = xmlHttp.responseText;
	}
	xmlHttp.open("GET", "http://kayali.io:1513/status", true); // true for asynchronous 
	xmlHttp.send(null);
}

document.getElementById("upload-button").addEventListener("click", function() {
	askforatarget();
});

window.addEventListener("load", function(){
	updatestatus();
});;
