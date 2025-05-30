var p_id=null;
var repBtns = document.querySelectorAll("a.repBtn");
function delFunc(){
    return confirm("Do you really want to delete this post?");
}

function getId(id){
    p_id = id;
    // console.log(id)
}

function delPost(result){
        $("#ModalDeletePost").modal('hide');
        // result = JSON.parse(result);
        // console.log(result)
        // console.log("Id="+result.id)
        result = JSON.parse(result);
        console.log(result.id);
        id=".f"+result.id;
        // $(id).attr('display', 'none');
        $(id).hide();
        console.log("MY DELETE MESSAGE")
        console.log(result.msg)
        $('div#mymsgs').html('<p>'+result.msg+'</p>')
        setTimeout(function(){
            $('div#mymsgs').html('')
        }, 2000)
        // console.log($('#mymsgs').val(result.msg))
}

function cChange(obj){
    console.log("cchange Button")
    console.log(obj)
    if(obj.value == ""){
        console.log(this.value);
        console.log("Enabled");
        setBtn("disable", obj);
        console.log($("#csub")[0].disabled);
    }else{
        setBtn("enable", obj);
        console.log("Disabled");
    }
}

function setBtn(status, obj){
    console.log("Set Button")
    console.log(obj)
    button = obj.parentNode.querySelector("button");
    if(status=="disable"){
        // console.log(form.querySelector("button"))
        // $("#csub")[0].disabled=true;
        // $("#csub").addClass("btn-secondary");
        // $("#csub").addClass("myclass");
        // $("#csub").removeClass("btn-primary");
        $(button)[0].disabled=true;
        $(button).addClass("btn-secondary");
        $(button).addClass("myclass");
        $(button).removeClass("btn-primary");
    }else{
        $(button)[0].disabled=false;
        $(button).removeClass("btn-secondary");
        $(button).addClass("btn-primary");
        $(button).removeClass("disabled");
        $(button).removeClass("myclass");
    }
}
//get elements for popup
const popupbtns = document.querySelectorAll('.popbtn');
const popup = document.querySelector("#econtent");
const popupContent = document.querySelector("#emodal");
const delbtns= document.querySelectorAll('.delbtn');

function imgChange(){
    // x = document.getElementById("p_content");
    // console.log(x.value);
    // popupContent.querySelector(".modal-image").src = x.value;
    // y = popupContent.querySelector(".modal-image").src
    // console.log(y.value);
    x = document.getElementById("p_content").files;
    // console.log(x[0]);
    popupContent.querySelector(".modal-image").src = URL.createObjectURL(x[0]);
    y = popupContent.querySelector(".modal-image").src
    // console.log(y);
}





// get post item info
popupbtns.forEach(btn => btn.addEventListener('click', () => {
    // console.log(btn.parentNode.parentNode.querySelector("#ptitle").innerHTML)
    // X = btn.parentNode.parentNode.querySelector("#ptitle").innerHTML;
    // console.log(popupContent)
    // console.log(popupContent.querySelector(".ptitle"));
    
    popupContent.querySelector(".ptitle").value = btn.parentNode.parentNode.querySelector("#ptitle").innerHTML;
    console.log(btn.parentNode.parentNode.querySelector("#ptitle").innerHTML);
    popupContent.querySelector(".modal-image").src = btn.parentNode.parentNode.querySelector("img").src;
    popupContent.querySelector(".pdesc").value = btn.parentNode.parentNode.querySelector(".mydesc").innerHTML;
    // popupContent.querySelector("form").action = "{% url 'post:epost' id=p_id %}"
    // popupContent.querySelector("form").action = "/post/mypost/edit/"+p_id;
    // popupContent.querySelector("form").action = "{% url 'post:epost' id=p_id %}".replace(p_id, p_id);
    // popupContent.querySelector("form").action = popupContent.querySelector("form").action.replace(/pid/, p_id.toString());
    popupContent.querySelector("form").action = btn.parentNode.parentNode.querySelector("#eurl").innerHTML;
    // console.log(popupContent.querySelector("form").action)
}));



// delete post
delbtns.forEach(btn => btn.addEventListener('click', () => {
    // document.querySelector("#cdel").href = btn.parentNode.parentNode.querySelector("#durl").innerHTML;
    url = btn.parentNode.parentNode.querySelector("#durl").innerHTML;
    // console.log(document.getElementsByName("csrfmiddlewaretoken")[0].value)
    $("#cdel").click(function(){

        var formData = new FormData();

        formData.append("csrfmiddlewaretoken", document.getElementsByName("csrfmiddlewaretoken")[0].value);
        $.ajax({
            type: "POST",
            url: url,
            data:formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(response){
                // console.log(typeof(response['result']))
                delPost(response['result']);
            },
            error: function(response){
                console.log(response);
            }
    
        })
    });
    
    console.log("Hello");
}));


