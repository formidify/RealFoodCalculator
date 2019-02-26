/// visualization.js: javascript file corresponding to the html
// author: RFC comps group 18'

// global defaults and function
Chart.defaults.global.plugins.datalabels.display = false

 // Hash any string into an integer value
// Then we'll use the int and convert to hex.
function hashCode(str) {
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
}

// Convert an int to hexadecimal with a max length
// of six characters.
function intToARGB(i) {
    var hex = ((i>>24)&0xFF).toString(16) +
            ((i>>16)&0xFF).toString(16) +
            ((i>>8)&0xFF).toString(16) +
            (i&0xFF).toString(16);
    // Sometimes the string returned will be too short so we 
    // add zeros to pad it out, which later get removed if
    // the length is greater than six.
    hex += '000000';
    return hex.substring(0, 6);
}

function arraysEqual(arr1, arr2) {
    if(arr1.length !== arr2.length)
        return false;
    for(var i = arr1.length; i--;) {
        if(arr1[i] !== arr2[i])
            return false;
    }

    return true;
}


/// QUICK CHARTS
divs = ["realCatChart", "nonCatChart", "realItemChart", "nonItemChart", 
        "realVendChart", "nonVendChart", "realBrandChart", "nonBrandChart"]

groups = ['category', 'description', 'vendor', 'label_brand']
type = ['real', 'nonreal']
background = ["rgba(255, 159, 64, 0.2)", "rgba(54, 162, 235, 0.2)"]
border = ["rgba(255, 159, 64)", "rgba(54, 162, 235)"]

prefix = "Top 5 "
title_parts = ['categories', 'items', 'vendors', 'labels/brands']

getData = $.get('http://cmc307-06.mathcs.carleton.edu:5001/visualization/quick_data')
getData.done(function(results) {
  year = results.year
for (i = 0; i < 4; i++) {
  for (j = 0; j < 2; j++) {

    key = groups[i] + ":" + type[j]
    labels = results[key].labels
    cost = results[key].cost


  data = {
      datasets: [{
          label: "Purchase in dollars",
          data: cost,
          borderWidth: 2,
          backgroundColor: background[j],
          borderColor: border[j]
      }],
      // These labels appear in the legend and in the tooltips when hovering different arcs
      labels: labels,
      options: {
          responsive: true
      }
  };
  title = prefix + title_parts[i] + " " + year + " in " + type[j] + " food"
  ctx = document.getElementById(divs[2*i + j]).getContext('2d');
  quickBarChart = new Chart(ctx, {
      type: 'bar',
      data: data,
      options: {
        title: {
              display: true,
              text: title
          },
          scales: {
          xAxes: [{
            ticks: {
              autoSkip: false
            }
          }]
      }
  }});

  }
}
});


/// TODO: implement move up and down 1 year at a time buttons

let num_items = document.querySelector('#num_items_percent');
let rank = document.querySelector('#rank_percent');

// manually added items
var new_real = [];
var new_nonreal = [];
var new_label = [];



/// PERCENT CHARTS
getData = $.get('http://cmc307-06.mathcs.carleton.edu:5001/visualization/pie_data')

