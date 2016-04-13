//render the cloud with animations
     function draw(words) {

        //render new tag cloud
        d3.select("body").selectAll("svg")
            .append("g")
                 .attr("transform", "translate(300,300)")
                .selectAll("text")
                .data(words)
            .enter().append("text")
            .style("font-size", function(d) { return ((d.size)* 1) + "px"; })
            .style("font-family", "Impact")
            .style("fill", function(d, i) { return fill(i); })
            .style("opacity", 1e-6)
            .attr("text-anchor", "middle")
            .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
            .transition()
            .duration(1000)
            .style("opacity", 1)
            .text(function(d) { return d.text; });