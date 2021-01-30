function changeColor(num){
    var pre_k = document.getElementById("pre-k")
    var grade_k = document.getElementById("grade-k")
    var grade_1 = document.getElementById("grade-1")
    var grade_2 = document.getElementById("grade-2")
    //pre_k.style.backgroundColor="LightGray"

    if(num == 1){
        pre_k.style.border="3px solid black"
        grade_k.style.border="1px solid black"
        grade_1.style.border="1px solid black"
        grade_2.style.border="1px solid black"
    }else if(num == 2){
        pre_k.style.border="1px solid black"
        grade_k.style.border="3px solid black"
        grade_1.style.border="1px solid black"
        grade_2.style.border="1px solid black"
    }else if(num == 3){
        pre_k.style.border="1px solid black"
        grade_k.style.border="1px solid black"
        grade_1.style.border="3px solid black"
        grade_2.style.border="1px solid black"
    }else{
        pre_k.style.border="1px solid black"
        grade_k.style.border="1px solid black"
        grade_1.style.border="1px solid black"
        grade_2.style.border="3px solid black"
    }
    
        
    
}

