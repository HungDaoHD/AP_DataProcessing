(function ($) {

    // msn-overview-chart
    var ctx_msn_overview_prj = $("#msn-overview-chart").get(0).getContext("2d");

    var elm = document.getElementById('msn-overview-json');
    var strVal = elm.value;
    strVal = strVal.replaceAll("'", '"');
    var obj_overview = JSON.parse(strVal);

    delete obj_overview.total;

    var arr_lbl = Object.keys(obj_overview);
    var arr_data = Object.values(obj_overview);

    var msn_overview_prj_chart = new Chart(ctx_msn_overview_prj, {
        type: "bar",
        data: {
            labels: arr_lbl,
            datasets: [{
                backgroundColor: [
                    "rgba(0, 156, 255, .7)",
                    "rgba(0, 156, 255, .5)",
                    "rgba(0, 156, 255, .3)",
                    "rgba(0, 156, 255, .1)"
                ],
                data: arr_data
            }]
        },
        options: {
            responsive: true
        }
    });

})(jQuery);

