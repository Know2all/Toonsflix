function last_date_of_month(){
    var currentDate = new Date();
    currentDate.setMonth(currentDate.getMonth() + 1);
    currentDate.setDate(0);
    var lastDayOfMonth = currentDate.toISOString().slice(0, 10);
    return lastDayOfMonth;
}

function first_date_of_month() {
    var currentDate = new Date();
    currentDate.setDate(1);
    var firstDayOfMonth = currentDate.toISOString().slice(0, 10);
    return firstDayOfMonth;
}

$('.removeItem-btn').on('click',function(e){
    var id = $(this).data('id');
    var tbl = $(this).data('table');

    $.ajax({
        url:'/api/removeItem',
        method:'POST',
        data:{'id':id,'table':tbl},
        success:function(response){
            if(response.status){
                alert(response.message);
            }else{
                alert(response.error);
            }
            location.reload();
        },
        error:function(xhr,status,err){
            console.log(err);
        }
    });
});

$('.receiptPrint-btn').on('click',function(e){
    var row = $(this).closest('tr');
    var lrno = $(this).data('lrno');
    var printType = row.find('.form-select').val();
    window.location.href=`receipt?lrno=${lrno}&type=${printType}`;
});

$('.clear-btn').on('click', function(e) {
    if (confirm("Are You Sure To Clear")) {
        var currentUrl = window.location.href;
        window.location.href = currentUrl;
    }
});
