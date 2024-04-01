$(document).ready(function () {
    $('#file').on('change', function(){
        let file = this.files[0];
        $('.file-input-name').html(file.name);
    });
});

/*
 $(".encrypt__form").on("submit", function (event) {
        event.preventDefault();
        let data = $(this).serialize();
        let file = $("#file-input").val();

        $.ajax({
            url: $(this).attr("action"),
            type: $(this).attr("method"),
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                password: data.split("=")[1]
            }),

            error: function(data){
                console.log("error", data.responseText);
            }
        });
    });
*/