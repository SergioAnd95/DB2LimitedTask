
$("#comment-form").submit(function (e) {
    e.preventDefault();
    $form = $(this);
    $form.find('.has-error').removeClass('has-error');
    var form = this;
    $.ajax({
        url: form.action,
        method: form.method,
        data: $form.serialize(),
        dataType: 'json',
        success: function (data) {
            if(data["status"] === "ok") {
                var redirect_url = data['redirect_url'];
                window.location.replace(redirect_url);
            }
            else {
                $.each(data['errors'], function (key, value) {
                    $("#id_"+key).parent().addClass('has-error')
                })
            }
        }
    });
});

$(".toggle_like").on("click", function (e) {
    e.preventDefault();
    $parent = $(this).parent();
    $link = $(this);
    var url = $(this).attr("href");
    $.ajax({
        url: url,
        dataType: "json",
        success: function (data) {
            if(data['status'] === 'ok') {
                if(data['liked']){
                    $link.removeClass("like-disable").addClass("like-active");
                }
                else{
                    $link.removeClass("like-active").addClass("like-disabled");
                }
                $parent.find(".likes_count").text(data['likes_count']);
            }
        }
    })
});
