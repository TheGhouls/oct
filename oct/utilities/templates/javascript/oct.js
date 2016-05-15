$(document).ready(function() {
    $('table.dataTable').DataTable({
        "searching": false
    });
    $('#timersTabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });
    $('table.dataTable').css("width", "100%");
    $('a.enlargeGraph').click(function (e) {
        e.preventDefault();
        var parent = $(this).parent().parent('div');
        if (parent.hasClass("col-md-4")) {
            $(this).parent().parent('div').removeClass("col-md-4");
            $(this).parent().parent('div').addClass("col-md-8");
        } else {
            $(this).parent().parent('div').removeClass("col-md-8");
            $(this).parent().parent('div').addClass("col-md-4");
        }
    });
});
