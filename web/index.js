import "./node_modules/jquery/dist/jquery.js"
import "./node_modules/jquery-ui-dist/jquery-ui.js"

$(document).ready(function () {
    var sliders = $(".slider-handle");
    toDataURL(
        "web/statics/img/test.jpg",
        function (dataUrl) {
            $("#showimg").attr('src', dataUrl).css("height", 800);
        }
    )
    sliders.each(function (index, element) {
        let handle = $(element.getElementsByClassName("ui-slider-handle"));
        let initMapping = { "custom-handle-low-h": 34, "custom-handle-low-s": 0, "custom-handle-low-v": 24, "custom-handle-high-h": 89, "custom-handle-high-s": 173, "custom-handle-high-v": 99 };
        let initValue = initMapping[handle.attr("id")];
        $(element).slider({
            min: 0,
            max: 255,
            step: 1,
            value: initValue,
            create: function () {
                handle.text($(this).slider("value"));
            },
            slide: function (event, ui) {
                handle.text(ui.value);
            },
            stop: function (event, ui) {
                let inputData = getPostData();
                console.log(inputData);
                if (inputData.success) {
                    $.post("/ledDetection", { data: JSON.stringify(inputData.data) }, function (res, status) {
                        $('#processedimg').attr('src', res.result).css("height", 800);
                    }, "json");
                } else {
                    alert("PLS UPLOAD SOME IMAGE");
                }
            }
        });
    });
    $('#uploadfile').change(function () {
        var input = this;
        var url = $(this).val();
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#showimg').attr('src', e.target.result).css("height", 800);
                let inputData = getPostData();
                console.log(inputData)
                if (inputData.success) {
                    $.post("/ledDetection", { data: JSON.stringify(inputData.data) }, function (res, status) {
                        $('#processedimg').attr('src', res.result).css("height", 800);
                    }, "json");
                } else {
                    alert("PLS UPLOAD SOME IMAGE");
                }
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            alert("PLS UPLOAD SOME IMAGE");
        }
    });
    $("#submitBtn").click(function () {
        let inputData = getPostData();
        console.log(inputData);
        if (inputData.success) {
            $.post("/digitRecognize", { data: JSON.stringify(inputData.data) }, function (res, status) {
                $('#processedimg').attr('src', res.result.image).css("height", 800);
                $('#result-value').text(res.result.digits);
            }, "json");
        } else {
            alert("PLS UPLOAD SOME IMAGE");
        }
    });
});

function getPostData() {
    let lowerB = [];
    let upperB = [];
    lowerB.push($("#slider-low-h").slider("value"));
    lowerB.push($("#slider-low-s").slider("value"));
    lowerB.push($("#slider-low-v").slider("value"));
    upperB.push($("#slider-high-h").slider("value"));
    upperB.push($("#slider-high-s").slider("value"));
    upperB.push($("#slider-high-v").slider("value"));
    if ($('#showimg').attr("src") == "#") {
        return { success: false };
    } else {
        return { success: true, data: { img: $('#showimg').attr("src").replace(/^data:image\/(png|jpg);base64,/, ""), lowerb: lowerB, upperb: upperB } };
    }

}

function toDataURL(src, callback, outputFormat) {
    var img = new Image();
    img.crossOrigin = 'Anonymous';
    img.onload = function () {
        var canvas = document.createElement('CANVAS');
        var ctx = canvas.getContext('2d');
        var dataURL;
        canvas.height = this.naturalHeight;
        canvas.width = this.naturalWidth;
        ctx.drawImage(this, 0, 0);
        dataURL = canvas.toDataURL(outputFormat);
        callback(dataURL);
    };
    img.src = src;
    if (img.complete || img.complete === undefined) {
        img.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
        img.src = src;
    }
}