// u_post function will update the post through ajax request
// function u_post(obj){
//     obj.preventDefault();
//     console.log(url)
//     var form = new FormData();
//     p_title = document.getElementById("p_title").innerHTML;
//     p_desc = document.getElementById("p_desc").innerHTML;
//     p_content = document.getElementById("p_content").files[0];
//     csrfmiddlewaretoken = document.getElementByName("csrfmiddlewaretoken").innerHTML
//     console.log(csrfmiddlewaretoken);
//     form.append('post_title', p_title);
//     form.append('post_description', p_desc);
//     form.append('post_content', p_content);

//     xhttp = new XMLHttpRequest();
//     xhttp.onreadystatechange = function() {
//         if(this.readystate == 4 && this.status == 200){
//             x = this.responseText;
//         }
//     }
//     xhttp.open("POST", url, true);
//     xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//     xhttp.send(form);
// }

$(document).ready(function() {
    // console.log("Ready")
    setTimeout(function(event){
            $('div#nmsg').remove()
            console.log("Working")
        }, 5000)

    


    $("#uform").submit(function(event) {
        event.preventDefault();
        form = document.getElementById("uform");
        if(form.checkValidity() === false){
            console.log("Validation worked")
            event.preventDefault();
            event.stopPropagation();
            form.classList.add("was-validated");
            return false;
        }
        // console.log($("#uform").classList);
        else{
            url = $(this).attr("action");
            console.log(url);
            // var formData = {
            //     post_title: $("#p_title").val(),
            //     post_description: $("#p_desc").val(),
            //     // post_content: $(".modal-image").attr("src"),
            //     csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            // };

            var formData = new FormData($('#uform')[0]);
            // console.log($('form')[0])
            // console.log($('#uform')[0])
            // console.log($(".modal-image").files[0]);
            // console.log($("#uform")[0].files[0]);
            // console.log(form.checkValidity());
            // var forms = document.getElementsByClassName('needs-validation');
            // if($('form')[0].checkValidity() === false){
            //     event.preventDefault();
            //     event.stopPropagation();
            // }


            $.ajax({
                type: "POST",
                url: url,
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                success: function(response) {
                    // console.log(response['result']);
                    $('#ModalEditPost').modal('hide');
                    // $('#ModalEditPost').attr("data-dismiss") = "modal";
                    updatePage(response['result'])
                },
                error: function(response){
                    console.log("Error");
                }
            })
        } 

    })



    $("#cform").submit(function(event){
        event.preventDefault();
        // console.log("Comment Form")
        // console.log(event.target.querySelector("#"))
        var formData = new FormData($('#cform')[0]);
        // formData.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken'))
        url = $('#cform').attr('action');
        console.log(url);
        obj = $("#commentp")[0];
        $("#commentp")[0].value="";
        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(response){
                // console.log(response['result']);
                comUpdate(response['result'], obj);
            },
            error: function(response){
                console.log("Error");
            }
        })
    })

    $("#cclose").click(function(e){
        // console.log(e.target.parentNode.parentNode.parentNode);
        // elem = e.target.parentNode.parentNode.parentNode.querySelectorAll(".rform");
        // console.log(elem)
        // console.log($("#repBlock")[0])
        // $("#repBlock").html("");
        // $("#repBlock").empty();
        // elem.forEach(function(el) {
        //     console.log(el.parentNode)
        //     $(el).remove();
        //     $(el).empty();
        //     el.remove();
        //     console.log(el)
        // })
        // for(var i=0; i<elem.length; i++){
        //     // console.log(i);
        //     // console.log(elem[i].parentNode);
        //     // $(elem[i].parentNode).innerHTML="";
        //     // document.querySelector(elem).innerHTML="";
        // }
        // console.log($(elem)[0].querySelectorAll(".rform"))
        // $(elem)[0].querySelector(".rform").remove();
        // console.log(e.target.parentNode.parentNode.parentNode)
        // console.log(e.target.parentNode.parentNode.parentNode.removeChild("#repBlock"))
        rbs = document.querySelectorAll("#repBlock");
        console.log(rbs[0].parentNode)
        // while(rbs[0]){
        //     if(rbs[0].innerHTML != ""){
        //         rbs[0].parentNode.removeChild(rbs[0]);
        //     }
        // }

        $("#ucom")[0].innerHTML="";
        $("#commentp")[0].value="";
        $("form.rform").remove();
    })

    
    
    
    
    function updatePage(result){
        result = result;
        jres = JSON.parse(result)
        console.log(result)
        console.log(typeof(jres))
        console.log(jres[0].fields.post_content)
        jres[0].fields.post_content
        pid = jres[0].pk;
        pid = 'f'+pid;
        pid = "."+pid
        console.log(pid);
        console.log(typeof(jres[0].fields.post_updated_date));
        // console.log(document.querySelector("."+pid));
        x = document.querySelector(pid);
        // y = "/" + window.location.host + "/media/" +jres[0].fields.post_content;
        y = "/media/" +jres[0].fields.post_content;
        var date = new Date(jres[0].fields.post_updated_date)
        console.log(date)
        mon = date.toLocaleString("default", {month: "short"});
        day = date.toLocaleString("default", {day: "numeric"});
        year = date.getFullYear();
        time = date.toLocaleTimeString("default", {hourCycle: "h12", hour: "numeric", minute: "numeric"});
        // time = time.replace(/(.{1})/g,".1")
        date = mon+". "+day+", "+year+", "+time+".";
        console.log(date)
        // date = date.getMonth()+1 +". "+ date.getDate() + " " + date.getFullYear();
        console.log(y);
        // x.parentNode.querySelector("#pdate").innerHTML=jres[0].fields.post_updated_date;
        x.querySelector("#pdate").innerHTML=date;
        x.querySelector("#ptitle").innerHTML=jres[0].fields.post_title;
        x.querySelector("img").src=y ;
        x.querySelector(".mydesc").innerHTML=jres[0].fields.post_description;
    
    }


    


    commbtns = document.querySelectorAll('.bcom');
    compop = document.querySelector('#CommentModal');
    commbtns.forEach(btn => btn.addEventListener('click', () => {
        console.log("button clicked");
        x = btn.parentNode.parentNode;
        console.log(x);
        compop.querySelector(".modal-title").innerHTML=x.querySelector('#fbuser').innerHTML+"'s post";
        console.log("image source")
        // console.log(e.target.closest('#fposts').querySelector('img').getAttribute('src'))
        $("img.com_img").attr('src', x.querySelector('img').getAttribute('src'))
        compop.querySelector("#p_user").innerHTML=x.querySelector('#fbuser').innerHTML;
        compop.querySelector("#p_desc").innerHTML=x.querySelector('.mydesc').innerHTML;
        // compop.querySelector("#p_img").src=x.querySelector('img').src;
        console.log(x.querySelector('.mydesc').innerHTML);
        document.querySelector("#cform").action = x.querySelector("#curl").innerHTML;
        
        fetchComments(x.querySelector('#fcurl').innerHTML);
        // comments = JSON.parse(comments);
        // console.log(comments);
        // comments.forEach(c => {
            //     document.querySelector("#ucom").innerHTML=
            //         result[0].fields.comment_desc+'<br>'+document.querySelector("#ucom").innerHTML;
        // })
        
        
        
    }));


    function comUpdate(result, obj){
        // com_user = this.querySelector("#pc_user").innerHTML;
        // f_user = JSON.parse(document.getElementById("c_user").textContent);
        // console.log(response['result']);
        result = JSON.parse(result);
        // console.log("Hello from"+document.getElementById("c_user").textContent);
        user = JSON.parse(document.getElementById("c_user").textContent);
        console.log(result[0].fields.comment_desc);
        console.log("Nice Javascript")
        console.log(result);
        // tempCom = '<div id="tempCom"><strong>'+user+"</strong><p>"+result[0].fields.comment_desc+'<br><a href="#">Like</a> <a href="#" class="repBtn">Reply</a></p></div>'
        // document.querySelector("#ucom").innerHTML=tempCom+document.querySelector("#ucom").innerHTML;
        // tempCom = '<div id="tempCom"><strong>'+user+"</strong><p>"+result[0].fields.comment_desc+'<br><a href="#">Like</a> <a href="#" class="repBtn">Reply</a></p></div>'
        // document.querySelector("#ucom").innerHTML=tempCom+document.querySelector("#ucom").innerHTML;
        tempCom = "<div class='c"+result[0].pk+"'><div id='com_block'><strong><span id='pc_user'>"+user+"</span></strong><p id='com_desc'><span>"+result[0].fields.comment_desc+"</span><button class='edcbtn'><i class='fa-solid fa-ellipsis'></i></button>\
                                    <br><a href='#'>Like</a>&nbsp;<a href='#' class='repBtn'>Reply</a>\
                                    <div id=pc_id>"+result[0].pk+"</div><div class='edccmt'></div>\
                                    </div><div id='repBlock'></div><div id='repBForm'></div><div id=pc_id>"+result[0].pk+"</div></div></div>";
        document.querySelector("#ucom").innerHTML=tempCom+document.querySelector("#ucom").innerHTML;
        setBtn("disable", obj);
        
    }

    function fetchComments(url){
        // var fdata = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value)
        // console.log(fdata)
        $.ajax({
            'type': 'POST',
            'url': url,
            // 'data': { 'csrfmiddlewaretoken': fdata},
            'data': formData,
            'cache': false,
            'processData': false,
            'contentType': false,
            success: function(response){
                // console.log(response['result']);
                showComments(response['result'], response['users'], response['rlist']);
                // showComments(response['result']);
            },
            error: function(response){
                console.log('error');
            }
        })
    }


    function showComments(result, users, rlist){
        comments = JSON.parse(result);
        console.log(comments)
        users = JSON.parse(users);
        console.log("FUnction check")
        console.log(users)
        rlist = JSON.parse(rlist);
        // console.log(comments);
        // console.log(users[0].username);
        function getUserName(id){
            a = "";
            users.forEach(user => {
                console.log(user[1])
                if(user[0] == id){
                    // console.log(id)
                    a = user[1]
                    // console.log(typeof(a))
                    // a = a.toString()
                }else{
                    return "Error";
                }
            })
            return a;
        }
        comments.forEach(c => {
            console.log("User Check")
            console.log(getUserName(c.fields.com_user))
            user = getUserName(c.fields.com_user);
            c_user = JSON.parse(document.getElementById("c_user").textContent);
            if(user == c_user){
                edc_block = "<div class='edccmt'></div>";
            }else{
                edc_block = "";
            }
            // console.log("Carror check")
            // console.log(c.pk)
            link = '';
            if(rlist.includes(c.pk)){
                console.log("Primary key check")
                console.log(c.pk)
                console.log(a)
                // link = "<a href='http://127.0.0.1:8000/post/freplies/"+c.pk+"' id='faReplies'>Show All Replies</a>";
                link = "<a href='https://localhost:8000/post/freplies/"+c.pk+"' id='faReplies'>Show All Replies</a>";
            }else{
                link = "No Replies to this comment";
            }
            $("#ucom")[0].innerHTML+="<div class='c"+c.pk+"'><div id='com_block'><strong><span id='pc_user'>"+user+"</span></strong><p><span id='com_desc'>"+c.fields.comment_desc+"</span><button class='edcbtn'><i class='fa-solid fa-ellipsis'></i></button>\
                                    <br><a href='#'>Like</a>&nbsp;<a href='#' class='repBtn'>Reply</a>\
                                    <div id=pc_id>"+c.pk+"</div>"+edc_block+"\
                                    </div><div id='repBlock'></div><div id='repBForm'></div>"+link+"<div id=pc_id>"+c.pk+"</div></div></div>";
        })
        var repBtns = document.querySelectorAll("a.repBtn");
        console.log(repBtns);
        // repBtns.forEach(btn => btn.addEventListener('click', () => {
        // $('.repBtn').on('click', function(){
        $(document).on('click', 'a.repBtn', function(e){
            elem = e.target
            console.log(e.target)
            console.log("Button clicked")
            url = $("#cform")[0].action;
            console.log(url);
            // console.log(btn.parentNode.parentNode);
            // console.log(this.parentNode.parentNode);
            console.log(elem.parentNode);
            console.log("Id check")
            console.log($(elem.parentNode).siblings("#pc_id").text())
            // block = '<form action="'+url+'" method="POST" class="rform">\
            // <input type="hidden" name="csrfmiddlewaretoken" value='+document.getElementsByName("csrfmiddlewaretoken")[0].value+'>\
            // <div class="form-group myinput">\
            // <label>'+btn.parentNode.parentNode.querySelector("#pc_user").innerHTML+'</label>\
            // <input type="hidden" name="com_reply" value='+btn.parentNode.parentNode.querySelector("#pc_user").innerHTML+'>\
            // <input type="text" name="comment_desc" class="form-control" id="commentp">&nbsp;&nbsp;\
            // <input type="hidden" name="reply_on_comment" value='+btn.parentNode.parentNode.querySelector("#pc_id").innerHTML+'>\
            // <button type="submit" class="btn btn-primary" id="rsub"><i class="fa-regular fa-paper-plane"></i></button>\
            // </div>\
            // </form>';
            // <input type="hidden" name="com_reply" value='+this.parentNode.parentNode.querySelector("#pc_user").innerHTML+'>
            // <input type="hidden" name="reply_on_comment" value='+this.parentNode.parentNode.querySelector("#pc_id").innerHTML+'>\
            console.log($(elem.parentNode.parentNode).siblings("#repBForm").html())
            block = '<form action="'+url+'" method="POST" class="rform">\
            <input type="hidden" name="csrfmiddlewaretoken" value='+document.getElementsByName("csrfmiddlewaretoken")[0].value+'>\
            <div class="form-group myinput">\
            <label>'+elem.parentNode.parentNode.querySelector("#pc_user").innerHTML+'</label>\
            <input type="hidden" name="com_reply" value='+elem.parentNode.parentNode.querySelector("#pc_user").innerHTML+'>\
            <input type="text" name="comment_desc" class="form-control" id="commentp">&nbsp;&nbsp;\
            <input type="hidden" name="reply_on_comment" value='+$(elem.parentNode).siblings("#pc_id").text()+'>\
            <button type="submit" class="btn btn-primary" id="rsub"><i class="fa-regular fa-paper-plane"></i></button>\
            </div>\
            </form>';
            // $("#repBlock")[0].innerHTML=block;
            // console.log($("#repBlock")[0]);
            // btn.parentNode.parentNode.querySelector("#repBlock").innerHTML += block;
            // btn.parentNode.parentNode.querySelector("#commentp").focus();
            // this.parentNode.parentNode.querySelector("#repBlock").innerHTML += block;
            // this.parentNode.parentNode.querySelector("#commentp").focus();
            // elem.parentNode.parentNode.querySelectorAll("#repBForm").innerHTML = block;
            console.log("comment check")
            console.log($(elem.parentNode.parentNode).siblings("#repBForm").html())
            $(elem.parentNode.parentNode).siblings("#repBForm").html(block);
            // elem.parentNode.parentNode.querySelector("#commentp").focus();
            console.log("Element Check")
            console.log($(elem.parentNode.parentNode).siblings("#repBForm")[0])
            $(elem.parentNode.parentNode).siblings("#repBForm")[0].querySelector("#commentp").focus();
            // console.log(btn.parentNode.parentNode.querySelectorAll("input")[1]);
            // console.log(btn.parentNode.parentNode.querySelector("#repBlock"));
            $(".rform").on('submit',function(event){
                console.log($(this));
                event.preventDefault();
                var formData = new FormData($("#rform")[0])
                // console.log($(".rform")[0]);
                // console.log($(this)[0]);
                // console.log($(".rform")[0].querySelector("#commentp").value);
                // console.log(this.querySelector("#commentp").value);
                // console.log(this);
                // var formData = new FormData(this);
                // btn=this.parentNode.parentNode.querySelector(".repBtn"); 
                console.log(this.querySelector("#commentp").value);
                console.log(this);
                var formData = new FormData(this);
                btn=this.parentNode.parentNode.querySelector(".repBtn");
                // console.log("My Button");
                // console.log(btn);
                // console.log("Before ajax");
                // console.log(this.parentNode)
                $.ajax({
                    'type': 'POST',
                    'url': url,
                    'data': formData,
                    'cache': false,
                    'processData': false,
                    'contentType': false,
                    success: function(response){
                        console.log(response);
                        // showReplies(response['result'], btn)
                        console.log(btn)
                        showReplies(response['result'], btn)
                    },
                    error: function(response){
                        console.log("Error")
                    }

                })

            })    
            
        });
        
        $(document).on('click', "a#faReplies", function(e){
            e.preventDefault();
            console.log("Fetch all replies.")
            var formData = new FormData();
            csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
            formData.append("csrfmiddlewaretoken", csrf);
            btn=e.target;
            id=$(btn).siblings("#pc_id").text();
            console.log(id)
            console.log(this.href)
            btn = this;
            $.ajax({
                'type': 'POST',
                'url': this.href,
                'data': formData,
                'cache': false,
                'processData': false,
                'contentType': false,
                success: function(response){
                    console.log(response);
                    // result = JSON.parse(response['result']);
                    // console.log(result);
                    showAllReplies(response['result'], response['users'], response['rlist'], btn);
                },
                error: function(response){
                    console.log("error");
                }
            })
        })
    
    }

    function showReplies(result, obj){
        console.log("Obj value");
        console.log(obj);
        user = JSON.parse(document.getElementById("c_user").textContent);
        console.log("today's result")
        console.log(result);
        result = JSON.parse(result);
        console.log(result[0].fields.comment_desc);
        r_id = result[0].fields.com_reply
        desc = result[0].fields.comment_desc
        // console.log($(obj.parentNode.parentNode).siblings("#repBForm")[0].querySelector(".rform"));
        console.log("current form"+$(obj.parentNode.parentNode).siblings("#repBForm")[0].querySelector(".rform"));
        // console.log(obj.parentNode.parentNode.querySelector("#repBlock").innerHTML);
        // console.log(obj.parentNode.parentNode.parentNode.querySelector("#repBlock"));
        var block = $(obj.parentNode.parentNode).siblings("#repBlock")[0].innerHTML;
        // obj.parentNode.parentNode.querySelector("#repBlock").innerHTML = "<div id='reply'><a href='#' id='cur_user'><strong><span id='pc_user'>"+user+"</span></strong></a>\
        //                                                                 <br><a id='r_info' href='#'><strong>"+r_id+"</strong></a>\
        //                                                                 <span id='r_info'>"+desc+"</span><br>\
        //                                                                 <a href='#'>Like</a> <a href='#' class='repBtn'>Reply</a></div>\
        //                                                                 <div id='repBlock'></div><div id='pc_id'>"+result[0].pk+"</div>"+block;

        // obj.parentNode.parentNode.querySelector("#repBlock").innerHTML ="<div id='reply' class='c"+result[0].pk+"'><div id='rep_block'><a href='#' id='cur_user'><strong><span id='pc_user'>"+user+"</span></strong></a><p><a id='r_info' href='#'><strong>"+r_id+"</strong></a>\
        $(obj.parentNode.parentNode).siblings("#repBlock")[0].innerHTML ="<div id='reply' class='c"+result[0].pk+"'><div id='rep_block'><a href='#' id='cur_user'><strong><span id='pc_user'>"+user+"</span></strong></a><p><a id='r_info' href='#'><strong>"+r_id+"</strong></a>\
                                                                        <span id='com_desc'>"+desc+"</span><button class='edcbtn'><i class='fa-solid fa-ellipsis'></i></button>\<br><a href='#'>Like</a>&nbsp;<a href='#' class='repBtn'>Reply</a></p>\
                                                                        <div id=pc_id>"+result[0].pk+"</div><div class='edccmt'></div></div><div id='repBlock'></div><div id='repBForm'></div></div>" + block;
        // obj.parentNode.parentNode.querySelector(".rform")[0].remove();
        c_form = obj.parentNode.parentNode.querySelector(".rform");
        console.log("vijay's form")
        console.log(c_form)
        $(c_form).remove();
        // $('.rform').remove()
        console.log(obj.classList[0]);
        // console.log($(obj)[0])
        // console.log($(obj).trigger('click'));
        // $(obj.classList[0]).trigger('click');
        console.log("Disply Info");
        console.log($(obj)[0]);

        $(obj)[0].click();
        console.log(repBtns)
        repBtns = document.querySelectorAll("a.repBtn");
        console.log(repBtns)
        
    }   
    function addReplyForm(obj){

        block = '<form action="'+url+'" method="POST" class="rform">\
        <input type="hidden" name="csrfmiddlewaretoken" value='+document.getElementsByName("csrfmiddlewaretoken")[0].value+'>\
        <div class="form-group myinput">\
        <label>'+btn.parentNode.parentNode.querySelector("#pc_user").innerHTML+'</label>\
        <input type="hidden" name="com_reply" value='+btn.parentNode.parentNode.querySelector("#pc_user").innerHTML+'>\
        <input type="text" name="comment_desc" class="form-control" id="commentp">&nbsp;&nbsp;\
        <input type="hidden" name="reply_on_comment" value='+btn.parentNode.parentNode.querySelector("#pc_id").innerHTML+'>\
        <button type="submit" class="btn btn-primary" id="rsub"><i class="fa-regular fa-paper-plane"></i></button>\
        </div>\
        </form>';
        // $("#repBlock")[0].innerHTML=block;
        // console.log($("#repBlock")[0]);
        obj.parentNode.parentNode.querySelector("#repBlock").innerHTML += block;
        obj.parentNode.parentNode.querySelector("#commentp").focus();
        // console.log(btn.parentNode.parentNode.querySelectorAll("input")[1]);
        // console.log(btn.parentNode.parentNode.querySelector("#repBlock"));
        $(".rform").on('submit',function(event){
            console.log($(this));
            event.preventDefault();
            var formData = new FormData($("#rform")[0])
            // console.log($(".rform")[0]);
            // console.log($(this)[0]);
            // console.log($(".rform")[0].querySelector("#commentp").value);
            console.log(this.querySelector("#commentp").value);
            console.log(this);
            var formData = new FormData(this);

            $.ajax({
                'type': 'POST',
                'url': url,
                'data': formData,
                'cache': false,
                'processData': false,
                'contentType': false,
                success: function(response){
                    console.log(response);
                    showReplies(response['result'], btn)
                },
                error: function(response){
                    console.log("Error")
                }
            })
        })
    }


    $(".repBtn2").on('click')

    // function subReply(event){
    //     event.preventDefault();
    //     console.log("Function worked");
    // }


    function showAllReplies(result, users, rlist, obj){
        results = JSON.parse(result);
        users = JSON.parse(users);
        rlist = JSON.parse(rlist)
        console.log(users)
        console.log("Result Check")
        console.log(results.length)
        $(obj).siblings("#repBlock")[0].innerHTML="";
        if(results.length == 0){
            $(obj).siblings("#repBlock")[0].innerHTML+="<br>No Replies to this comment";
        }else{
        // console.log(results);
        results.forEach(function(r){
            console.log(r)
            // user = r.fields.com_user;
            r_id = r.fields.com_reply;
            desc = r.fields.comment_desc;
            function getUserName(id){
                console.log("Get User Name");
                a = "";
                users.forEach(user => {
                    // console.log(user.username)
                    // console.log(user.fields)
                    if(user.id == id){
                        // console.log(id)
                        a = user.username
                        // console.log(typeof(a))
                        // a = a.toString()
                    }else{
                        return "Error";
                    }
                })
                console.log(a);
                return a;
            }
            console.log("Replies check");
            console.log(rlist);
            console.log($(obj).siblings("#repBlock")[0]);
            link = ''
            rlist.forEach(function(a){
                console.log(a)
                if(a == r.pk){
                    // link = "<a href='http://127.0.0.1:8000/post/freplies/"+r.pk+"' id='faReplies'>Show All Replies</a>"
                    link = "<a href='https://localhost:8000/post/freplies/"+r.pk+"' id='faReplies'>Show All Replies</a>"
                }else{
                    link = "No Replies"
                }
            })
            c_user = JSON.parse(document.getElementById('c_user').textContent);
            if(c_user == getUserName(parseInt(r.fields.com_user))){
                edc_block = "<div class='edccmt'></div>";
            }else{
                edc_block = "";
            }
            $(obj).siblings("#repBlock")[0].innerHTML+="<div id='reply' class='c"+r.pk+"'><div id='rep_block'><a href='#' id='cur_user'><strong><span id='pc_user'>"+getUserName(parseInt(r.fields.com_user))+"</span></strong></a><p><a id='r_info' href='#'><strong>"+r_id+"</strong></a>\
                                                                        <span id='com_desc'>"+desc+"</span><button class='edcbtn'><i class='fa-solid fa-ellipsis'></i></button>\
                                                                        <br><a href='#'>Like</a>&nbsp;<a href='#' class='repBtn'>Reply</a>\
                                                                        <div id=pc_id>"+r.pk+"</div>"+edc_block+"</div><div id='repBlock'></div><div id='repBForm'></div>"+link+"</div>";
        })
        }
        $(obj).hide();

    }

    // $("div#com_block").mouseover(function(){
    $(document).on('mouseover', 'div#com_block, div#reply', function(){
        // console.log("Mouse Over");
        com_user = this.querySelector("#pc_user").innerHTML;
        f_user = JSON.parse(document.getElementById("c_user").textContent);
        // console.log(com_user);
        // console.log(f_user);
        if(com_user == f_user){
            // console.log(com_user == f_user);
            this.querySelector(".edcbtn").style.display = "inline";
            // console.log(this.querySelector(".edcbtn").style.display);
            // console.log(this.querySelector(".edcbtn").style.display);
        }
    });
    // $("div#com_block").mouseout(function(){
    // $(document).on('mouseout', 'div#com_block, div#reply', function(){
    //     console.log("Mouse Out");
    //     com_user = this.querySelector("#pc_user").innerHTML;
    //     f_user = JSON.parse(document.getElementById("c_user").textContent);
    //     console.log(com_user == f_user);
    //     if(com_user == f_user){
    //         console.log(this);
    //         this.querySelector(".edcbtn").style.display = "none";
    //         // console.log());
    //     }
    // });

    $(document).on('click', 'button.edcbtn', function(e){
        // console.log("Button clicked");
        console.log(this.parentNode.parentNode);
        id = this.parentNode.parentNode.querySelector('#pc_id').innerHTML
        // block = "<a class='editcomment' href='http://127.0.0.1:8000/post/cedit/"+id+"'>Edit</a><br><a href='#DeleteCommentModal' class='delcomment' data-toggle='modal' target-data='#DeleteCommentModal'>Delete</a>"
        block = "<a class='editcomment' href='https://localhost:8000/post/cedit/"+id+"'>Edit</a><br><a href='#DeleteCommentModal' class='delcomment' data-toggle='modal' target-data='#DeleteCommentModal'>Delete</a>"
        this.parentNode.parentNode.querySelector("div.edccmt").innerHTML = block;
    });

    // $(document).mouseup(function(e){
    //     if(!$('.edccmt').is(e.target) && $('.edccmt').has(e.target).length ===0)
    //     {
    //         $('.edccmt').hide()
    //     }
    // })
    // $('.editcomment').on('click', function(e){
    $(document).on('click', 'a.editcomment', function(e){
        e.preventDefault();
        console.log(e.target.parentNode.parentNode);
        previousValue = e.target.parentNode.parentNode.querySelector('p');
        user = e.target.parentNode.parentNode.querySelector('#pc_user');
        $(previousValue).hide();
        $(user).hide();
        url = e.target.href;
        console.log(e.target.parentNode.parentNode);
        parent = e.target.parentNode.parentNode;
        // e.target.parentNode.parentNode.removeChild(".edccmt");
        console.log(url);
        console.log(previousValue.querySelector('#com_desc').textContent);
        e.target.parentNode.parentNode.innerHTML += '<form action="'+url+'" method="POST" class="ecform">\
        <input type="hidden" name="csrfmiddlewaretoken" value='+document.getElementsByName("csrfmiddlewaretoken")[0].value+'>\
        <div class="form-group myinput">\
        <label><strong>'+user.innerHTML+'</strong></label>\
        <input type="hidden" name="com_reply" value=>\
        <input type="text" name="comment_desc" class="form-control" id="commentp" autofocus value="'+previousValue.querySelector('#com_desc').textContent+'" onfocus="this.setSelectionRange(this.value.length,this.value.length);" oninput="cChange(this)">&nbsp;&nbsp;\
        <input type="hidden" name="reply_on_comment" value=>\
        <button type="submit" class="btn btn-primary" id="rsub"><i class="fa-regular fa-paper-plane"></i></button>\
        </div>\
        </form>';
        // console.log($(e.target.parentNode)[0].siblings("form")[0])
        // $(e.parentNode).siblings(".ecform")[0].querySelector("#commentp").focus()
        // console.log(e.target.parentNode.innerHTML);
        // e.target.parentNode.style.display = "none";
        // $(e.target.parentNode).hide();
        ele = e.target.parentNode.querySelector("a.editcomment")
        parent.querySelector(".edccmt").innerHTML = "";
        console.log("Edit Check")
        // console.log(parent.querySelector(".edccmt").innerHTML)

        this.parentNode.removeChild(ele)
        // ele.style.backgroundColor = "blue";
        // e.target.parentNode.removeChild(ele)
        // e.target.outerHTML = "";
        e.target.remove();
        // console.log(e.target.parentNode.removeChild(e.target))
        // $(e.target.parentNode).empty();
        // $(e.target.parentNode).remove();
    })
    
    $(document).on('submit', 'form.ecform', function(e){
        e.preventDefault();
        console.log("Form worked.");
        console.log(e.target.parentNode);
        com_block = e.target.parentNode
        url = this.action;
        var formData = new FormData(this);

        $.ajax({
            'type': 'POST',
            'url': url,
            'data': formData,
            'cache': false,
            'processData': false,
            'contentType': false,
            success: function(response){
                // console.log(response);
                showUpdateComment(response['result'], com_block);
            },
            error: function(resonse){
                console.log(response);
            }
        })
        
    });
    function showUpdateComment(result, com_block){
        console.log(result);
        result = JSON.parse(result);
        console.log(result[0].fields.comment_desc)
        console.log(com_block)
        com_block.querySelector("#com_desc").innerHTML = result[0].fields.comment_desc;
        form = com_block.querySelector(".ecform")
        com_p = com_block.querySelector("p")
        user = com_block.querySelector('#pc_user')
        $(form).remove();
        $(user).show();
        $(com_p).show();
        // $(com_block.ecform).hide();
        // $(com_block.ecform).hide();

    }
    
    $(document).on('click', 'a.delcomment', function(e){
        e.preventDefault();
        id = e.target.parentNode.parentNode.querySelector("#pc_id").innerHTML;
        console.log("Button clicked.")
        console.log(e.target.parentNode.parentNode.querySelector("#pc_id").innerHTML)
        // $('a#delcbtn').attr('href', 'http://127.0.0.1:8000/post/cdelete/'+id)
        $('a#delcbtn').attr('href', 'https://localhost:8000/post/cdelete/'+id)

    })

    $(document).on('click', 'a#delcbtn', function(e){
        e.preventDefault();
        // obj = e.target;
        url = e.target.href;
        console.log(url);
        csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrf)
        $.ajax({
            'type': 'POST',
            'url': url,
            'data': formData,
            'cache': false,
            'processData': false,
            'contentType': false,
            success: function(response){
                // console.log(response);
                delComment(response['result']);
            },
            error: function(response){
                console.log("Error");
            }
        })
    })

    function delComment(result, obj){
        $("#DeleteCommentModal").modal('hide');
        result = JSON.parse(result)
        console.log(result.id);
        id = '.c'+result.id
        console.log($(id)[0]);
        $(id)[0].innerHTML="";
    }


    $(document).on("click", "button.bstars", function(e){
        console.log("stars clicked")
        console.log(e.target.parentNode.parentNode)
        received_by = e.target.parentNode.parentNode.querySelector("span#fbuser").innerHTML
        post = e.target.parentNode.parentNode.classList[0].replace('f', '')
        // console.log(post[0].replace('f', ''))
        $("input#stars_received_by").attr('value', received_by)
        $("input#stars_sent_on_post").attr('value', post)
    })

    $("form#sendStars").submit(function(e){
        e.preventDefault();
        console.log("Send Stars")

        // obj = e.target;
        url = e.target.action;
        console.log(url);
        csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        var formData = new FormData($("form#sendStars")[0]);
        formData.append('csrfmiddlewaretoken', csrf)
        $.ajax({
            'type': 'POST',
            'url': url,
            'data': formData,
            'cache': false,
            'processData': false,
            'contentType': false,
            success: function(response){
                // console.log("response"+response);
                // delComment(response['result']);
                updateStars(response['result'])
            },
            error: function(response){
                console.log("Error");
            }
        })
    })


    function updateStars(result){
        console.log("stars working")
        result = JSON.parse(result)
        console.log(result['post_id'])
        post_class = 'f'+result['post_id']
        console.log(post_class)
        console.log($('div.'+post_class)[0].querySelector("#nstars").innerHTML)
        $('div.'+post_class)[0].querySelector("#nstars").innerHTML = result['amount']
        // console.log($("input#amountp")[0].attr('value'))
        // quantity of stars
        console.log('stars'+$("#amountp").val())
        qos = document.getElementById("quantity_stars")
        qos.innerHTML = parseInt(qos.innerHTML)-parseInt($("#amountp").val())
        $("#amountp").attr('value', '');
        $("#amountp").val('');
        $("#PaymentModal").modal('hide');
    }



    $("input#amountp").on('input', function(e){
        console.log("stars changing")
        console.log(e.target.value)
        stars_input_value = parseInt(e.target.value)
        qos = parseInt(document.getElementById("quantity_stars").innerHTML)
        if(stars_input_value > qos){
            console.log("Not Sufficient Stars")
            e.target.value = qos
        }
        
        // $("input#hidden_stars").val(e.target.value)

    })

});