/* 
 * Used to redirect to appropriate candidate pages based on particular
 * candidate radio button selected on app's home page.
 */
function idForm(){
    var selectvalue = $('input[name=optradio]:checked', '#idForm').val();

    if(selectvalue === "r0"){
    window.open('http://www.google.com','_self');
    return true;
    }
    else if(selectvalue === "r1"){
    window.open('http://www.google.com','_self');
    return true;
    }else if(selectvalue === 'r2'){
    window.open('http://www.google.com','_self');
    return true;
    }else if(selectvalue === 'r3'){
    window.open('http://www.google.com','_self');
    return true;
    }else if(selectvalue === 'r4'){
    window.open('http://www.google.com','_self');
    return true;
    }
    return false;
    };


