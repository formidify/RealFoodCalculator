/*
Chae Kim
 */

initialize();

function initialize() {

  var logged_in = sessionStorage.getItem("logged_in");
  console.log(logged_in);
  // TODO : change logged_in from true back to false if wanting to develop
  //    functionality.
  if (logged_in == null) {logged_in = true;}
  if (!window.location.href.includes("/login") && !(logged_in)){
    console.log("Getting false in line 15")
    redirect_to_login();
  }

  if (window.location.href.includes("/login")){
    // recognizes buttons, assigns functions for each button click
    var login_btn = document.getElementById('login_btn');
    login_btn.onclick = function() {
      var inputID = document.getElementById('id_bar').value;
      var inputPW = document.getElementById('pw_bar').value;
      if (confirm_credentials(inputID, inputPW)){
        login();
        console.log("Getting into the login if at least");
        go_to_home();
        console.log("WHY IS THIS NOT WORKING?2?@?@?");
        //redirect_to_home();
      }
      else{
        try_again();
      }
    }
  } else {
    // recognizes buttons, assigns functions for each button click
    var home_btn = document.getElementById('home_btn');
    if (home_btn != null){
      home_btn.onclick = function() {
        go_to_home();
      }
    }
    // TODO : might want to delete later
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
  document.location.href = (getBaseWebURL() + "/");
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
  document.location.href = (getBaseWebURL() + "/view_download");
}

function go_to_visualization() {
  console.log("Recognizing visualization button");
  document.location.href = (getBaseWebURL() + "/visualization");
}

function confirm_credentials(inputID, inputPW) {
  // TODO un-hard code this
  var userID = "RealFoodCalc2019";
  var userPW = "REALLYYUMMY";
  if (inputID==userID && inputPW==userPW){
   return true;
  }
 return false;
}

function try_again(){
  // TODO output console message onto screen so normal users can see
  console.log("Incorrect credentials, try again.");
  window.location.reload();
}

function login(){
  // TODO maybe look into localstorage if sessionstorage causes bugs.
  sessionStorage.setItem("logged_in",true);
  logged_in = true;
  console.log(logged_in);
}

function redirect_to_login(){
  console.log("Redirecting to log in page")
  document.location.href=(getBaseWebURL() + "/login");
}

function getBaseApiURL() {
  // TODO : unhard-code this!!
  var api_port = 5001;
  var baseURL = window.location.protocol + '//' + 'cmc307-06.mathcs.carleton.edu' + ':' + api_port;
  //var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + api_port;
  //console.log(baseURL);
  return baseURL;
}

function getBaseWebURL() {
  var baseWebURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port;
  //console.log(baseWebURL);
  return baseWebURL;
}

function vd_go_btn() {
  console.log("Go button pressed");
  var inputDict = {};
  var queryStrings = [];
  var inputList = document.getElementsByTagName("input");
  for (var i=0; i<inputList.length; i++){
    var element = inputList[i];
    if (element.value != ""){
      inputDict[element.getAttribute("placeholder")]=element.value;
      queryStrings.push(element.getAttribute("placeholder").toLowerCase()+"="+element.value+"&");
    }
  }
  console.log("queryString -> " + queryStrings);
  var query = getBaseApiURL()+"/test_data_large?";
  for (var i=0; i<queryStrings.length; i++){
    var str = queryStrings[i];
    query = query+str;
  }
  var url = query.substring(0,query.length - 1);
  console.log("url -> " + url);

  fetch(url)
    .then(res => res.json())
    .then((out) => {
      console.log('Checkout this JSON! ', out);
      append_json(out);})
    .catch(err => { throw err });
}

function append_json(data){
  var table = document.getElementById('results');
  console.log(table.getAttribute("id"));
  data.forEach(function(object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td>' + object.vendor + '</td>' +
    '<td>' + object.description + '</td>' +
    '<td>' + object.category + '</td>' +
    '<td>' + object.fair + '</td>' +
    '<td>' + object.year +'/'+ object.month + '</td>';
    table.appendChild(tr);
  });
}


  /*
  var advanced_search_button = document.getElementById('visualization_page_btn')
  advanced_search_button.onclick = function() {
    go_to_visualization();
  }

  // stores search text to query with and pass to next html page
  var search_button = document.getElementById('submit_search');
  search_button.onclick = function() {
    sessionStorage.setItem("search_text",document.getElementById("search_bar").value);
    sessionStorage.setItem("advanced_search", 1);
    go_to_display_page();
  }

  // when on advanced_search page, stores texts to search and pass to next page with
  if (window.location.pathname.includes("/advanced_search")) {
    var advanced_search_submit_button = document.getElementById('advanced_search_submit_button');
    console.log("created advanced_search_submit_button var");
    advanced_search_submit_button.onclick = function() {
      console.log("advanced_search_submit_button was clicked");
      sessionStorage.setItem("varieties_search_text",document.getElementById("varieties_search_bar").value);
      sessionStorage.setItem("taster_search_text",document.getElementById("taster_search_bar").value);
      sessionStorage.setItem("region_search_text",document.getElementById("region_search_bar").value);
      sessionStorage.setItem("description_search_text",document.getElementById("description_search_bar").value);
      sessionStorage.setItem("vineyard_search_text",document.getElementById("vineyard_search_bar").value);
      sessionStorage.setItem("country_search_text",document.getElementById("country_search_bar").value);
      sessionStorage.setItem("title_search_text",document.getElementById("title_search_bar").value);
      sessionStorage.setItem("advanced_search", 0);
    }
  }

  // when on display page, calls different functions for different types of search: advanced or regular
  if (window.location.pathname.includes("display")){
    console.log("in display page with: ");
    try {console.log(sessionStorage.getItem("search_text"));}
    catch(err) {
      console.log("sessionStorage search text empty");
    }
    console.log("as my search text");
    console.log(sessionStorage.getItem("advanced_search"));

    if (sessionStorage.getItem("advanced_search") == 1) {
      console.log("normal search");
      onWinesSearch("default", sessionStorage.getItem("search_text"));
    }
    else {
      console.log("advanced search");
      onAdvancedWinesSearch(sessionStorage.getItem("varieties_search_text"),
                            sessionStorage.getItem("taster_search_text"),
                            sessionStorage.getItem("region_search_text"),
                            sessionStorage.getItem("description_search_text"),
                            sessionStorage.getItem("vineyard_search_text"),
                            sessionStorage.getItem("country_search_text"),
                            sessionStorage.getItem("title_search_text"),
                            );
    }
  } else {
    discover_wine();
  }
}

// gives random wine for wine highlight of the moment
function discover_wine() {
  var url = getBaseApiURL() + '/wines';
  fetch(url)
  .then((response) => response.json())
  .then(function(wine_list) {
      var random_wine = wine_list[Math.floor(Math.random() * wine_list.length)];
      console.log(random_wine);
      var random_wine_body = '<header name="discover_wine" class="discover_wine">Discover Wine</header>'+
                             '<div class="left_box"><p class = "title">' + random_wine['title'] +
                             '</p><p class = "varieties"> varieties: ' + random_wine['variety'] +
                             '</p><text class = "winery"> Winery: ' + random_wine['winery'] +
                             '</text><text class = "place"> (' + random_wine['region'] +', '+ random_wine['province'] + ', ' + random_wine['country'] +
                             ')</text><p class = "points"> Points: ' + random_wine['points'] + '/100</p></div>'+
                             '<div class="middle_box"><p class = "description">Review: ' + random_wine['description'] +
                             '</p><text class = "taster_name">' + random_wine['taster_name'] +
                             '</text>  <text class = "taster_twitter_handle">(' + random_wine['taster_twitter_handle'] +
                             ')</text></div>' +
                             '<div class = "right_box">  <text class = "price">$' + random_wine['price'] +
                             '</text></div></div>';


      var discover_wine = document.getElementById('discover_wine');
      if (discover_wine) {
          discover_wine.innerHTML = random_wine_body;
      }})

      .catch(function(error) {
          console.log(error);
      });
}

function append(parent, el) {
  return parent.appendChild(el);
}

// function for displaying/writing into html the search results
function onWinesSearch(category, search_text) {
  if (category == "default") {category = "title"}
  var url = getBaseApiURL() + `/wines?${category}=${search_text}`;
  console.log(url);

  fetch(url)
    .then(response => response.json())
    .then(function(data) {
      console.log(data);
      var list = '';
      for (var k=0; k<data.length;k++) {
        list += '<li><div id="discover_wine" class="info_box">'+
                               '<div class="left_box"><p class = "title">' + data[k]['title'] +
                               '</p><p class = "varieties"> varieties: ' + data[k]['variety'] +
                               '</p><text class = "winery"> Winery: ' + data[k]['winery'] +
                               '</text><text class = "place"> (' + data[k]['region'] +', '+ data[k]['province'] + ', ' + data[k]['country'] +
                               ')</text><p class = "points"> Points: ' + data[k]['points'] + '/100</p></div>'+
                               '<div class="middle_box"><p class = "description">Review: ' + data[k]['description'] +
                               '</p><text class = "taster_name">' + data[k]['taster_name'] +
                               '</text>  <text class = "taster_twitter_handle">(' + data[k]['taster_twitter_handle'] +
                               ')</text></div>' +
                               '<div class = "right_box">  <text class = "price">$' + data[k]['price'] +
                               '</text></div></div></div></li>';
      }

      var search_wrap = document.getElementById('search_wrap');
      if (search_wrap) {
          search_wrap.innerHTML = list;
      }
    })
    .catch(error => console.error(error));
}

// creates query url
function onAdvancedWinesSearch(varieties, taster, region, description, vineyard, country, title) {
  var query_string="/wines?"

  if (varieties.length != 0) {
    query_string = query_string + `variety=${varieties}&`;
  }
  if (taster.length != 0) {
    query_string = query_string + `taster=${taster}&`;
  }
  if (region.length != 0) {
    query_string = query_string + `region=${region}&`;
  }
  if (description.length != 0) {
    query_string = query_string + `description=${description}&`;
  }
  if (vineyard.length != 0) {
    query_string = query_string + `vineyard=${vineyard}}&`;
  }
  if (country.length != 0) {
    query_string = query_string + `country=${country}&`;
  }
  if (title.length != 0) {
    query_string = query_string + `title=${title}&`;
  }
  if (query_string != "/wines?") {
    query_string = query_string.substring(0,query_string.length-1);
  }

  var url =  getBaseApiURL() + query_string;

  console.log(url);

  // create/write into html for search results
  fetch(url)
    .then(response => response.json())
    .then(function(data) {
      console.log(data);
      var list = '';
      for (var k=0; k<data.length;k++) {
        list += '<li><div id="discover_wine" class="info_box">'+
                               '<div class="left_box"><p class = "title">' + data[k]['title'] +
                               '</p><p class = "varieties"> varieties: ' + data[k]['variety'] +
                               '</p><text class = "winery"> Winery: ' + data[k]['winery'] +
                               '</text><text class = "place"> (' + data[k]['region'] +', '+ data[k]['province'] + ', ' + data[k]['country'] +
                               ')</text><p class = "points"> Points: ' + data[k]['points'] + '/100</p></div>'+
                               '<div class="middle_box"><p class = "description">Review: ' + data[k]['description'] +
                               '</p><text class = "taster_name">' + data[k]['taster_name'] +
                               '</text>  <text class = "taster_twitter_handle">(' + data[k]['taster_twitter_handle'] +
                               ')</text></div>' +
                               '<div class = "right_box">  <text class = "price">$' + data[k]['price'] +
                               '</text></div></div></div></li>';
      }
      var search_wrap = document.getElementById('search_wrap');
      if (search_wrap) {
          search_wrap.innerHTML = list;
      }
    })
    .catch(error => console.error(error));
}
*/
