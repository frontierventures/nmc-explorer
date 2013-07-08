$(document).ready(function() {
    $.ajax({
        url: '../loadInventory',
        dataType: 'json',
        success: function(data) {
            results = data;
            $('#results').empty();
            if (results.length == 0) {
                $('#results').append('None Found');
            } else {
                for (var i = 0; i < results.length; i++ ) {
                    $('#results').append('<tr>' + 
                        '<td>' + results[i][0] + '</td>' + 
                        '<td>' + results[i][1] + '</td>' + 
                        '<td>' + results[i][2] + '</td>' + 
                        '<td><a href="../update?name=' + results[i][0] + '" id=' + results[i][0] + '>Update</a></td>' + 
                        '</tr>');
                }
                $('#results').append('<div>Count: ' + results.length  + '</div>');
                $('a[href*=update]').colorbox({
                    inline: true,
                    //showClose: true,
                    href: function() {
                        var name = $(this).attr('id');
                        $('#info').empty();
                        $('#info').append('<h1>' + name + '</h1>');
                        $('input[name=name]').val(name);
                        return "#updateDomainPopup";
                    }
                });
            }
        }
    });
    //return false;
});
$('#updateDomainForm').submit(function() {
    $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        success: function() {
        }
    });
    return true;
});
