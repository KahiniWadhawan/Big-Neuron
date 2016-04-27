//http://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_onclick_win
var fill = d3.scale.category20b();
var w = window.innerWidth,h = window.innerHeight;
var max,fontSize;
var layout = d3.layout.cloud()
        .timeInterval(1)
        .size([w, h])
        .fontSize(function(d) {
            return fontSize(+d.value);
        })
        .text(function(d) {
            return d.key;
        })
        .on("end", draw);

//vis covers the whole screen
var svg = d3.select("#vis").append("svg")
        .attr("width", w)
        .attr("height", h);

var vis = svg.append("g").attr("transform", "translate(" + [w >> 1, h >> 1] + ")");

//update();
var tags="Dummy"
var chart;

var chartData1 = 
            [
                {
                    "year": 2000,
                    "income": 1
                },
                {
                    "year": 2006,
                    "income": 1
                },
                {
                    "year": 2007,
                    "income": 1
                },
                {
                    "year": 2008,
                    "income": 1
                },
                {
                    "year": 2009,
                    "income": 1
                }
            ];

var chartData2 = 
            [
                {
                    "year": 2000,
                    "income": 1
                },
                {
                    "year": 2006,
                    "income": 1
                },
                {
                    "year": 2007,
                    "income": 1
                },
                {
                    "year": 2008,
                    "income": 1
                },
                {
                    "year": 2009,
                    "income": 1
                }
            ];
var chartData3 = 
            [
                {
                    "year": 2000,
                    "income": 1
                },
                {
                    "year": 2006,
                    "income": 1
                },
                {
                    "year": 2007,
                    "income": 1
                },
                {
                    "year": 2008,
                    "income": 1
                },
                {
                    "year": 2009,
                    "income": 1
                }
            ];

// This function calls the update function on window click
window.onclick = function(event) {

            var xhttp = new XMLHttpRequest();
            var xhttp1 = new XMLHttpRequest();
            var xhttp2 = new XMLHttpRequest();
            var xhttp3 = new XMLHttpRequest();



            xhttp.onreadystatechange = function() {
                if (xhttp.readyState == 4 && xhttp.status == 200) {
                  var temp= xhttp.responseText
                  tags= eval(temp)
                }
              };

            xhttp1.onreadystatechange = function() {
            if (xhttp1.readyState == 4 && xhttp1.status == 200) {
                var temp1=xhttp1.responseText
                chartData1 = eval(temp1)

            }
          };

          xhttp2.onreadystatechange = function() {
            if (xhttp2.readyState == 4 && xhttp2.status == 200) {
                var temp2=xhttp2.responseText
                chartData2 = eval(temp2)

            }
          };


          xhttp3.onreadystatechange = function() {
            if (xhttp3.readyState == 4 && xhttp3.status == 200) {
                var temp3=xhttp3.responseText
                chartData3 = eval(temp3)

            }
          };


            xhttp.open("GET", "/static/data.json?something="+(Math.random()*10).toString(), true);
            xhttp1.open("GET", "/static/testdata1.json?something="+(Math.random()*10).toString(), true);
            xhttp2.open("GET", "/static/testdata2.json?something="+(Math.random()*10).toString(), true);
            xhttp3.open("GET", "/static/testdata3.json?something="+(Math.random()*10).toString(), true);



            xhttp.send();
            xhttp1.send();
            xhttp2.send();
            xhttp3.send();




     

    update();
    update1();
    update2();
    update3();

};



//This function is related with the transition of the text on clicking the window.
function draw(data, bounds) {
    var w = window.innerWidth,
        h = window.innerHeight;

    svg.attr("width", w).attr("height", h);

    scale = bounds ? Math.min(
            w / Math.abs(bounds[1].x - w / 2),
            w / Math.abs(bounds[0].x - w / 2),
            h / Math.abs(bounds[1].y - h / 2),
            h / Math.abs(bounds[0].y - h / 2)) / 2 : 1;
    //console.log("scale = "+scale)
    var text = vis.selectAll("text")
            .data(data, function(d) {
                return d.text.toLowerCase();
            });
    text.transition()
            .duration(2500)
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .style("font-size", function(d) {
                return d.size + "px";
            });
    text.enter().append("text")
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .style("font-size", function(d) {
                return d.size + "px";
            })
            .style("opacity", 1e-6)
            .transition()
            .duration(2000)
            .style("opacity", 1);
    text.style("font-family", function(d) {
        return d.font;
    })
            .style("fill", function(d) {
                return fill(d.text.toLowerCase());
            })
            .text(function(d) {
                return d.text;
            });

    vis.transition().attr("transform", "translate(" + [w >> 1, h >> 1] + ")scale(" + scale + ")");
    text.exit().remove();
}

