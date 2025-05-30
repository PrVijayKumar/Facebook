function ldlike(id, uid, btn){
    // console.log(user)
    // flag = document.getElementById("lstatus").innerHTML;
    flag = btn.parentElement.parentElement.querySelector('#lstatus').innerHTML;
    nlikes = parseInt(btn.parentElement.parentElement.querySelector('#nlikes').innerHTML);
    console.log(nlikes)
    if(flag == "Liked"){
        btn.parentElement.parentElement.querySelector('#lstatus').innerHTML = "Not Liked";
        btn.parentElement.parentElement.querySelector('#nlikes').innerHTML = nlikes-1;
        btn.classList.remove("liked");
        console.log(btn.parentElement.querySelector(".fa-heart").classList);
        btn.parentElement.querySelector(".fa-heart").classList.remove("fa-solid");
        btn.parentElement.querySelector(".fa-heart").classList.add("fa-regular");
        // flike("http://127.0.0.1:8000/post/lpost/", id, 0, uid)
        flike("https://localhost:8000/post/lpost/", id, 0, uid)
    }else{
        btn.parentElement.parentElement.querySelector('#lstatus').innerHTML = "Liked";
        btn.parentElement.parentElement.querySelector('#nlikes').innerHTML = nlikes+1;
        btn.classList.add("liked");
        btn.parentElement.querySelector(".fa-heart").classList.remove("fa-regular");
        btn.parentElement.querySelector(".fa-heart").classList.add("fa-solid");
        // flike("http://127.0.0.1:8000/post/lpost/", id, 1, uid)
        flike("https://localhost:8000/post/lpost/", id, 1, uid)
    }
}
function flike(url, id, flag, uid){
    // console.log(user)
    csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    console.log(csrf)

    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.readystate == 4 && this.status == 200){
            x = this.responseText;
        }
    }
    xhttp.open("POST", url+id, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("csrfmiddlewaretoken="+csrf+"&id="+id+"&flag="+flag+"&uid="+uid);
    // console.log(csrf)
}

// const lbtns= document.querySelectorAll('.blike');

// lbtns.forEach(btn => btn.addEventListener('click', () => {
//     flag = btn.parentElement.parentElement.querySelector('.lstatus').innerHTML;
//     flag = btn.parentElement.parentElement.querySelector('.lstatus').innerHTML;
// }));



