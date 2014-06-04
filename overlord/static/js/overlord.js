function ajaxmodal(alink) {
    var hrefid = "#" + alink.pathname.replace(/(\/)/g, "") + "_modal";

    if ($(hrefid).length>0) {
        $(hrefid).remove();
    }

    $.get(alink.href, function (data) {
        $("body").append(data);
        $(hrefid).modal();
    });

    return false;
}

function ajaxform(form) {
    var action = $(form).attr("action");
    var splittedurl = action.split("/");
//    var divid = "#" + splittedurl.splice(0, splittedurl.length-3).join("");
//    var divid = "#" + 
    var hrefid = "#" + action.replace(/(\/)/g, "") + "_modal";

//    $(form).submit(function() {

        $.ajax({
            data: $(form).serialize(),
            type: $(form).attr('method'),
            url: action,
            success: function(data) {
                $(divid).empty();
                $(divid).html(data);
		$(hrefid).modal('hide');
            }
        });
        return false;

//    });
}

function imagemodal(image) {
    
    
    
}

function load_fitting_image(link) {
    img = $($(link).children('img')[0]);
    a = $(link)[0];
    src = img.attr('src');
    image_name_sized = src.split("_");
    image_name_sized.pop();
    image_name = image_name_sized.join("");

    if( $(window).width() > 1600 && $(window).height() > 1200) {
	return image_name + "/";
	img.attr('src', image_name);
	a.href = image_name;
    } else if( $(window).width() > 1400 && $(window).height() > 1050) {
	return image_name + "_f/";
	img.attr('src', image_name + "_f");
	a.href = image_name;
    } else if( $(window).width() > 1067 && $(window).height() > 800) {
	return image_name + "_e/";
	img.attr('src', image_name + "_e");
	a.href = image_name;
    } else if( $(window).width() > 720 && $(window).height() > 576) {
	return image_name + "_d/";
	img.attr('src', image_name + "_d");
	a.href = image_name + "_f";
    } else if( $(window).width() > 400 && $(window).height() > 300) {
	return image_name + "_c/";
	img.attr('src', image_name + "_c");
	a.href = image_name + "_e";
    } else if( $(window).width() > 250 && $(window).height() > 190) {
	return image_name + "_b/";
	img.attr('src', image_name + "_b");
    } else {
	return image_name + "_a/";
	img.attr('src', image_name + "_a");
    }
}


function get_fitting_image_url(obj) {
    console.log(obj);
    if( obj.width() > 1600 && obj.height() > 1200) {
	return image_name + image_ext;
    } else if( obj.width() > 1400 && obj.height() > 1050) {
	return image_name + "_f" + image_ext;
    } else if( obj.width() > 1067 && obj.height() > 800) {
	return image_name + "_e" + image_ext;
    } else if( obj.width() > 720 && obj.height() > 576) {
	return image_name + "_d" + image_ext;
    } else if( obj.width() > 400 && obj.height() > 300) {
	return image_name + "_c" + image_ext;
    } else if( obj.width() > 250 && obj.height() > 190) {
	return image_name + "_b" + image_ext;
    } else {
	return image_name + "_a" + image_ext;
    }
    

}

//$(document).ready( function() {
//    $('.image')

//$(window).resize( function() {
//    $('.image').each( functon() {
//	sdfsdfsload_fitting_image(this);
//    }
//}); 
