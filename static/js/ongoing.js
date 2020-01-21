$(function(){
    $.ajax({
        method: "GET",
        url: "/render_lists"
    }).done(function(res){
        $('#lists').html(res)
    });
    $.ajax({
        method: "GET",
        url: "/trip_time"
    }).done(function(res){
        $('#current_time').text(res)
    })
});
setInterval(function(){
    $.ajax({
        method: "GET",
        url: "/trip_time"
    }).done(function(res){
        $('#current_time').html(res)
    })
}, 1000);
$('#lists').on('click', '.found', function(){
    $.ajax({
        method: "GET",
        url: $(this).attr('href')
    }).done(function(res){
        $('#lists').html(res)
    });
    return false
});
$('#lists').on('submit', '.new', function(){
    $.ajax({
        method: "POST",
        url: $(this).attr('action'),
        data: $(this).serialize()
    }).done(function(res){
        $('#lists').html(res)
    });
    return false
});
$('#open_end').click(function(){
    $('.modal').css('display', 'block')
});
$('#cancel').click(function(){
    $('.modal').css('display', 'none')
});
