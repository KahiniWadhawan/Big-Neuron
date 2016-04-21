#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Jessica"
__date__ = "$Apr 19, 2016 12:18:04 AM$"


def format_into_divs(cand):
    
    fo        = open(cand+"_divs.txt", 'w')
    tweetlist = open("tweetlist_filename.txt", 'r')  #if cand == "clinton":
    
    count = 0
    for tweet in tweetlist:
        l0 = "    <div class=\"radio\">\n"
        l1 = "        <label style=\"background-color: #cccccc; padding:3px 3px;\" id=\"lbl" + count + "\" onclick=\"changeVisualization()\">\n"
        l2 = "            <input type=\"radio\" name=\"optionsRadios\" id=\"optionsRadios" + count + "\" value=\"option" + count + "\">" + tweet + "\n"
        l3 = "        </label>\n"
        l4 = "    </div>\n"
        
        fo.write(l0 + l1 + l2 + l3 + l4)
        
        count+=1


if __name__ == "__main__":
    candidates = ["clinton", "cruz", "kasich", "sanders", "trump"]
    
    for cand in candidates:
        format_into_divs(cand)
    ''' TO DO: Need tweet list before you can do testing!!
    format_into_divs("clinton")
    '''