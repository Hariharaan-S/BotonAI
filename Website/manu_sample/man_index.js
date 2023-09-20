const imageInput = document.getElementById("images");
const imagePreview = document.getElementById("image-preview");
const dropcontainerElement = document.getElementById("dropcontainer");
const clr = document.getElementById("clear");

clr.addEventListener("click", function () {
    imageInput.value = "";
    document.querySelector(".output").style.display = "none";
    dropcontainerElement.style.display = "flex";
    document.getElementById("identify").value = "";
    document.getElementById("verified").innerHTML = "";
    document.getElementById("predict_output").innerHTML = "";
    document.getElementById("predict_img").src = "";
    imagePreview.style.display = "none";
});

$('#images').on('change', function () {
    var imageInput = this;
    var imagePreview = $('#image-preview');

    if (imageInput.files && imageInput.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            imagePreview.attr('src', e.target.result);

            imagePreview.css('display', 'block');

            $('#dropcontainer').css('display', 'none');
        };

        reader.readAsDataURL(imageInput.files[0]);
    } else {
        imagePreview.css('display', 'none');
        $('#dropcontainer').css('display', 'block');
    }
});

$(document).ready(function () {
    $("#submit").click(function () {
        var formData = new FormData();
        var raw = document.getElementById("identify");
        const raw_material_name = raw.value;
        var verify = document.getElementById("verified")
        const res = document.getElementById("predict_output");
        formData.append("image", $("#images")[0].files[0]);

        $.ajax({
            type: "POST",
            url: "/predict",
            contentType: false,
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function () {
                $('#loading').css("visibility", "visible");
            },
            success: function (response) {
                document.querySelector(".output").style.display = "block";
                const temp = response.split("$");
                const t1 = temp[0].split(":");
                const t2 = temp[1].split(":");
                const t3 = temp[2].split(":");
                const t4 = temp[3].split(":");
                const name = t1[1];
                const spe = t2[1];
                const desc = t3[1];
                const hab = t4[1];
                if (name.trim() === raw_material_name) {
                    $("#name").text(name);
                    $("#species").text(spe);
                    $("#description").text(desc);
                    $("#habitat").text(hab);
                    document.getElementById("predict_img").src = "static\\predict_image\\" + name.trim() + ".jpg";
                    res.innerHTML = "Identified as " + raw_material_name;
                    verify.innerHTML = '<lottie-player class="verify_icon" src="https://lottie.host/712cc0d7-0319-445b-80b7-ed662a3d4db3/9idUOQtExU.json" background="transparent" speed="1" style="width: 300px; height: 300px;" loop autoplay></lottie-player>';
                }
                else {
                    verify.innerHTML = '<lottie-player class="verify_icon" src="https://lottie.host/fdfcdf78-8b44-4d5c-a6ed-0daaedc20483/3HUQ76oYY8.json" background="transparent" speed="1" style="width: 250px; height: 250px; margin-top: 20px; margin-left: 15px;" loop autoplay></lottie-player>';
                    res.innerHTML = "Fake Raw Material or Wrong Raw Material";
                    document.querySelector(".output").style.display = "none";
                }
            },
            complete: function () {
                $('#loading').css("visibility", "hidden")
            },
            error: function () {
                $("#prediction-result").text("Error: Unable to make a prediction.");
            }
        });
    });

    $("#capture").click(function () {
        var formData = new FormData();
        formData.append("image", $("#live_image"));
        $.ajax({
            type: "POST",
            url: "/capture",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                const temp = response.split("$");
                const t1 = temp[0].split(":");
                const t2 = temp[1].split(":");
                const t3 = temp[2].split(":");
                const t4 = temp[3].split(":");
                const name = t1[1];
                const spe = t2[1];
                const desc = t3[1];
                const hab = t4[1];
                $("#name").text(name);
                $("#species").text(spe);
                $("#description").text(desc);
                $("#habitat").text(hab);
                document.getElementById("predict_img").src = "static\\predict_image\\" + name.trim() + ".jpg";
            },
            error: function () {
                $("#prediction-result").text("Error: Unable to make a prediction.");
            }
        });

    });

    $("#view_report").on("click", function () {
        $.ajax({
            type: "POST",
            url: "/report",
            contentType: "application/json;charset=UTF-8",
            data: JSON.stringify({ 'sup_id': "2" }),
            success: function (response) {
                $("body").html(response);
            }
        });
    });

    // setInterval(function () {
    //     document.getElementById('image').src = "{{url_for('video_feed')}}?" + new Date().getTime();
    // }, 1000);

    // function captureAndSend() {

    //     const result = fetch('/predict').then(response => response.json()).then(data => {
    //         const temp = data.split("$");
    //         const t1 = temp[0].split(":");
    //         const t2 = temp[1].split(":");
    //         const t3 = temp[2].split(":");
    //         const t4 = temp[3].split(":");
    //         const name = t1[1];
    //         const spe = t2[1];
    //         const desc = t3[1];
    //         const hab = t4[1];
    //         $("#name").text(name);
    //         $("#species").text(spe);
    //         $("#description").text(desc);
    //         $("#habitat").text(hab);
    //         document.getElementById("predict_img").src = "static\\predict_image\\" + name.trim() + ".jpg";
    //     })
    // }
});

$("#capture").click(function () {

    var formData = new FormData();
    formData.append("image", $("#live_image"));
    $.ajax({
        type: "POST",
        url: "/capture",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            const temp = response.split("$");
            const t1 = temp[0].split(":");
            const t2 = temp[1].split(":");
            const t3 = temp[2].split(":");
            const t4 = temp[3].split(":");
            const name = t1[1];
            const spe = t2[1];
            const desc = t3[1];
            const hab = t4[1];
            $("#name").text(name);
            $("#species").text(spe);
            $("#description").text(desc);
            $("#habitat").text(hab);
            document.getElementById("predict_img").src = "static\\predict_image\\" + name.trim() + ".jpg";
        },
        error: function () {
            $("#prediction-result").text("Error: Unable to make a prediction.");
        }
    });

});

//scroll animation
ScrollReveal({ distance: '80px', duration: 1500, delay: 100 });
ScrollReveal().reveal('.side-nav', { origin: 'left' });
ScrollReveal().reveal('.logo_img', { origin: 'top', delay: 330 })
ScrollReveal().reveal('.identify_header , .wrap_container', { origin: 'top' });
ScrollReveal().reveal('.drop-container, .predict_output, .view_report, .outer', { origin: 'bottom' });