$(function(){
    $.ajax({
        method: "GET",
        url: "/render_lists"
    }).done(function(res){
        $('#lists').html(res)
    })
});
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
    form = 
    $.ajax({
        method: "POST",
        url: $(this).attr('action'),
        data: $(this).serialize()
    }).done(function(res){
        $('#lists').html(res)
    });
    return false
})