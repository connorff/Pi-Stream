class Messages {
	constructor() {
		let messages = this.checkMessages(true)
	}
	
	post(content) {
		let error = document.getElementById("error")
		
		if (content.length > 250) {
			error.innerHTML = `Comment length ${content.length - 250} characters too long`
			return
		}
		else if (content.trim() == "") {
			error.innerHTML = "Comment cannot be empty"
			return
		}
		
		let xhr = createXHR()
		
		xhr.onreadystatechange = () => {
			if (this.readyState == 4 && this.status == 200) {
			   
			}
		}
		
		xhr.open("GET", `../apis/post?content=${content}`, true);
		xhr.send();
	}
	
	checkMessagesAfter() {
		let xhr = createXHR()
		
		xhr.onreadystatechange = () => {
			if (xhr.readyState == 4 && xhr.status == 200) {
				let response = JSON.parse(xhr.responseText);
				
				//if there is a new message
				if (response.length) {
					addMessages(response)
					this.lastMessage = response[response.length - 1][0]
				}
			}
		}
		
		xhr.open("GET", `/apis/checkafter?id=${this.lastMessage}`, true);
		xhr.send();
	}
	
	checkMessages(struct = false) {
		let xhr = createXHR();
		
		xhr.onreadystatechange = () => {
			if (xhr.readyState == 4 && xhr.status == 200) {
				let messages = JSON.parse(xhr.responseText);
				
				if (struct) {
					this.lastMessage = messages[messages.length - 1][0];
					return;
				}
				
				return messages;
			}
		}
		
		xhr.open("GET", "/apis/check", true);
		xhr.send();
	}
}

let m = new Messages()
document.getElementById("comments").scrollTop = document.getElementById("comments").scrollHeight;

setInterval(() => {
	m.checkMessagesAfter(m.lastMessage);
}, 1000)

function createXHR() {
	let xhr;

	//if XHR is supported
	if (window.XMLHttpRequest){
		xhr = new XMLHttpRequest();
	}
	else {
		xhr = new ActiveXObject("Microsoft.XMLHTTP");
	}

	return xhr;
}

function addMessages(messages) {
	messages.forEach((message) => {
		let link = "/user/" + message[4]
		//innerHTML is not good, change to createTextNode() later
		document.getElementById("comments").innerHTML += `<div class="comment-block">
				<div><strong>${message[1]}</strong><a href="/user/${message[4]}" style="color: gray; margin-left: 10px;">(${link})</a></div>
				<div class="comment-content">${message[3]}</div>
				<div class="comment-time">${message[2]}</div>
			</div>`
	})
	document.getElementById("comments").scrollTop = document.getElementById("comments").scrollHeight;
}

document.getElementById("post-button").onclick = postContent

function postContent() {
	m.post(document.getElementById("create-post-content").value)
	document.getElementById("create-post-content").value = "";
}

window.onkeydown = (e) => {
	switch (e.keyCode) {
		case 13:
			postContent()
			break;
	}
}

document.getElementById("create-post-content").onkeyup = () => {
	let error = document.getElementById("error")
	let content = document.getElementById("create-post-content").value
	
	if (content.length > 250) {
		error.innerHTML = `Comment length ${content.length - 250} characters too long`
	}
	else if (content.trim() == "") {
		error.innerHTML = "Comment cannot be empty"
		return
	}
	else {
		error.innerHTML = null;
	}
}


