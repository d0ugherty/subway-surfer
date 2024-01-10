/**
 *  Updates the arrivals table at a specified interval
 * 
 *  This replaces the table body without having to refresh the page
 */
function update_table(csrf_token, station, tableId) {
    setInterval(function() {
        $.ajax({
            type: "POST",
            url: "/update_arrivals_table/" + tableId + "/",
            data: { 'station': station,
                    'csrfmiddlewaretoken': csrf_token},
            cache: false
        })
        .done(function(response) {
            $('#' + tableId + ' tbody').html(response.html);
        });
    }, 2000);  
}