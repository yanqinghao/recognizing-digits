// import 'https://code.jquery.com/jquery-3.3.1.min.js'
// import 'https://code.jquery.com/ui/1.12.1/jquery-ui.js'
import "./node_modules/jquery/dist/jquery.js"
import "./node_modules/jquery-ui-dist/jquery-ui.js"
// import "./node_modules/jquery-ui-dist/jquery-ui.css"
// window.$ = $
// window.$ = window.jQuery = require('jquery');

$(document).ready(function () {
    var sliders = $(".slider-handle");
    sliders.each(function (index, element) {
        var handle = $(element.getElementsByClassName("ui-slider-handle"));
        $(element).slider({
            min: 0,
            max: 255,
            step: 1,
            value: 0,
            create: function () {
                handle.text($(this).slider("value"));
            },
            slide: function (event, ui) {
                handle.text(ui.value);
            }
        });
    });
    $("#slider-high-s").slider("value", 255);
    $("#slider-high-v").slider("value", 255);
});