if ($(window).width()<600) {
    $('#menuButton').show();
    $('.closeButton').hide();
    $('.menulist').hide();
} else {
    $('#menuButton').hide();
    $('.closeButton').hide();
};

$(window).resize( function() {
    if ($(window).width()<600){
        $('#menuButton').show();
        $('.closeButton').hide();
        $('.menulist').hide();
    } else {
        $('#menuButton').hide();
        $('.closeButton').hide();
        $('.menulist').show();
    }
});

$('#menuButton').click(function() {
        $('.closeButton').show();
        $('.menulist').show();
        $('#menuButton').hide();    
});

$('.closeButton').click(function() {
    $('#menuButton').show();
    $('.closeButton').hide();
    $('.menulist').hide();
});