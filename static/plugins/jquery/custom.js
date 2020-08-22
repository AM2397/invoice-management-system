$(document).ready(function(){
    $("#add").click(function(e){
    event.preventDefault()
    var i = $('#items tr').length;
    if(i <= 5) {
    $('#items').append('<tr><td width="500"><input type="text" class="form-control" name="itx_item_desc"/></td>'+
        '<td><input type="text" class="form-control" name="itx_item_quantity"/></td><td><input type="text" class="form-control" name="itx_item_rate"/>'+
        '</td><td><input type="button" value="delete" id="delete" /></td></tr>');
    }
    });

    $('body').on('click', '#delete' , function(e){
        $(this).closest('tr').remove();
    });
});