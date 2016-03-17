/* 
 * Author:          Jessica Lynch
 * Date:            10-Mar-2016
 * Description:     Create bar chart to display data from tsv file.
 */

function displayTsvData( source )
{   
    var margin = {top: 80, right: 20, bottom: 30, left: 80},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(10);

    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    //legend  
    var colors =	[ ["Item 1", "#377EB8"],
                      ["Item 2", "#4DAF4A"],
                      ["Item 3", "#FA1F4F"],
                      ["Item 4", "#FFCF00"] ];

    //var horizontalLegend = d3.svg.legend()
    //                     .labelFormat("none")
    //                     .cellPadding(5)
    //                     .orientation("horizontal")
    //                     .units("quantity")
    //                     .cellWidth(25)
    //                     .cellHeight(18)
    //                     .inputScale(x)
    //                     .cellStepping(10);
    var legend = svg.append("g")
                    .attr("class", "legend")
                    .attr("height", 100)
                    .attr("width", 100)
                    .attr('transform', 'translate(-20,50)');
      //              .call(horizontalLegend);

    var legendRect = legend.selectAll('rect').data(colors);

    var legendText = legend.selectAll('text').data(colors);


    d3.tsv(source, type, function(error, data) {
      if (error) throw error;

      x.domain(data.map(function(d) { return d.letter; }));
      y.domain([0, d3.max(data, function(d) { return d.frequency; })]);

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
          .append("text")
          .attr("x",-200)
          //.attr("y",-1000)
          .attr("transform", "rotate(-90)")
          //.attr("transform", "translate(-30,200)")//"rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Frequency");

      svg.selectAll(".bar")
          .data(data)
          .enter().append("rect")
          .attr("class", "bar") 
          .attr("x", function(d) { return x(d.letter); })
          .attr("width", x.rangeBand())
          .attr("y", function(d) { return y(d.frequency); })
          .attr("height", function(d) { return height - y(d.frequency); });
    });

    //legend
    legendRect.enter()
          .append("rect")
          .attr("x", width - 65)
          .attr("width", 10)
          .attr("height", 10);

    legendRect
          .attr("y", function(d, i) { return i * 20; })
          .style("fill", function(d) { return d[1]; });

    legendText.enter()
          .append("text")
          .attr("x", width - 52);

    legendText
          .attr("y", function(d, i) { return i * 20 + 9; })
          .text(function(d) { return d[0]; });
}

function type(d) {
  d.frequency = +d.frequency;
  return d;
}