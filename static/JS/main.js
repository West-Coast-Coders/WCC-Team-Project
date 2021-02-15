// Sending filter data to the backend

$(document).ready(function () {
    
    $('.filter-form').on('submit', function(event) {

        var filters = {
            type: $('#type').val(),
            start_year: $('#start-year').val(),
            end_year: $('#end-year').val(),
            start_rating: $('#start-rating').val(),
            end_rating: $('#end-rating').val(),
            min_runtime: $('#min-runtime').val(),
            max_runtime: $('#max-runtime').val()
        }

        $.ajax({
            data : JSON.stringify(filters),
            type : 'POST',
            url : `/${$('#current-list').val()}`,
            dataType : 'json',
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                $.ajax({
                    type: 'GET',
                    url: `/${$('#current-list').val()}`,
                    data: data,
                });
            }
        })

        event.preventDefault()

    })

})