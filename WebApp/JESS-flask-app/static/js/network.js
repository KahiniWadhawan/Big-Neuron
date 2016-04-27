var width = window.innerWidth,
    height = window.innerHeight;

var svg = d3.select("#network").append("svg")
    .attr("width", width)
    .attr("height", height);

var force = d3.layout.force()
    .gravity(0.05)
    .distance(100)
    .charge(-100)
    .size([width, height]);

function show(user){
d3.json("static/data/"+ user + "_network.json", function(json) {

  console.log(json)
  console.log("static/data/"+ user + "_network.json")

  force
      .nodes(json.nodes)
      .links(json.links)
      .start();

  var link = svg.selectAll(".link")
      .data(json.links)
    .enter().append("line")
      .attr("class", "link");

  //var border=10;
  //var bordercolor='black';
  var node = svg.selectAll(".node")
      .data(json.nodes)
    .enter().append("g")
      .attr("class", "node")
      .call(force.drag);

  /*node.append("text")
      .attr("dx", 12)
      .attr("dy", ".35em")
      .text(function(d) { return d.name });
  */

  node.append("image")
      //.attr("xlink:href", "https://github.com/favicon.ico")
      .attr("xlink:href", function(d) { return d.profile_image_url; })
     /*.attr("xlink:href", function(d) {
       var rnd = Math.floor(Math.random() * 64 + 1);
       var imagePath = "http://www.bigbiz.com/bigbiz/icons/ultimate/Comic/Comic"
           + rnd.toString() + ".gif";
       console.Log(imagePath);
      return imagePath;
      })*/
      .attr("x", -8)
      .attr("y", -8)
      .attr("width", 18)
      .attr("height", 18);
      //.style("stroke", bordercolor)
      //.style("stroke-width", border);


  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  });
}); 
}//end of show