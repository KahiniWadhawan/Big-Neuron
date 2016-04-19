#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Jessica"
__date__ = "$Apr 19, 2016 12:18:04 AM$"


def format_into_divs(cand):
    
    fo = open(cand+"_divs.txt", 'a')
    tweetlist = open("tweetlist_filename.txt", 'r')  #if cand == "clinton":
    
    count = 0
    for tweet in tweetlist:
        l0 = "    <div class=\"radio\">"
        l1 = "        <label style=\"background-color: #cccccc; padding:3px 3px;\" id=\"lbl" + count + "\" onclick=\"changeVisualization()\">"
        l2 = "            <input type=\"radio\" name=\"optionsRadios\" id=\"optionsRadios" + count + "\" value=\"option" + count + "\">" + tweet
        l3 = "        </label>"
        l4 = "    </div>"
        
        fo.write(l0)
        fo.write(l1)
        fo.write(l2)
        fo.write(l3)
        fo.write(l4)
        
        count+=1


if __name__ == "__main__":
    candidates = ["clinton", "cruz", "kasich", "sanders", "trump"]
    
    '''
    for cand in candidates:
        format_into_divs(cand)
    '''
    format_into_divs("clinton")