getData.done(function(results) {
    years = results.labels
    // year 1
    yr = years[0]
    result = results[yr]
    data = {
        datasets: [{
            data: result.data,
            backgroundColor: palette('tol', result.data.length).map(function(hex) {
            return '#' + hex;
          })
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: result.labels,
        options: {
            responsive: true
        }
    };

     ctx1 = document.getElementById("percentChart1").getContext('2d');
    var myPieChart1 = new Chart(ctx1, {
        type: 'pie',
        data: data ,
        options: {
          title: {
              display: true,
              position: 'bottom',
              text: yr
          }
      }
    });


    // year 2
    yr = years[1]
    result = results[yr]
    data = {
        datasets: [{
            data: result.data,
            backgroundColor: palette('tol', result.data.length).map(function(hex) {
            return '#' + hex;
          })
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: result.labels,
        options: {
            responsive: true
        }
    };

     ctx6 = document.getElementById("percentChart3").getContext('2d');
    var myPieChart2 = new Chart(ctx6, {
        type: 'pie',
        data: data ,
        options: {
          title: {
              display: true,
              position: 'bottom',
              text: yr
          }
      }
    });


    // year 3
    yr = years[2]
    result = results[yr]
    data = {
        datasets: [{
            data: result.data,
            backgroundColor: palette('tol', result.data.length).map(function(hex) {
            return '#' + hex;
          })
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: result.labels,
        options: {
            responsive: true
        }
    };

     ctx7 = document.getElementById("percentChart4").getContext('2d');
    var myPieChart3 = new Chart(ctx7, {
        type: 'pie',
        data: data ,
        options: {
          title: {
              display: true,
              position: 'bottom',
              text: yr
          }
      }
    });


    // total
    yr = years[3]
    result = results.total
    data = {
        datasets: [{
            data: result.data,
            backgroundColor: palette('tol', result.data.length).map(function(hex) {
            return '#' + hex;
          })
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: result.labels,
        options: {
            responsive: true
        }
    };

     ctx8 = document.getElementById("percentChart5").getContext('2d');
    var myPieChart4 = new Chart(ctx8, {
        type: 'pie',
        data: data ,
        options: {
          title: {
              display: true,
              position: 'bottom',
              text: yr
          }
      }
    });
})

 barData = $.get('http://cmc307-06.mathcs.carleton.edu:5001/visualization/bar_data/produce+total')
 var myBarChart;

barData.done(function(results) {
  // bar plot
   items = results.items // food items
   real_color = Array(items.length).fill('rgba(255, 99, 132, 0.2)')
   nonreal_color = Array(items.length).fill('rgba(255, 159, 64, 0.2)')

   real_border_color = Array(items.length).fill('rgba(255,99,132,1)')
   nonreal_border_color = Array(items.length).fill('rgba(255, 159, 64, 1)')

  data = {
      datasets: [{
          label: "real",
          data: results.real,
          borderWidth: 2,
          backgroundColor: real_color,
          borderColor: real_border_color
      },
      {
          label: "non-real",
          data: results.nonreal,
          borderWidth: 2,
          backgroundColor: nonreal_color,
          borderColor: nonreal_border_color
        }
      ],
      // These labels appear in the legend and in the tooltips when hovering different arcs
      labels: items,
      options: {
          responsive: true
      }
  };

   ctx2 = document.getElementById("percentChart2").getContext('2d');
  myBarChart = new Chart(ctx2, {
      type: 'bar',
      data: data,
      options: {
          scales: {
              xAxes: [{
                  stacked: true
              }],
              yAxes: [{
                  stacked: true
              }]},
              title: {
              display: true,
              text: "Purchase for total produce"
          }

      }
  });
})

// update bar chart
function updateBarChart(cat, yr){
   updatedData = $.get("http://cmc307-06.mathcs.carleton.edu:5001/visualization/bar_data/" + cat + "+" + yr);
  updatedData.done(function(results) {
   real_color = Array(results.items.length).fill('rgba(255, 99, 132, 0.2)')
   nonreal_color = Array(results.items.length).fill('rgba(255, 159, 64, 0.2)')

   real_border_color = Array(results.items.length).fill('rgba(255,99,132,1)')
   nonreal_border_color = Array(results.items.length).fill('rgba(255, 159, 64, 1)')

  data = {
      datasets: [{
          label: "real",
          data: results.real,
          borderWidth: 2,
          backgroundColor: real_color,
          borderColor: real_border_color
      },
      {
          label: "non-real",
          data: results.nonreal,
          borderWidth: 2,
          backgroundColor: nonreal_color,
          borderColor: nonreal_border_color
        }
      ],
      // These labels appear in the legend and in the tooltips when hovering different arcs
      labels: results.items,
      options: {
          responsive: true
      }
  };

  myBarChart.data = data;
  myBarChart.options.title.text = yr + " purchase of " + cat;

  myBarChart.update();
    })
}

function pc1click(evt)
{
     activePoints = myPieChart1.getElementsAtEvent(evt);

    if(activePoints.length > 0)
    {
      //get the internal index of slice in pie chart
       clickedElementindex = activePoints[0]["_index"];

      //get specific label by index
       label = myPieChart1.data.labels[clickedElementindex];

      //get value by index
       value = myPieChart1.data.datasets[0].data[clickedElementindex];

       year = years[0];

      updateBarChart(label, year);
   }
}

document.getElementById("percentChart3").onclick = function(evt)
{
     activePoints = myPieChart2.getElementsAtEvent(evt);

    if(activePoints.length > 0)
    {
      //get the internal index of slice in pie chart
       clickedElementindex = activePoints[0]["_index"];

      //get specific label by index
       label = myPieChart2.data.labels[clickedElementindex];

      //get value by index
       value = myPieChart2.data.datasets[0].data[clickedElementindex];

       year = years[1];

      updateBarChart(label, year);
   }
}

document.getElementById("percentChart4").onclick = function(evt)
{
     activePoints = myPieChart3.getElementsAtEvent(evt);

    if(activePoints.length > 0)
    {
      //get the internal index of slice in pie chart
       clickedElementindex = activePoints[0]["_index"];

      //get specific label by index
       label = myPieChart3.data.labels[clickedElementindex];

      //get value by index
       value = myPieChart3.data.datasets[0].data[clickedElementindex];

       year = years[2];

      updateBarChart(label, year);
   }
}

document.getElementById("percentChart5").onclick = function(evt)
{
     activePoints = myPieChart4.getElementsAtEvent(evt);

    if(activePoints.length > 0)
    {
      //get the internal index of slice in pie chart
       clickedElementindex = activePoints[0]["_index"];

      //get specific label by index
       label = myPieChart4.data.labels[clickedElementindex];

      //get value by index
       value = myPieChart4.data.datasets[0].data[clickedElementindex];

       year = years[3];

      updateBarChart(label, year);
   }
}

/// HYPOTHETICAL INCREASE CHART

Chart.Legend.prototype.afterFit = function() {
    this.height = this.height + 20;
};
// pie chart
// load data from Flask; shows all categories
 getData = $.get('http://cmc307-06.mathcs.carleton.edu:5001/visualization/pie_data')

getData.done(function(results) {
    years = results.labels
    // year 1
    yr = years[0]
    result = results[yr]
    data = {
        datasets: [{
            data: result.data,
            backgroundColor: palette('tol', result.data.length).map(function(hex) {
            return '#' + hex;
          })
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: result.labels,
        options: {
            responsive: true
        }
    };

     ctx1 = document.getElementById("increaseChart1").getContext('2d');
    myPieChart1 = new Chart(ctx1, {
        type: 'pie',
        data: data ,
        options: {
          title: {
              display: true,
              position: 'bottom',
              text: yr
          }
      }
    });


    // year 2
    yr = years[1]
    result = results[yr]
    data = {
        datasets: [{
            data: result.data,
            backgroundColor: palette('tol', result.data.length).map(function(hex) {
            return '#' + hex;
          })
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: result.labels,
        options: {
            responsive: true
        }
    };

     ctx6 = document.getElementById("increaseChart3").getContext('2d');
    myPieChart2 = new Chart(ctx6, {
        type: 'pie',
        data: data ,
        options: {
          title: {
              display: true,
              position: 'bottom',
              text: yr
          }
      }
    });


    // year 3
    yr = years[2]
    result = results[yr]
    data = {
        datasets: [{
            data: result.data,
            backgroundColor: palette('tol', result.data.length).map(function(hex) {
            return '#' + hex;
          })
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: result.labels,
        options: {
            responsive: true
        }
    };

     ctx7 = document.getElementById("increaseChart4").getContext('2d');
    myPieChart3 = new Chart(ctx7, {
        type: 'pie',
        data: data ,
        options: {
          title: {
              display: true,
              position: 'bottom',
              text: yr
          }
      }
    });


    // total
    yr = years[3]
    result = results.total
    data = {
        datasets: [{
            data: result.data,
            backgroundColor: palette('tol', result.data.length).map(function(hex) {
            return '#' + hex;
          })
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: result.labels,
        options: {
            responsive: true
        }
    };

     ctx8 = document.getElementById("increaseChart5").getContext('2d');
    myPieChart4 = new Chart(ctx8, {
        type: 'pie',
        data: data ,
        options: {
          title: {
              display: true,
              position: 'bottom',
              text: yr
          }
      }
    });
})

 lineData = $.get('http://cmc307-06.mathcs.carleton.edu:5001/visualization/percent_data/produce+total')
 var mixedChart;

lineData.done(function(results) {
   ctx4 = document.getElementById("increaseChart2").getContext('2d');
   mixedChart = new Chart(ctx4, {
    type: 'bar',
    data: {
      datasets: [{
            type: "bar",
            label: 'Increase in dollar amount',
            data: results['dollars'],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            yAxisID: "bar",
            datalabels: {
            // display labels for this specific dataset
            display: true,
            anchor: 'center'
          }}, {
            label: 'Percent increase in single item',
            data: results['ind_percent'],
            yAxisID: "A",
            type: 'line',
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              borderColor: 'rgba(255,99,132,1)',
              fill: false
          }, {
            label: 'Percent increase for all purchases',
            data: results['total_percent'],
            yAxisID: "B",
            type: 'line',
          backgroundColor: 'rgba(75, 00, 1300, 0.2)',
          borderColor: 'rgba(75, 00, 1300,1)',
          fill: false
          }],
      labels: results['items']
    },
    options: {
      title: {
        display: true,
        text: "Hypothetical Increase for total produce"
      },
      scales: {
        yAxes: [{
          id: 'A',
          type: 'linear',
          position: 'left',
          ticks: {
            fontColor: 'rgba(255,99,132,1)',
            max: 100.5,
            min: -0.5,
            stepSize: 10,
            callback: function(value, index, values) {
                           if (value !== 100.5 && value != -0.5) {
                               return values[index]
                           }
                       }
          },
            scaleLabel: {
            display: true,
            labelString: 'Percent increase in single item (%)'
          }
        }, {
          id: 'B',
          type: 'linear',
          position: 'right',
          ticks: {
            fontColor: 'rgba(75, 00, 1300,1)',
            beginAtZero: true
          },
            scaleLabel: {
            display: true,
            labelString: 'Percent increase for all purchases (%)'
          }
        }, {
          id: 'bar',
          type: 'linear',
          display: false,
          ticks: {
            beginAtZero: true
          }
        }],
        plugins: {
          datalabels: {
             display: false,
             font: {weight: 'bold'},
             align: 'center',
             anchor: 'center',
             clamp: true
          }

        }
      }
    }
})});

function updateMixedChart(cat, yr){
   updatedData = $.get("http://cmc307-06.mathcs.carleton.edu:5001/visualization/percent_data/" + cat + "+" + yr);
  updatedData.done(function(results) {

  data = {
      datasets: [{
            type: "bar",
            label: 'Increase in dollar amount (non-real $ amount of item)',
            data: results['dollars'],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            yAxisID: "bar",
            datalabels: {
            // display labels for this specific dataset
            display: true,
            anchor: 'center'
          }}, {
            label: 'Percent increase in single item',
            data: results['ind_percent'],
            yAxisID: "A",
            type: 'line',
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              borderColor: 'rgba(255,99,132,1)',
              fill: false
          }, {
            label: 'Percent increase for all purchases',
            data: results['total_percent'],
            yAxisID: "B",
            type: 'line',
          backgroundColor: 'rgba(75, 00, 1300, 0.2)',
          borderColor: 'rgba(75, 00, 1300,1)',
          fill: false
          }],
      labels: results['items']
    };

  mixedChart.data = data;
  mixedChart.options.title.text = "Hypothetical Increase for " + yr + " " + cat;

  mixedChart.update();
    });
};

document.getElementById("increaseChart1").onclick = function(evt)
{
     activePoints = myPieChart1.getElementsAtEvent(evt);

    if(activePoints.length > 0)
    {
      //get the internal index of slice in pie chart
       clickedElementindex = activePoints[0]["_index"];

      //get specific label by index
       label = myPieChart1.data.labels[clickedElementindex];

      //get value by index
       value = myPieChart1.data.datasets[0].data[clickedElementindex];

       year = years[0];

      updateMixedChart(label, year);
   }
}

document.getElementById("increaseChart3").onclick = function(evt)
{
     activePoints = myPieChart2.getElementsAtEvent(evt);

    if(activePoints.length > 0)
    {
      //get the internal index of slice in pie chart
       clickedElementindex = activePoints[0]["_index"];

      //get specific label by index
       label = myPieChart2.data.labels[clickedElementindex];

      //get value by index
       value = myPieChart2.data.datasets[0].data[clickedElementindex];

       year = years[1];

      updateMixedChart(label, year);
   }
}

document.getElementById("increaseChart4").onclick = function(evt)
{
     activePoints = myPieChart3.getElementsAtEvent(evt);

    if(activePoints.length > 0)
    {
      //get the internal index of slice in pie chart
       clickedElementindex = activePoints[0]["_index"];

      //get specific label by index
       label = myPieChart3.data.labels[clickedElementindex];

      //get value by index
       value = myPieChart3.data.datasets[0].data[clickedElementindex];

       year = years[2];

      updateMixedChart(label, year);
   }
}

document.getElementById("increaseChart5").onclick = function(evt)
{
     activePoints = myPieChart4.getElementsAtEvent(evt);

    if(activePoints.length > 0)
    {
      //get the internal index of slice in pie chart
       clickedElementindex = activePoints[0]["_index"];

      //get specific label by index
       label = myPieChart4.data.labels[clickedElementindex];

      //get value by index
       value = myPieChart4.data.datasets[0].data[clickedElementindex];

       year = years[3];

      updateMixedChart(label, year);
   }
}

/// TIME SERIES CHART

var searches_time = [];
//var select = document.getElementById("categoeis");
c = $.get("http://cmc307-06.mathcs.carleton.edu:5001/visualization/get_categories/");

c.done(function(results) {
  cats = results.cats;
  for (i = 0; i < cats.length; i++) {
    cat = cats[i]
    $("select#categories").append( $("<option>")
    .val(cat)
    .html(cat)
);
  }
});

sessionStorage.setItem("timeSearch", JSON.stringify([]));
sessionStorage.setItem("timeCurrent", JSON.stringify([]));
sessionStorage.setItem("timeConfigs", JSON.stringify([]));

function searchItem() {
  x = document.getElementById("add_time").value;
  if (x.length > 1) {
  searches = $.get("http://cmc307-06.mathcs.carleton.edu:5001/visualization/get_item/" + x);

  old_searches = JSON.parse(sessionStorage.timeSearch);

    searches.done(function(results) {
    if (!arraysEqual(old_searches, results.search)) {
    sessionStorage.setItem("timeSearch", JSON.stringify(results.search));
      var dataList = $("#items_time");
        dataList.empty();
        if(results.search.length) {
          for(i=0; i<results.search.length; i++) {
            item = results.search[i];
            var opt = $("<option></option>").attr("value", item).attr("text", item);
            dataList.append(opt);
          }
        }
    }});
}
};

Chart.defaults.global.plugins.datalabels.display = false;

 types = ['total', 'real']
 dashes = [[0, 0], [10, 5]]

 lineChartData = {}
 lineChartData.datasets = []
// add legend for real vs non real
for (i = 0; i < types.length; i++) {
    line = {}
    line.data = 0 // arbitrary
    line.type = 'line'
    line.label = types[i]
    //line.backgroundColor = colors[i]
    if (i > 0) {
        line.borderDash = [10, 5]
    }
    line.fill = false
    line.showLine = false
    lineChartData.datasets.push(line)
}

var total_configs = JSON.parse(sessionStorage.timeConfigs)
var ctx5 = document.getElementById("timeSeriesChart").getContext('2d');
var myLineChart;
myLineChart = new Chart(ctx5, {data: lineChartData,
    type: 'line',
    options: {scales: {yAxes:[{scaleLabel: {display: true, labelString: "Dollar purchases ($)"}, ticks: {min: 0}}]},
              legend: {
                display: true,
                fill: false,
                labels: {
                  filter: function(legendItem, data) {
                  //return legendItem.datasetIndex >= total_configs.length
                  return !total_configs.includes(data.datasets[legendItem.datasetIndex].label)
                }
              }
              },
              responsive: true,
              maintainAspectRatio: false
  }
});

// add single item to the time series chart
function addItemData() {
  current_list = JSON.parse(sessionStorage.timeCurrent);
  y = document.getElementById("add_time").value;
  // check input is longer than 1 and has not appeared in current list
  if (y.length > 1 && !current_list.includes(y)) {
    searches = $.get("http://cmc307-06.mathcs.carleton.edu:5001/visualization/item_data/" + y + "+year");

    searches.done(function(results) {
      types = ['total', 'real']
      myLineChart.data.labels = results.yrs
      //datasets = []
      color = "#" + intToARGB(hashCode(y))

      cost = results.cost


total_configs = JSON.parse(sessionStorage.timeConfigs)

    for (j = 0; j < types.length; j++) {
        line = {}
        line.data = cost[j]
        line.type = 'line'
        line.label = types[j] + " " + y
        total_configs.push(line.label)
        //line.backgroundColor = colors[i]
        line.borderColor = color
        line.fill = false
        if (j > 0) {
            line.borderDash = [10, 5]
        }
        myLineChart.data.datasets.push(line)
    }
// console.log(datasets.toString())
// add legend for each item
    line = {}
    line.data = 0 // arbitrary
    line.type = 'line'
    line.label = y
    line.backgroundColor = color
    line.borderColor = color
    //line.fillColor = colors[i]
    line.fill = true
    line.showLine = false
    myLineChart.data.datasets.push(line)

  myLineChart.update();

sessionStorage.setItem("timeConfigs", JSON.stringify(total_configs));

    })

    sessionStorage.setItem("timeCurrent", JSON.stringify(current_list.concat([y])));
  }
}


function updateTimeChart(cat){
   updatedData = $.get("http://cmc307-06.mathcs.carleton.edu:5001/visualization/percent_data/" + cat);
  updatedData.done(function(results) {

lineChartData = {};
lineChartData.labels  = results.labels; // time frame
lineChartData.datasets = [];  //add 'datasets' array element to object

 items = results.item
 colors = palette('tol', items.length).map(function(hex) {
        return '#' + hex;
      })


 data = results.data

 //[[[304, 407, 529], [1777, 2378, 3454], [665, 798, 300, 200], [234, 567, 987], [111, 222, 333]], // total
//[[204, 40, 519], [1577, 2368, 3254], [635, 758, 20, 100], [134, 537, 947], [101, 202, 303]]] // real


total_configs = []

datasets = []
for (i = 0; i < items.length; i++) {
    for (j = 0; j < types.length; j++) {
        line = {}
        line.data = data[j][i]
        line.type = 'line'
        line.label = types[j] + " " + items[i]
        total_configs.push(line.label)
        //line.backgroundColor = colors[i]
        line.borderColor = colors[i]
        line.fill = false
        if (j > 0) {
            line.borderDash = [10, 5]
        }
        datasets.push(line)
    }
}

// add legend for each item
for (i = 0; i < items.length; i++) {
    line = {}
    line.data = 0 // arbitrary
    line.type = 'line'
    line.label = items[i]
    line.backgroundColor = colors[i]
    line.borderColor = colors[i]
    //line.fillColor = colors[i]
    line.fill = true
    line.showLine = false
    datasets.push(line)
}

lineChartData.datasets = datasets

  myLineChart.data =lineChartData;
  myLineChart.options.maintainAspectRatio = true;

  myLineChart.update();
    });
};


/// ITEM/LABEL/VENDOR CHARTS

function addItem() {

}

function addVendor() {

}

function addBrand() {

}
