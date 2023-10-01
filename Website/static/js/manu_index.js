const imageInput = document.getElementById("images");
const imagePreview = document.getElementById("image-preview");
const dropcontainerElement = document.getElementById("dropcontainer");
var cap = false;

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
    document.getElementById("camera").style.display = "none";
    document.getElementById("send").style.display = "none";
    document.getElementById("capture_out").style.display = "none";
    document.getElementById("capture").style.display = "none";
    $("#submit").click(function () {
        var formData = new FormData();
        var raw = document.getElementById("manu-identify");
        const raw_material_name = raw.value.toLowerCase();
        if (raw_material_name !== "") {
            var verify = document.getElementById("verified")
            const res = document.getElementById("predict_output");
            formData.append("image", $("#images")[0].files[0]);
            var url = "/predict?raw_material_name=" + encodeURIComponent(raw_material_name);

            $.ajax({
                type: "POST",
                url: url,
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
                    const name = t1[1].trim().toLowerCase();
                    const spe = t2[1];
                    const desc = t3[1];
                    const hab = t4[1];
                    const f1 = raw_material_name.split(/[\s-]/);
                    if ((name.includes(raw_material_name) || f1[0] === name.split("-")[0] || f1[1] === name.split("-")[1] || name.startsWith(raw_material_name) || f1[1] && name.split("-")[1].startsWith(f1[1]))) {
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
        }
        else {
            alert("Enter the Raw Material Name");
        }
    });


    $("#toggle").click(function () {
        $("#camera").toggle();
        if ($("#camera").is(":visible")) {
            document.getElementById("capture_out").style.display = "none";
            $("#buttons").css("display", "flex");
            $("#send").css("display", "block");
            $("#dropcontainer").css("display", "none");
            $("#capture").css("display", "flex");
            $("#submit").css("display", "none");

        } else {
            $("#send").css("display", "none");
            $("#dropcontainer").css("display", "flex");
            $("#submit").css("display", "block");
            $("#send").css("display", "none");
            $("#capture").css("display", "none");
            document.getElementById("capture_out").style.display = "none";
        }
    });
    $("#clear").click(function () {
        if (cap) {
            document.getElementById("capture_out").style.display = "none";
            $("#buttons").css("display", "flex");
            $("#send").css("display", "block");
            $("#dropcontainer").css("display", "none");
            $("#capture").css("display", "flex");
            $("#submit").css("display", "none");
            $("#camera").show();
            $("#verified").text("");
            $("#predict_output").text("");
            $("#manu-identify").text("");
            cap = false;

        } else {
            $("#send").css("display", "none");
            $("#dropcontainer").css("display", "flex");
            $("#submit").css("display", "block");
            $("#capture").css("display", "none");
            $("#capture_out").css("display", "none");
            $("#camera").hide();
            $("#verified").text("");
            $("#predict_output").text("");
            $("#manu-identify").text("");
        }

    });

    $("#capture").click(function () {
        cap = false;
        $("#camera").hide();
        document.getElementById("capture_out").style.display = "flex";
        Webcam.snap(function (data_uri) {
            document.getElementById("capture_out").innerHTML = '<img id="capture_image" src="' + data_uri + '"/>';
        })
    });

    $("#view_report").on("click", function () {
        var username = document.getElementById("supplier").value;
        console.log(username);
        $.ajax({
            type: "POST",
            url: "/report",
            contentType: "application/json;charset=UTF-8",
            data: JSON.stringify({ 'sup_id': username }),
            success: function (response) {
                $("body").html(response);
            }
        });
    });
});

$("#send").click(function () {
    var formData = new FormData();
    var raw = document.getElementById("manu-identify");
    const raw_material_name = raw.value.toLowerCase();
    console.log(raw_material_name);
    if (raw_material_name !== "") {
        var verify = document.getElementById("verified")
        const res = document.getElementById("predict_output");
        var send_image = document.getElementById("capture_image").src;
        formData.append("image", send_image);
        var url = "/capture?raw_material_name=" + encodeURIComponent(raw_material_name);
        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function () {
                $('#loading').css("visibility", "visible");
            },
            success: function (response) {
                console.log(response);
                if (response.prediction !== null) {
                    const temp = response.prediction.split("$");
                    const t1 = temp[0].split(":");
                    const t2 = temp[1].split(":");
                    const t3 = temp[2].split(":");
                    const t4 = temp[3].split(":");
                    const name = t1[1].trim().toLowerCase();
                    const nm = name.replace(/[^a-zA-Z]/g, '');
                    const rw = raw_material_name.replace(/[^a-zA-Z]/g, '');
                    const spe = t2[1];
                    const desc = t3[1];
                    const hab = t4[1];

                    if (raw_material_name != null) {
                        if (nm.includes(rw)) {
                            document.querySelector(".output").style.display = "block";
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
                    }
                    else {
                        verify.innerHTML = '<lottie-player class="verify_icon" src="https://lottie.host/fdfcdf78-8b44-4d5c-a6ed-0daaedc20483/3HUQ76oYY8.json" background="transparent" speed="1" style="width: 250px; height: 250px; margin-top: 20px; margin-left: 15px;" loop autoplay></lottie-player>';
                        res.innerHTML = "Fake Raw Material or Wrong Raw Material";
                        document.querySelector(".output").style.display = "none";
                    }
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
    }
    else{
        alert("Enter the raw material name");
    }

});

Webcam.set({
    width: 400,
    height: 300,
    image_format: 'jpeg',
    jpeg_quality: 100
});
Webcam.attach("#camera");
//scroll animation
