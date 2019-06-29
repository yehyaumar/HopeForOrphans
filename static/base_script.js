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

function set_csrftoken() {
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        },
    });
}

function post_req(txt, url) {
    set_csrftoken();

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

function run_ajax(e) {
    // e.preventDefault()
        amount = $('input[name=amount]').val().trim();
        firstname = $('input[name=firstname]').val().trim();
        email = $('input[name=email]').val().trim();
        productinfo = $('textarea[name=productinfo]').val().trim();
        phone = $('input[name=phone]').val().trim();
        orphanage_pk = $('#orphanage_pk').text();
        $('input[name=udf1]').val(orphanage_pk);
        udf1 = $('input[name=udf1]').val();

        console.log(orphanage_pk);
        set_csrftoken();

        data = {
            'amount': amount,
            'firstname': firstname,
            'email': email,
            'productinfo': productinfo,
            'phone': phone,
            'udf1': udf1,
        };

        $.ajax({
            url: '/donate/'+orphanage_pk,
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (data) {
                if (data){
                    console.log(data);

                    $('input[name=key]').val(data.merchant_key);
                    $('input[name=hash]').val(data.hashh);

                    $('input[name=hash_string]').val(data.hash_string);
                    $('input[name=txnid]').val(data.txnid);

                    $('input[name=surl]').val(data.surl);
                    $('input[name=furl]').val(data.furl);
                    $('input[name=service_provider]').val(data.service_provider);

                    var payuForm = document.forms.payuForm;
                    payuForm.action = data.action;
                    payuForm.submit();
                }
            }
        });
    }

jQuery(document).ready(function ($) {
    $('form[name=payuForm]').submit(run_ajax)
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
        handler($('.checkbox-wrap:eq(0)'), $('#txt_add_facility'), 'facilities', '/home/ajax/add_facility');

    });
    $("#btn_add_income_src").click(function () {
        handler($('.checkbox-wrap:eq(1)'), $('#txt_add_income_src'), 'income_source', '/home/ajax/add_income_src');

    });

    var len = $('.orphans-pk').length;
    console.log(len);


    $('.delete-buttons').on("click", function (event) {
        var target = $(event.target);
        var pk = target.parent().parent().find('span').first().text();
        set_csrftoken();

        $.ajax({
            type: 'POST',
            url: 'ajax/delete-orphan',
            data: {
                'pk': pk
            },
            dataType: 'json',

            success: function (data) {
                if (data.success) {
                    location.reload();
                    console.log('Success')
                } else
                    console.log('Failure')
            }
        });
    });

    $('.edit-buttons').on("click", function (event) {
        var target = $(event.target);
        var pk = target.parent().parent().find('span').first().text();

        window.location = "/home/edit-orphan/" + pk;
    });

    //Modal
        var modal = $('#myModal');

    // var modal = document.getElementById('myModal');
    let pk;
    $('.adopt-request').click(function () {

        $.ajax({
            url: '/ajax/adopt_request',
            type: 'get',
            beforeSend: function () {
                modal.css('display', 'block');

            },

            success: function (data) {
                $('#myModal .modal-content').html(data.html_form);
            }
        });
        var target = $(event.target);
        pk = target.parent().parent().find('span').first().text();
    });

    modal.on('click', '.close',function () {
        modal.css('display', 'none');
    });

    modal.on('click', '.close-button',function () {
        modal.css('display', 'none');
    });

    modal.on('submit', '.adopt-request-form', function () {
        var form = $(this);
        data = form.serialize();
        console.log(pk);
        data = data+'&pk='+pk;
        set_csrftoken();
        $.ajax({
            url: '/ajax/adopt_request',
            data: data,
            type: form.attr('method'),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid){
                    console.log('Success');
                    $('#myModal .modal-content').fadeOut(30, function () {
                        $('#myModal .modal-content').html(data.success_page).fadeIn();
                        $('.request-id').text(data.req_id)

                    });
                }else {
                    $('#myModal .modal-content').html(data.html_form);
                }
            }
        });
        return false;
    });

    $(window).click(function (event) {
        if ($(event.target).attr('id') === modal.attr('id')) {
            modal.css('display', 'none');

        }
    });

    let request_id;
    $('.card-table-row').click(function () {
        var target = $(event.target);

        request_id = target.parent().children().eq(1).text().trim();

        console.log(request_id);
        if (request_id) {
            $.ajax({
                url: 'ajax/adoption_approval',
                data: {'request_id': request_id},
                type: 'get',
                beforeSend: function () {
                    modal.css('display', 'block');
                },

                success: function (data) {
                    $('#myModal .modal-content').html(data.html_form);
                }
            });
        }
    });


    modal.on('submit', '.adoption-request-details', function () {
        var form = $(this);
        data = form.serialize();
        data = data+'&request_id='+request_id;
        set_csrftoken();
        $.ajax({
            url: 'ajax/adoption_approval',
            data: data,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid){
                    $('#myModal .modal-content').fadeOut(30);
                    location.reload();
                }
            }
        });
        return false;
    });

});