/*
Chae Kim
Dawson d'Almeida
Justin Washington

Web application phase 6
 */

initialize();

function initialize() {

  // recognizes buttons, assigns functions for each button click
  var home_button = document.getElementById('go_to_home_page');
  home_button.onclick = function() {
    go_to_home_page();
  }

  var discover_wine_button = document.getElementById('go_to_discover_wine');
  discover_wine_button.onclick = function() {
    go_to_discover_wine();
  }

  var about_button = document.getElementById('go_to_about_page');
  about_button.onclick = function () {
    go_to_about_page();
  }

  var advanced_search_button = document.getElementById('go_to_advanced_search_page')
  advanced_search_button.onclick = function() {
    go_to_advanced_search_page();
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

function go_to_home_page() {
  document.location.href = getBaseWebURL();
}

function go_to_discover_wine(){
  document.location.href = (getBaseWebURL() + "#discover_wine");
}

function go_to_about_page(){
  document.location.href = (getBaseWebURL() + "/about");
}

function go_to_display_page() {
  document.location.href = (getBaseWebURL() + "/display");
}

function go_to_advanced_search_page() {
  document.location.href = (getBaseWebURL() + "/advanced_search");
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

function getBaseApiURL() {
  var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + api_port;
  return baseURL;
}

function getBaseWebURL() {
    var baseWebURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port;
    console.log(baseWebURL);
    return baseWebURL;
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
