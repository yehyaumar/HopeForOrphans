function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function post_req(txt, url) {
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        },
    });

    $.ajax({
        url: url,
        type: 'POST',
        data: {
            'value': txt
        },
        dataType: 'json',

        success: function (data) {
            if (data.success) {
                console.log('Success')
            } else
                console.log('Failure')
        }
    });

}

function addCheckBox(container, name, value) {
    var labels = container.find('label');
    var inputs = container.find('input');
    var id = labels.length + 1;
    var id_lbl = 'id_' + name + '_' + id;

    var lbl = $('<label />', {'for': id_lbl, class: 'checkbox-container'});
    lbl.insertAfter(labels.last());

    $('<input />', {type: 'checkbox', name: name, id: id_lbl, value: id}).appendTo(lbl);
    lbl.append("<span class='checkbox-label'>" + value + '</span>');
    lbl.append("<span class='checkbox-mark'></span>");

}

function handler(container, txt_box, name, url) {

    let txt = txt_box.val();
    if (txt_box.css('display') === 'none') {
        txt_box.fadeIn();
    } else if (txt === '') {
        txt_box.css('border', '1px solid red')
    } else {
        post_req(txt, url);
        addCheckBox(container, name, txt);

        txt_box.val('');
        txt_box.css('border', 'none');

        txt_box.fadeOut();
    }

}

jQuery(document).ready(function ($) {
    $(".accordian").on("click", ".card-div", function () {
        $(this).toggleClass("active").next().slideToggle();
    });

    $(".checkbox-wrap").on("click", "#facility-div", function () {
        $(this).toggleClass("active").next().slideToggle();
    });
    $(".checkbox-wrap").on("click", "#income-div", function () {
        $(this).toggleClass("active").next().slideToggle();
    });



    $("#btn_add_facility").click(function () {
        handler($('.checkbox-wrap:eq(0)'), $('#txt_add_facility'), 'facilities', '/ajax/add_facility');

    });
$("#btn_add_income_src").click(function () {
        handler($('.checkbox-wrap:eq(1)'), $('#txt_add_income_src'), 'income_source', '/ajax/add_income_src');

    });

});