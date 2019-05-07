/*
This javascript file takes care of the login system
It also holds the functions for the navigation bar.
 */

initialize();

function initialize() {
  // this object does not exist unless attempted to log in
  var logged_in = sessionStorage.getItem("logged_in");
  // if (logged_in == null) {logged_in =true;}
  if (logged_in == null) {logged_in =false;}

  // if not logged in but attempting to get onto another page of website
  //  , redirect to login page.
  if (!window.location.href.includes("/rfc_login") && !(logged_in)){
    redirect_to_login();
  }

  // extra step taken so if someone tries to manually set the sessionStorage
  //  will also check where you got redirected from.
  if (logged_in && !window.location.href.includes("/rfc_login")){
    if (document.referrer.includes("/rfc_login")){
    }else if (document.referrer.includes("/rfc_home")){
    }else if (document.referrer.includes("/entry_session")){
    }else if (document.referrer.includes("/data_entry")){
    }else if (document.referrer.includes("/visualization")){
    }else if (document.referrer.includes("/rfc_view_download")){
    }else{
      sessionStorage.removeItem("logged_in");
      redirect_to_login();
    }
  }

  if (window.location.href.includes("/rfc_login")){
    // get user input and use login() funct. below to check credentials.
    var login_btn = document.getElementById('login_btn');
    login_btn.onclick = function() {
      var inputID = document.getElementById('id_bar').value;
      var inputPW = document.getElementById('pw_bar').value;
      login(inputID, inputPW);
    }
  } else {
    // assigns functions for each button on navigation bar
    var home_btn = document.getElementById('home_btn');
    if (home_btn != null){
      home_btn.onclick = function() {
        go_to_home();
      }
    }
    var data_entry_btn = document.getElementById('data_entry_btn');
    if (data_entry_btn != null){
      data_entry_btn.onclick = function() {
        go_to_data_entry();
      }
    }

    var entry_session_btn = document.getElementById('entry_session_btn');
    if (entry_session_btn != null) {
      entry_session_btn.onclick = function() {
        go_to_entry_session();
      }
    }

    var view_download_btn = document.getElementById('view_download_btn');
    if (view_download_btn != null) {
      view_download_btn.onclick = function () {
        go_to_view_download();
      }
    }

    var visualization_btn = document.getElementById('visualization_btn');
    if (visualization_btn != null) {
      visualization_btn.onclick = function () {
        go_to_visualization();
      }
    }
  }
}

//BUTTON FUCTIONS
function go_to_home() {
  console.log("Recognizing home button");
  document.location.href = (getBaseWebURL() + "/rfc_home");
}

function go_to_data_entry(){
  console.log("Recognizing data entry button");
  document.location.href = (getBaseWebURL() + "/data_entry");
}

function go_to_entry_session(){
  console.log("Recognizing entry session button");
  document.location.href = (getBaseWebURL() + "/entry_session");
}

function go_to_view_download() {
  console.log("Recognizing view download button");
  document.location.href = (getBaseWebURL() + "/rfc_view_download");
}

function go_to_visualization() {
  console.log("Recognizing visualization button");
  document.location.href = (getBaseWebURL() + "/visualization");
}

// checks whether login credentials are correct
/*function login(inputID, inputPW) {
  var query = getBaseApiURL()+"/52Ow41jelt"
  console.log(query);
  fetch(query)
  .then(function(u){ return u.json();})
  .then(function(data){
    var key = data[0].random;
    console.log(key);
    var eActualID ="U2FsdGVkX18wOFwtwuBHkOYPeQ3dUlcl7NUNj2b0ms9SgTlq4hj3lBLwKlmMR+ar"
    var eActualPW ="U2FsdGVkX1+O7Wb3KqZ0qK1e7lrRWgqqipFG/N5cgjg="
    var dActualID = CryptoJS.AES.decrypt(eActualID, key).toString(CryptoJS.enc.Utf8);
    var dActualPW = CryptoJS.AES.decrypt(eActualPW, key).toString(CryptoJS.enc.Utf8);
    if (inputID == dActualID && inputPW == dActualPW) {
      sessionStorage.setItem("logged_in",true);
      go_to_home();
      console.log("gotin");
    }
    else { try_again();}
  })
  return true;
}*/

function login(inputID, inputPW){
  if (inputID && inputPW){
    sessionStorage.setItem("logged_in",true);
    go_to_home();
    console.log("gotin");
  }
  else { try_again();}
}

function try_again(){
  // TODO output console message onto screen so normal users can see
  console.log("Incorrect credentials, try again.");
  window.location.reload();
}

function redirect_to_login(){
  console.log("Redirecting to log in page")
  document.location.href=(getBaseWebURL() + "/rfc_login");
}

function getBaseApiURL() {
  // TODO : figure out how to unhard-code this!!
  var api_port = 5001;
  var baseURL = window.location.protocol + '//' + 'cmc307-06.mathcs.carleton.edu' + ':' + api_port;
  return baseURL;
}

function getBaseWebURL() {
  var baseWebURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port;
  //console.log(baseWebURL);
  return baseWebURL;
}
