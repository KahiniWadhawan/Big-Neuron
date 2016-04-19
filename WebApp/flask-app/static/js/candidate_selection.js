/* 
 * Used to redirect to appropriate candidate pages based on particular
 * candidate radio button selected on app's home page.
 */
function whichCandidate(form){
    var candidates = form.elements.candidate;
    var i          = candidates.length;
    assert("i = " + i);
    while (--i > -1){
        assert("checked[" + i + "] = " + candidates[i].checked);
        if(candidates[i].checked){
            return candidates[i].value;
        }
    }
}


