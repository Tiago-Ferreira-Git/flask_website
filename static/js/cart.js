$('.add-to-cart').on('click', function () {
    var cart = $('.shopping-cart');
    var imgtodrag = $("#teste, img");
    if (imgtodrag) {
        var imgclone = imgtodrag.clone()
            .offset({
            top: imgtodrag.offset().top,
            left: imgtodrag.offset().left
        })
            .css({
                 'opacity': '0.8',
                'position': 'absolute',
                'height': '10%',
                'width': '3%',
                'z-index': '100'
        })
            .appendTo($('body'))
            .animate({
                'top': cart.offset().top + 10,
                'left': cart.offset().left + 10,
                'width': 60,
                'height': 75
        }, 1000, 'easeInOutExpo');
        setTimeout(function () {
            cart.effect("shake", {
                times: 2
            }, 200);
        }, 1500);

        imgclone.animate({
            'width': 0,
                'height': 0
        }, function () {
            $(this).detach()
        });
    }
});

function adicionA(){
    var elements = document.getElementsByClassName("item");
    $("#Produto1").find("input").attr({"value" : parseInt($("#number1").val())});
    elements[0].dataset.checked = "True";
    document.getElementById("Produto1").style.display = "flex";
    document.getElementById("Produto1").style.visibility = "visible";
    var value1,value2,value3;
    if(document.getElementsByTagName("input")[0].value == null){
        value1 = 0;
    }else{
        value1 = document.getElementsByTagName("input")[0].value;
    }
    if(document.getElementsByTagName("input")[1].value == null){
        value2 = 0;
    }else{
        value2 = document.getElementsByTagName("input")[1].value;
    }
    if(document.getElementsByTagName("input")[2].value == null){
        value3 = 0;
    }else{
        value3 = document.getElementsByTagName("input")[2].value;
    }
    data = Number(value1) * 3 + Number(value2) + Number(value3);
    data = "Preço: " + data + "€";
    document.querySelector('#preço').innerHTML = data;
}
function adicionB(){
    var elements = document.getElementsByClassName("item");
    $("#Produto2").find("input").attr({"value" : parseInt($("#number2").val())});
    elements[1].dataset.checked = "True"
    document.getElementById("Produto2").style.display = "flex";
    document.getElementById("Produto2").style.visibility = "visible";
    var value1,value2,value3;
    if(document.getElementsByTagName("input")[0].value == null){
        value1 = 0;
    }else{
        value1 = document.getElementsByTagName("input")[0].value;
    }
    if(document.getElementsByTagName("input")[1].value == null){
        value2 = 0;
    }else{
        value2 = document.getElementsByTagName("input")[1].value;
    }
    if(document.getElementsByTagName("input")[2].value == null){
        value3 = 0;
    }else{
        value3 = document.getElementsByTagName("input")[2].value;
    }
    data = Number(value1) * 3 + Number(value2) + Number(value3);
    data = "Preço: " + data + "€";
    document.querySelector('#preço').innerHTML = data;
}
function adicionC(){
    var elements = document.getElementsByClassName("item");
    $("#Produto3").find("input").attr({"value" : parseInt($("#number3").val())});;
    elements[2].dataset.checked = "True"
    document.getElementById("Produto3").style.display = "flex";
    document.getElementById("Produto3").style.visibility = "visible";
    var value1,value2,value3;
    if(document.getElementsByTagName("input")[0].value == null){
        value1 = 0;
    }else{
        value1 = document.getElementsByTagName("input")[0].value;
    }
    if(document.getElementsByTagName("input")[1].value == null){
        value2 = 0;
    }else{
        value2 = document.getElementsByTagName("input")[1].value;
    }
    if(document.getElementsByTagName("input")[2].value == null){
        value3 = 0;
    }else{
        value3 = document.getElementsByTagName("input")[2].value;
    }
    data = Number(value1) * 3 + Number(value2) + Number(value3);
    data = "Preço: " + data + "€";
    document.querySelector('#preço').innerHTML = data;
}