// This function is responsible for pulling the updated JSON file from the server.
function update() {
    //console.log("tags.length"+tags.length)
    //console.log("word-cloud"+tags)
    layout.font('impact').spiral('rectangular');
    fontSize = d3.scale['sqrt']().range([30,70]);   //This is to change the range of font size
    //console.log("fontSize = "+fontSize)
    if (tags.length){
        fontSize.domain([+tags[tags.length - 1].value || 1, +tags[0].value]);
    }
    layout.stop().words(tags).start();
}

function update1() {
                // SERIAL CHART
                chart = new AmCharts.AmSerialChart();
                chart.dataProvider = chartData1;
                chart.categoryField = "year";
                // this single line makes the chart a bar chart,
                // try to set it to false - your bars will turn to columns
                chart.rotate = true;
                // the following two lines makes chart 3D
                chart.depth3D = 20;
                chart.angle = 30;

                // AXES
                // Category
                var categoryAxis = chart.categoryAxis;
                categoryAxis.gridPosition = "start";
                categoryAxis.axisColor = "#DADADA";
                categoryAxis.fillAlpha = 1;
                categoryAxis.gridAlpha = 0;
                categoryAxis.fillColor = "#FAFAFA";

                // value
                var valueAxis = new AmCharts.ValueAxis();
                valueAxis.axisColor = "#DADADA";
                valueAxis.title = "Income in millions, USD";
                valueAxis.gridAlpha = 0.1;
                chart.addValueAxis(valueAxis);

                // GRAPH
                var graph = new AmCharts.AmGraph();
                graph.title = "Income";
                graph.valueField = "income";
                graph.type = "column";
                graph.balloonText = "Income in [[category]]:[[value]]";
                graph.lineAlpha = 0;
                graph.fillColors = "#bf1c25";
                graph.fillAlphas = 1;
                chart.addGraph(graph);

                chart.creditsPosition = "top-right";

                // WRITE
                chart.write("chartdiv1");
        
    }
function update2() {
                // SERIAL CHART
                chart = new AmCharts.AmSerialChart();
                chart.dataProvider = chartData2;
                chart.categoryField = "year";
                // this single line makes the chart a bar chart,
                // try to set it to false - your bars will turn to columns
                chart.rotate = true;
                // the following two lines makes chart 3D
                chart.depth3D = 20;
                chart.angle = 30;

                // AXES
                // Category
                var categoryAxis = chart.categoryAxis;
                categoryAxis.gridPosition = "start";
                categoryAxis.axisColor = "#DADADA";
                categoryAxis.fillAlpha = 1;
                categoryAxis.gridAlpha = 0;
                categoryAxis.fillColor = "#FAFAFA";

                // value
                var valueAxis = new AmCharts.ValueAxis();
                valueAxis.axisColor = "#DADADA";
                valueAxis.title = "Income in millions, USD";
                valueAxis.gridAlpha = 0.1;
                chart.addValueAxis(valueAxis);

                // GRAPH
                var graph = new AmCharts.AmGraph();
                graph.title = "Income";
                graph.valueField = "income";
                graph.type = "column";
                graph.balloonText = "Income in [[category]]:[[value]]";
                graph.lineAlpha = 0;
                graph.fillColors = "#bf1c25";
                graph.fillAlphas = 1;
                chart.addGraph(graph);

                chart.creditsPosition = "top-right";

                // WRITE
                chart.write("chartdiv2");
        
}

function update3() {
                // SERIAL CHART
                chart = new AmCharts.AmSerialChart();
                chart.dataProvider = chartData3;
                chart.categoryField = "year";
                // this single line makes the chart a bar chart,
                // try to set it to false - your bars will turn to columns
                chart.rotate = true;
                // the following two lines makes chart 3D
                chart.depth3D = 20;
                chart.angle = 30;

                // AXES
                // Category
                var categoryAxis = chart.categoryAxis;
                categoryAxis.gridPosition = "start";
                categoryAxis.axisColor = "#DADADA";
                categoryAxis.fillAlpha = 1;
                categoryAxis.gridAlpha = 0;
                categoryAxis.fillColor = "#FAFAFA";

                // value
                var valueAxis = new AmCharts.ValueAxis();
                valueAxis.axisColor = "#DADADA";
                valueAxis.title = "Income in millions, USD";
                valueAxis.gridAlpha = 0.1;
                chart.addValueAxis(valueAxis);

                // GRAPH
                var graph = new AmCharts.AmGraph();
                graph.title = "Income";
                graph.valueField = "income";
                graph.type = "column";
                graph.balloonText = "Income in [[category]]:[[value]]";
                graph.lineAlpha = 0;
                graph.fillColors = "#bf1c25";
                graph.fillAlphas = 1;
                chart.addGraph(graph);

                chart.creditsPosition = "top-right";

                // WRITE
                chart.write("chartdiv3");
        
    
}
