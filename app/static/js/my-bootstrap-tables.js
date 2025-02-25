
// using plugin bootstrap-table - docs: https://bootstrap-table.com/docs/getting-started/introduction/

$(document).ready(function() {
    $('.my-event-bootstrap-table').bootstrapTable({
        cache: false,
        sortName:"my-driver",
        sortOrder:"asc",
        striped: true,
        pagination: true,
        pageSize: 10, //specify 5 here
        pageList: "[10, 20, 50, all]",//list can be specified here
        search: true, // Enable search functionality
        classes: 'table table-borderless table-hover table-striped'
    });

    $("<style>")
        .prop("type", "text/css")
        .html(".fixed-table-container { padding-bottom: 25px !important; }")
        .appendTo("head");
});


