var webURL;
var ingredients;

$(function() {
    $('button').click(function() {
        var label = $('#txtLabel').val();
        var amount = $('#intAmount').val();
        var units = $('#txtUnits').val();
        var expdate = $('#dateExpDate').val();
        var picture_id = $('#intImgID').val();
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
    $('modifybutton').click(function() {
	var label = $('#txtLabel').val();
	console.log(label + " label");
	var amount = $('#intAmount').val();
	$.get("/items", function(data, status){
	    if (status = "success") {
		var temp_json = JSON.parse(data);
		console.log(temp_json);
		for(var i=0;i<temp_json.length;i++){
		    var object = temp_json[i];
		    var templabel = object['label'];
		    console.log(templabel);
		    if (templabel.toUpperCase() == label.toUpperCase()) {
			console.log(templabel + " " + object['id'] + " successful match");
			tempurl = "/items/" + object['id'];
			if (amount == 0) {
			    $.ajax({
				url: tempurl,
				data: $('form').serialize(),
				type: 'DELETE',
				success: function(response) {
				    console.log(response);
				},
				error: function(error) {
				    console.log(error);
				}
			    });
			}
			else {
			    $.ajax({
				url: tempurl,
				data: $('form').serialize(),
				type: 'POST',
				success: function(response) {
				    console.log(response);
				},
				error: function(error) {
				    console.log(error);
				}
			    });
			}
			break;
		    }
		    if(i == temp_json.length - 1){
			alert("Item does not exist in Fridge");
		    }
		}
		window.location.reload();
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
