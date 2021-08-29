addEventListener("DOMContentLoaded", () => {
	try {
		CSRFTOKEN = document.getElementsByName("csrfmiddlewaretoken")[0].value;
	} catch (error) {
		console.log("No form in this page");
	}
	highlightsideDiv();
	highlightPageNumber();
});

function adjustFollowCounter(direction, profileId) {
	var followCounter = document.querySelector(".followerCounter");
	var followNumber = parseInt(followCounter.innerText);
	var followButton = document.querySelector("#followButton");
	switch (direction) {
		case "increase":
			followNumber += 1;
			followCounter.innerText = followNumber;
			followButton.innerText = "Unfollow";
			followButton.onclick = function () {
				unfollowUser(profileId);
			};
			break;
		case "decrease":
			followNumber -= 1;
			followCounter.innerText = followNumber;
			followButton.innerText = "Follow";
			followButton.onclick = function () {
				followUser(profileId);
			};
			break;
	}
}

function highlightPageNumber() {
	var pageNumber = document.getElementsByName("pageNumber")[0].value;
	var currentPage = document.getElementById(pageNumber);
	currentPage.classList.add("currentPage");
}
// Funtion to highlight current page in side div
function highlightsideDiv() {
	var page = window.location.pathname.split("/").pop();
	var profileId = document.querySelector("#profileId").value;
	if (page == "") {
		element = document.querySelector("#allPosts");
		element.classList.add("highlight");
		element.firstElementChild.src =
			"/static/network/images/homeClicked.svg";
	} else if (page == "following") {
		element = document.querySelector("#following");
		element.classList.add("highlight");
	} else {
		if (profileId == page) {
			element = document.querySelector("#profile");
			element.classList.add("highlight");
			element.firstElementChild.src =
				"/static/network/images/userClicked.svg";
		}
	}
}
// A function that counts number of characters in a post
function characterCount() {
	text = document.querySelector("#newPost");
	return text.innerText.length;
}

// Like or dislike a post
function postClicked(postId, obj) {
	likesCountSpan = obj.nextSibling;
	likesCount = parseInt(likesCountSpan.innerText);
	if (obj.className == "True") {
		obj.className = "False";
		obj.src = "/static/network/images/heart.svg";
		likesCount -= 1;
		likesCountSpan.innerText = likesCount;
		dislikePost(postId);
	} else {
		obj.className = "True";
		obj.src = "/static/network/images/heartClicked.svg";
		likesCount += 1;
		likesCountSpan.innerText = likesCount;
		likePost(postId);
	}
}
// Adding a max character limit for new posts
function CharactersNumber() {
	// Getting the paragrapgh containing word count and the submit button
	count = document.querySelector("#charactersNumber");
	submitNewPost = document.querySelector("#submitNewPost");

	// Counting the charachters in the new post to limit the number below 500
	numberOfCharacters = characterCount();
	if (numberOfCharacters > 500) {
		submitNewPost.disabled = true;
		count.className = "charCountRed";
		count.innerText = `${numberOfCharacters} Characters (${
			500 - numberOfCharacters
		})`;
	} else {
		submitNewPost.disabled = false;
		count.className = "charCountGreen";
		count.innerText = numberOfCharacters + " Characters";
	}
}
function logResponse(data) {
	data.success
		? console.log(`%c ${data.success}`, "color:green;font-size:15px")
		: console.error(data.fail);
}
// Funtion to Save users new posts
function submitPost(obj) {
	postContent = document.querySelector("#newPost").innerText;
	numberOfCharacters = characterCount();
	if (numberOfCharacters > 500 || numberOfCharacters == 0) {
		obj.disabled = true;
	} else {
		fetch("/post", {
			method: "POST",
			headers: { "X-CSRFToken": CSRFTOKEN },
			credentials: "same-origin",
			body: JSON.stringify({
				content: postContent,
			}),
		})
			.then((response) => response.json())
			.then((data) => {
				logResponse(data);
				location.reload();
			});
	}
}

function likePost(postId) {
	fetch("/likePost", {
		method: "POST",
		headers: { "X-CSRFToken": CSRFTOKEN },
		credentials: "same-origin",
		body: JSON.stringify({
			id: postId,
		}),
	})
		.then((response) => response.json())
		.then((data) => logResponse(data));
}

function dislikePost(postId) {
	fetch("/dislikePost", {
		method: "POST",
		headers: { "X-CSRFToken": CSRFTOKEN },
		credentials: "same-origin",
		body: JSON.stringify({
			id: postId,
		}),
	})
		.then((response) => response.json())
		.then((data) => logResponse(data));
}

function followUser(profileId) {
	fetch(`/followUser`, {
		method: "POST",
		headers: { "X-CSRFToken": CSRFTOKEN },
		credentials: "same-origin",
		body: JSON.stringify({
			id: profileId,
		}),
	})
		.then((response) => response.json())
		.then((data) => {
			logResponse(data);
			adjustFollowCounter("increase", profileId);
		});
}
function unfollowUser(profileId) {
	fetch(`/unfollowUser`, {
		method: "POST",
		headers: { "X-CSRFToken": CSRFTOKEN },
		credentials: "same-origin",
		body: JSON.stringify({
			id: profileId,
		}),
	})
		.then((response) => response.json())
		.then((data) => {
			logResponse(data);
			adjustFollowCounter("decrease", profileId);
		});
}

function editPost(postId,useCase) {
	// get the div containing the post body and text area
	var post = document.getElementsByClassName(`postBody ${postId}`)[0];
	var postEditForm = document.getElementsByClassName(`editForm ${postId}`)[0]

	// get the contents of the post to populate the text field
	var postContent = post.firstElementChild.innerText;
	switch (useCase){
		case 'edit':
			// Hide original Post Content
			post.firstElementChild.style.display = "none";
			
			// display the edit form and populate it with the post content 
			postEditForm.style.display= "block"
			postEditForm.firstElementChild.value = postContent 
			break

		case 'save':
			// Append the new post content and display the post element
			postContent = postEditForm.firstElementChild.value
			post.firstElementChild.innerText = postContent
			post.firstElementChild.style.display="block"

			// Hide the Edit form again and reset it's value
			postEditForm.style.display= 'none'
			postEditForm.firstElementChild.value = ''
			return postContent
		
		case 'cancel':
			// Hide the Edit form again and reset it's value
			postEditForm.style.display= 'none'
			postEditForm.firstElementChild.value = ''	

			// Reset post content to it's original value then display it
			post.firstElementChild.innerText = postContent
			post.firstElementChild.style.display="block"
			break
	}


}
function updatePostData(postId) {
	postContent= editPost(postId,'save')

	fetch("/editPost", {
		method: "POST",
		headers: { "X-CSRFToken": CSRFTOKEN },
		credentials: "same-origin",
		body: JSON.stringify({
			id: postId,
			postContent:postContent,
		}),
	})
		.then((response) => response.json())
		.then((data) => {
			logResponse(data);
		});
}
