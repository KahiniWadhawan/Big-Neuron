/* 
 * Used to redirect to appropriate candidate pages based on particular
 * candidate radio button selected on app's home page.
 */
function whichCandidate(form){
    var candidates = form.elements.candidate;
    var i          = candidates.length;
    
    while (--i > -1){
        if(candidates[i].checked){
            return candidates[i].value;
        }
    }
}


