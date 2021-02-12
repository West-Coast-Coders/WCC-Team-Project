// Sending filter data to the backend

$(document).ready(function () {
    
    $('.filter-form').on('submit', function(event) {

        var filters = {
            "type":$('#type').val(),
            "start_year":$('#start-year').val(),
            "orderby":$('#order').val(),
            "audiosubtitle_andor":$('andor').val(),
            "start_rating":$('#start-rating').val(),
            "end_rating":$('#end-rating').val(),
            "subtitle":$('#subtitle').val(),
            "countrylist":$('#country-list').val(),
            "audio":$('#audio').val(),
            "country_andorunique":$('#andorunique').val(),
            "end_year":$('#end-year').val(),
        }

        $.ajax({
            data : {
                // type : $('#type').val(),
                // start_year : $('#start-year').val(),
                // order_by : $('#order').val(),
                // audiosubtitle_andor : $('andor').val(),
                // start_rating : $('#start-rating').val(),
                // end_rating : $('#end-rating').val(),
                // subtitle : $('#subtitle').val(),
                // country_list : $('#country-list').val(),
                // audio : $('#audio').val(),
                // country_andorunique : $('#andorunique').val(),
                // end_year : $('#end-year').val(),
                // current_list : $('#current-list').val(),
                filter_query : filters
            },
            type : 'POST',
            url : `/${$('#current-list').val()}`
        })

        event.preventDefault()

    })

})