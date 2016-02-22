function ridimensionamentoPagina(){
    if ($(window).width()<600) {
        $('#menuButton').show();
        $('#closeButton').hide();
        $('.menulist').css({position: "absolute",top: -999}).appendTo('body');
    } else {
        $('#menuButton').hide();
        $('#closeButton').hide();
        $('.menulist').css({position: "relative",top: 0}).appendTo($('#nav'));
    }
    $('#menuButton').click(function() {
        $('#closeButton').show();
        $('.menulist').css({position: "relative",top: 0}).appendTo($('#nav'));
        $('#menuButton').hide();
    });

    $('#closeButton').click(function() {
        $('#menuButton').show();
        $('#closeButton').hide();
        $('.menulist').css({position: "absolute",top: -999}).appendTo('body');
    });

    $(window).resize( function() {
    if ($(window).width()<600) {
        $('#menuButton').show();
        $('#closeButton').hide();
        $('.menulist').css({position: "absolute",top: -999}).appendTo('body');
    } else {
        $('#menuButton').hide();
        $('#closeButton').hide();
        $('.menulist').css({position: "relative",top: 0}).appendTo($('#nav'));
    }
});
}
