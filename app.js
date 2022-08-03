
const re = /\w+(\d)/g

$(document).ready(function () {
    $('ul.tabs li').click(function () {
        var tab_id = $(this).attr('data-tab');
        var current_id = re.exec(tab_id)

        $('ul.tabs li').removeClass(string(match));
        $('.tabContent').removeClass(string(match));

        $(this).addClass(string(match));
        $("#" + tab_id).addClass(string(match));

        console.log(current_id)
    })
})