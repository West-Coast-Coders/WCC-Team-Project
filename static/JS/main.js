// Sending filter data to the backend

$(document).ready(function () {
    
    $('#filter-form').on('submit', function(event) {

        $.ajax({
            data : {
                imbd_rating : $('#imbd').val(),
                year : $('#year').val(),
                type : $('#type').val(),
                filter : $('#filter').val(),
                order : $('#order').val(),
                audio : $('#audio').val(),
                subtitle : $('#subtitle').val()
            },
            type : 'POST',
            url : '/process'
        })

        event.preventDefault()

    })

})