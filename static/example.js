/*
Chae Kim
 */

initialize();

function initialize() {

  var logged_in = sessionStorage.getItem("logged_in");
  console.log(logged_in);
  var key=get_key();
  console.log(CryptoJS.AES.encrypt("RealFoodCalc2019", key));
  console.log(CryptoJS.AES.encrypt("REALLYYUMMY", key));
  // TODO : change logged_in from true back to false if wanting to develop
  //    functionality.
  if (logged_in == null) {logged_in =false;}
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

function get_key() {
  var key;
  var query = getBaseApiURL()+"/52Ow41jelt";
  fetch(query)
    .then(res => res.json())
    .then(data => key=data)
    .then(()=> console.log(obj))
    .catch(err => { throw err });
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
  var orderBy = document.getElementById("category");
  var table = document.getElementById('results');
  var table_len = table.getElementsByTagName('tr').length;
  console.log(table_len);
  for (var row=table_len-1; row>0; row--){
    //console.log("row: "+row.toString());
    table.deleteRow(row);
  }

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
  queryStrings.push("orderBy="+orderBy.value);
  console.log("queryString -> " + queryStrings);
  var query = getBaseApiURL()+"/test_data_large?";
  for (var i=0; i<queryStrings.length; i++){
    var str = queryStrings[i];
    query = query+str;
  }
  /*var url = query.substring(0,query.length - 1);
  console.log("url -> " + url);*/

  var search_result={};

  fetch(query)
    .then(res => res.json())
    .then((out) => {
      search_result=out;
      // TODO : figure out how to transfer json data
      append_json(out);})
    .catch(err => { throw err });

  console.log('Checkout this search result! ', search_result)
}

function append_json(data){
  var table = document.getElementById('results');
  console.log(table.getAttribute("id"));
  var cur_row = 0;
  data.forEach(function(object) {
    var tr = document.createElement('tr');
    tr.innerHTML =
    '<td>'+'<button class="editbtn" onclick="editbtn(' +
    cur_row.toString()+');">' + 'edit</button></td>' +
    '<td contenteditable=false title="month">' + object.month + '</td>' +
    '<td contenteditable=false title= "year">' + object.year + '</td>' +
    '<td contenteditable=false title="description">' + object.description + '</td>' +
    '<td contenteditable=false title="category">' + object.category + '</td>' +
    '<td contenteditable=false title="productCode">' + object.productCode + '</td>' +
    '<td contenteditable=false title="productCodeType">' + object.productCodeType + '</td>' +
    '<td contenteditable=false title="brand">' + object.brand + '</td>' +
    '<td contenteditable=false title="vendor">' + object.vendor + '</td>' +
    '<td contenteditable=false title="rating">' + object.rating + '</td>' +
    '<td contenteditable=false title="local">' + object.local + '</td>' +
    '<td contenteditable=false title="localDescription">' + object.localDescription + '</td>' +
    '<td contenteditable=false title="fair">' + object.fair + '</td>' +
    '<td contenteditable=false title="fairDescription">' + object.fairDescription + '</td>' +
    '<td contenteditable=false title="ecological">' + object.ecological + '</td>' +
    '<td contenteditable=false title="ecologicalDescription">' + object.ecologicalDescription + '</td>' +
    '<td contenteditable=false title="humane">' + object.humane + '</td>' +
    '<td contenteditable=false title="humaneDescription">' + object.humaneDescription + '</td>' +
    '<td contenteditable=false title="disqualifier">' + object.disqualifier + '</td>' +
    '<td contenteditable=false title="disqualfierDescription">' + object.disqualifierDescription + '</td>' +
    '<td contenteditable=false title="cost">' + object.cost + '</td>' +
    '<td contenteditable=false title="notes" >' + object.notes + '</td>' +
    '<td contenteditable=false title="facility" >' + object.facility + '</td>';
    table.appendChild(tr);
    tr.setAttribute("id",'cur_row'+cur_row.toString());
    // TODO : might not need class = can_updt
    tr.setAttribute("class", "can_updt");
    cur_row++;
  });
}

function editbtn(cur_row){

  origInfo={}
  var edit_cells = document.getElementById('cur_row'+cur_row).getElementsByTagName('td');
  var parent = document.getElementById('cur_row'+cur_row);
  var child = parent.getElementsByTagName('td')[0];
  for (var i=1; i<edit_cells.length; i++){
    var cur_cell = edit_cells[i];
    cur_cell.setAttribute('contenteditable', 'true');
    origInfo[cur_cell.getAttribute("title")]=cur_cell.innerHTML;
  }

  localStorage.setItem("origInfo",JSON.stringify(origInfo));
  child.remove();

  var cell = document.createElement('td');
  var para = document.createElement("button");
  para.innerHTML='save';
  para.setAttribute('class','savebtn');
  para.setAttribute('onclick', 'savebtn('+cur_row.toString()+');');
  cell.appendChild(para);

  var new_child = parent.getElementsByTagName('td')[0];
  console.log(new_child.innerHTML);
  parent.insertBefore(cell, new_child);
}

function savebtn(cur_row){
  // TODO : CHANGE THE ACTUAL DATABASE
  var newInfo={};
  var queryStrings=[];
  var addQueryStrings=[];
  var edit_cells = document.getElementById('cur_row'+cur_row).getElementsByTagName('td');
  var parent = document.getElementById('cur_row'+cur_row);
  var child = parent.getElementsByTagName('td')[0];
  for (var i=1; i<edit_cells.length; i++){
    var cur_cell=edit_cells[i];
    cur_cell.setAttribute('contenteditable', 'false');
    newInfo[cur_cell.getAttribute("title")]=cur_cell.innerHTML;
  }
  child.remove();
  var origInfo = JSON.parse(localStorage.getItem("origInfo"));
  console.log(origInfo);

  for (var key in newInfo){
    addQueryStrings.push(key+"="+newInfo[key]+"&");
  }
  console.log("addQueryString -> " + addQueryStrings);
  for (var key in origInfo){
    queryStrings.push(key+"="+origInfo[key]+"&");
  }
  console.log("queryString -> " + queryStrings);

  var add_query = "";
  for (var i=0; i<addQueryStrings.length; i++){
    var str = addQueryStrings[i];
    add_query = add_query+str;
  }
  var base_query = "";
  for (var i=0; i<queryStrings.length; i++){
    var str = queryStrings[i];
    base_query = base_query+str;
  }

  var add_url = getBaseApiURL()+"/vd_add_entry?"+add_query.substring(0,add_query.length - 1);
  var del_url = getBaseApiURL()+"/delete_entry?"+base_query.substring(0,base_query.length - 1);
  console.log("add_url -> " + add_url);
  console.log("delete_url ->" + del_url);

  fetch(add_url)
    .then(res => res.text())
    //.then(res => res.json())
    .then((out) => {
      console.log(out);
      return out;})
    .catch(err => { throw err });

  var success=false;

  // TODO : try to make it so can catch errors here?

  fetch(del_url)
    //.then(res => res.json())
    .then(res => res.text())
    .then((out) => {
      console.log(out);
    })
    .catch(err => { throw err });

  var cell = document.createElement('td');
  var para = document.createElement("button");
  para.innerHTML='edit';
  para.setAttribute('class','editbtn');
  para.setAttribute('onclick', 'editbtn('+cur_row.toString()+');');
  cell.appendChild(para);

  var new_child = parent.getElementsByTagName('td')[0];
  parent.insertBefore(cell, new_child);
}

function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;

    // CSV file
    csvFile = new Blob([csv], {type: "text/csv"});

    // Download link
    downloadLink = document.createElement("a");

    // File name
    downloadLink.download = filename;

    // Create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);

    // Hide download link
    downloadLink.style.display = "none";

    // Add the link to DOM
    document.body.appendChild(downloadLink);

    // Click download link
    downloadLink.click();
}

function exportTableToCSV(filename) {
    var csv = [];
    var rows = document.querySelectorAll("table tr");

    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");

        for (var j = 1; j < cols.length; j++)
            row.push('"'+cols[j].innerText+'"');

        csv.push(row.join(","));
    }

    // Download CSV file
    /*var csv = new TableExport(document.getElementById("results"));*/
    downloadCSV(csv.join("\n"), filename);
}
