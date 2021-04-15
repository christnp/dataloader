

// image.preview.js

// a couple of different backgrounds to style the shop
var background1 = 'black';
var background2 = 'firebrick';

var width = 150;
var height = 200;

// this lets us toggle the background state
var color = true;

// every 1 second, switch the background color, alternating between the two styles
// setInterval(function () {
//   document.body.style.backgroundColor = (color ? background1 : background2)
//   color = !color;
// }, 1000);

// function previewImage(input) {
//     if (input.files && input.files[0]) {
//         var reader = new FileReader();

//         reader.onload = function (e) {
//             $('#target')
//             .attr('src', e.target.result)
//             .width(width)
//             .height(height);
//         };

//         reader.readAsDataURL(input.files[0]);
//     }
// }
// Preview image once selected
$("input").change(function(e) {
// TODO: use Jquery to do all of this... instead of a mix
    for (var i = 0; i < e.originalEvent.srcElement.files.length; i++) {
        
        var file = e.originalEvent.srcElement.files[i];
        
        // var img = document.createElement("img");
        var img = document.createElement("img");
        var reader = new FileReader();
        reader.onloadend = function() {
             img.src = reader.result;
        }
        reader.readAsDataURL(file);
        // if the image already exists, use jquery to remove it (we only want one)
        if($('#preview').find('img').length > 0) {
            $("#preview img:last-child").remove()
        }   
        document.getElementById("preview").appendChild(img);
    }
});

// Enable button when image is selected
$(document).ready(
    function(){
        $('input:file').change(
            function(){
                if ($(this).val()) {
                    $('input:submit').attr('disabled',false);
                } 
            }
            );
    });
