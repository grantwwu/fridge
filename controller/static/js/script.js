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
        //$.get("/items", function(data, status){
	//    alert("Data: " + data + "\nStatus: " + status);
	window.location.reload();
	//});
    });
});
$(function() {
    $('refreshtable').click(function() {
        $.get("/items", function(data, status){
	    if (status = "success") {
		return data;
	    }
	});
    });
});
function updatetable() {
    $.get("/items", function(data, status){
	if (status = "success") {
	    return data;
	}
    });
};
