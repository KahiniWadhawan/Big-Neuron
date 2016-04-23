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
// This function calls the update function on window click
window.onclick = function(event) {

            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (xhttp.readyState == 4 && xhttp.status == 200) {
                  var temp= xhttp.responseText
                  tags= eval(temp)
                }
              };
            xhttp.open("GET", "/static/data.json?something="+(Math.random()*10).toString(), true);
            xhttp.send();
     

    update();
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
    console.log("scale = "+scale)
    var text = vis.selectAll("text")
            .data(data, function(d) {
                return d.text.toLowerCase();
            });
    text.transition()
            .duration(2000)
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
    text.exit.remove();
}

// This function is responsible for pulling the updated JSON file from the server.
function update() {
    console.log("tags.length"+tags.length)
    console.log("word-cloud"+tags)
    layout.font('impact').spiral('archimedean');
    fontSize = d3.scale['sqrt']().range([30,70]);   //This is to change the range of font size
    console.log("fontSize = "+fontSize)
    if (tags.length){
        fontSize.domain([+tags[tags.length - 1].value || 1, +tags[0].value]);
    }
    layout.stop().words(tags).start();
}
