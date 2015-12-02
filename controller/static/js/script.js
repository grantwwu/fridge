$(function() {
    $('button').click(function() {
        var label = $('#txtLabel').val();
	var amount = $('#intAmount').val();
        var units = $('#txtUnits').val();
        var expdate = $('#dateExpDate').val();
        var imgid = $('#intImgID').val();
        $.ajax({
            url: '/add',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
	window.location.reload();
    });
});
$(function() {
    $('updatebutton').click(function() {
       	window.location.reload();
    });
});
$(function() {
    $('deletebutton').click(function() {
	var label = $('#txtLabel').val();
	var amount = $('#intAmount').val();
        $.ajax({
            url: '',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
	window.location.reload();
    });
});
function updatetable() {
    $.get("/items", function(data, status){
	if (status = "success") {
	    return data;
	}
    });
};
