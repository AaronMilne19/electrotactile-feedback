function triggerDevice(type) {
    var csrf = document.getElementsByName('csrfmiddlewaretoken');
    $.ajax({
        type: 'post',
        url: '/trigger/',
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'widgetType': type,
        },
        dataType: 'json',
        success: function (response) {
            console.log(response);
        },
        error: function (error) {
            console.log(error);
            alert('Oops, something went wrong!');
        }
    })
}