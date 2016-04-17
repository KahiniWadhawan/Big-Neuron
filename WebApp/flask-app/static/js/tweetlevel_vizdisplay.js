/* 
 * Display tweet-level visualizations.
 */

function getAndPostData(input) {
    $.ajax({
        type: "GET, POST",
        url: "/amcharts_JSON.py",
        data: { param: input }
    });
}

function changeVisualization() {
    var labels = ["lbl0",  "lbl1",  "lbl2",  "lbl3",  "lbl4",  "lbl5",  "lbl6",  
                  "lbl7",  "lbl8",  "lbl9", "lbl10", "lbl11", "lbl12", "lbl13",
                  "lbl14", "lbl15", "lbl16", "lbl17", "lbl18", "lbl19"];

    var input = $('script[src*=../../../static/data/jess_test.json').attr('src');
    input = input.replace('example.js', '');
    var radios = document.getElementsByName( "optionsRadios" );
    if( radios === null )
    {
        alert( "Radios is null" );
    }
    for( var l = 0; l < labels.length; l++ )
    {
        var elmnt = document.getElementById( labels[l] );
        if( elmnt === null )
        {
            alert( "element " + l + " was not found." );
        }

        if( radios[l].checked === true )
        {
            cleanData(input); 
        }
        else
        {
            elmnt.style.backgroundColor = "lightgray"; 
        }
    }
}




