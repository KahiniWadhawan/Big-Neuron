  //ajax call
    function get_words() {
        //make ajax call
        d3.json("http://127.0.0.1:5000/feed/word_count", function(json, error) {
          if (error) return console.warn(error);
          var words_array = [];
          for (key in json){
            words_array.push({text: key, size: json[key]})
          }
          //render cloud
          mycloud.stop().words(words_array).start();
        });
    };