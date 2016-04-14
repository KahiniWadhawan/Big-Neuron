var fontSize = d3.scale.log().range([10, 90]);

    //create my cloud object
    var mycloud = d3.layout.cloud().size([600, 600])
          .words([])
          .padding(2)
          .rotate(function() { return ~~(Math.random() * 2) * 90; })
          .font("Impact")
          .fontSize(function(d) { return fontSize(d.size); })
          .on("end", draw)