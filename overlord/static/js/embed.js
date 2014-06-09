//function overlord_load_embedded(div) {
//    return
//    var xmlhttp = new XMLHttpRequest();
//    xmlhttp.onreadystatechange = function() {
//        if (xmlhttp.readyState == 4 ) {
//           if(xmlhttp.status == 200){
//               document.getElementById("overlord_embedded").innerHTML = xmlhttp.responseText;
//               alert(xmlhttp.responseText);
//               overlord_activate_colorbox();
//           } else {
//               document.getElementById("overlord_embedded").innerHTML = "ERROR loading the gallery";
//               alert("ERROR");
//           }
//        }
//    }

//    xmlhttp.open("GET", "/image/set/2/2/", true);
//    xmlhttp.setRequestHeader("X-Requested-With","XMLHttpRequest");
//    xmlhttp.send();
//}

if( ! window.jquery ) {
    var head = document.getElementsByTagName('HEAD').item(0);
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'http://code.jquery.com/jquery-1.11.1.min.js'
    head.appendChild(script);
}
if( ! window.colorbox ) {
    var head = document.getElementsByTagName('HEAD').item(0);
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'http://ishimura.server.haithun.com:8000/static/js/jquery.colorbox.js'
    head.appendChild(script);
    script = document.createElement('link');
    script.rel = 'stylesheet';
    script.href = 'http://www.jacklmoore.com/colorbox/example3/colorbox.css';
    head.appendChild(script);
}

function get_fitting_image(link) {
    img = $($(link).children('img')[0]);
    a = $(link)[0];
    src = img.attr('src');
    image_name_sized = src.split("_");
    image_name_sized.pop();
    image_name = image_name_sized.join("");

    if( $(window).width() > 1600 && $(window).height() > 1200) {
        return image_name + "/";
    } else if( $(window).width() > 1400 && $(window).height() > 1050) {
        return image_name + "_f/";
    } else if( $(window).width() > 1067 && $(window).height() > 800) {
        return image_name + "_e/";
    } else if( $(window).width() > 720 && $(window).height() > 576) {
        return image_name + "_d/";
    } else if( $(window).width() > 400 && $(window).height() > 300) {
        return image_name + "_c/";
    } else if( $(window).width() > 250 && $(window).height() > 190) {
        return image_name + "_b/";
    } else {
        return image_name + "_a/";
    }
}

//function embedImage(aimagelink) {
//    var id = $(aimagelink).attr('rel');
//
//    var anchor =$('<a>').attr({
//        class: 'cboxElement overlord',
//        rel: id,
//        style: 'display: none, visibility: hidden',
//        href: aimagelink.href
//    })
//
//    $('<img>').attr({
//        style: 'display: none',
//        src: load_fitting_image(aimagelink),
//        alt: $(aimagelink).children('img')[0].alt
//    }).appendTo(anchor);
//
//
//    $('body').append(anchor);
//}

//var xmlhttp = new XMLHttpRequest();
//xmlhttp.onreadystatechange = function() {
//    if (xmlhttp.readyState == 4 ) {
//        if(xmlhttp.status == 200){
//            document.getElementById("overlord_embedded").innerHTML = xmlhttp.responseText;
//            alert(xmlhttp.responseText);
//            overlord_activate_colorbox();
//        } else {
//           document.getElementById("overlord_embedded").innerHTML = "ERROR loading the gallery";
//           alert("ERROR");
//        }
//    }
//}
//xmlhttp.open("GET", "/image/set/ajax/2/2/", true);
//xmlhttp.setRequestHeader("X-Requested-With","XMLHttpRequest");
//xmlhttp.send();

var checker = 0;

function doStuff() {
    clearInterval(checker);
    var location_ = parent.location.href.split("/");
    var location_rev = location_.reverse();
    location_.pop();
    location_rev.pop();
    location_rev.pop();
    var toLoad = "http://" + location_rev.pop() + "/image/set/" + location_.pop() + "/" + location_.pop() + "/";

    $("#overlord_embedded").load("http://ishimura.server.haithun.com:8000/image/set/2/2/", function() {
        $("#overlord_embedded > .imagerow > #images > .column > .image > a").each(  function() {
                                                                                        parent.embedImage(this);
                                                                                        $(this).click(  function (event) {
                                                                                                            event.preventDefault();
                                                                                                            parent.triggerImage(this);
                                                                                                        });
                                                                                    });
        parent.embedColorBox();
    });

}


function checkJquery() {
    if (window.jQuery) {
        doStuff();
    } else {
        checker = window.setInterval(checkJquery, 100);
    }
}

checkJquery();
