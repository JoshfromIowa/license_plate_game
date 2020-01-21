$('.trip').click(function(){
    location.href = $(this).attr('url')
});
$('#open_start').click(function(){
    $('.modal').css('display', 'block')
});
$('#cancel').click(function(){
    $('.modal').css('display', 'none')
    $('#error').html('')
});
$('.modal-content').on('submit', '#start', function(){
    $.ajax({
        method: "POST",
        url: $(this).attr('action'),
        data: $(this).serialize()
    }).done(function(res){
        if (res == 'passed'){
            location.href = '/ongoing'
        }else{
            $('#error').html(res)
        }
    });
    return false
})