// Not successful because the recommendation system is being loaded even before the page is loaded
// window.addEventListener("load", () => {
//   var element = document.getElementById("loader");
//   element.id = "loading";
// });

// to show loader animation when the recommendation system is loading
function loader() {
  var element = document.getElementById("loader");
  element.id = "loading";
}

// to show password when checkbox is checked
function show_password() {
  var checkBox = document.getElementById("passwordCheck");
  var pass = document.getElementById("password");
  var confirm_pass = document.getElementById("confirmPassword");
  if (checkBox.checked == true) {
    pass.type = "text";
    // to check whether confirm_pass element exists
    if (typeof confirm_pass != "undefined" && confirm_pass != null) {
      confirm_pass.type = "text";
    }
  } else {
    pass.type = "password";
    if (typeof confirm_pass != "undefined" && confirm_pass != null) {
      confirm_pass.type = "password";
    }
  }
}

// to change bookmark button on click
function turnBookmark() {
  var bookmark_icon = document.getElementById("bookmark-icon");
  if (bookmark_icon.classList.contains("bi-bookmark-check-fill")) {
    bookmark_icon.classList.remove("bi-bookmark-check-fill");
    bookmark_icon.classList.add("bi-bookmark");
  } else {
    bookmark_icon.classList.remove("bi-bookmark");
    bookmark_icon.classList.add("bi-bookmark-check-fill");
  }
}

// function update_data_frame() {
//   url = "/update";
//   fetch(url, { method: "POST" })
//     .then(function (response) {
//       return response.json();
//     })
//     .then(function (myJson) {
//       store = myJson;
//       //This line prints out "{somedata":"somedatavalue","somedata1":"somedatavalue1"}" every 2000 milliseconds
//       console.log(store);
//     });
// }

// form.addEventListener("submit", function (event) {
//   event.preventDefault(); // prevent page from refreshing
//   const formData = new FormData(form); // grab the data inside the form fields
//   url = "/anime";
//   fetch(url, {
//     // assuming the backend is hosted on the same server
//     method: "POST",
//     body: formData,
//   }).then(function (response) {
//     // do something with the response if needed.
//     // If you want the table to be built only after the backend handles the request and replies, call buildTable() here.
//   });
// });
