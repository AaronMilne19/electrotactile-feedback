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
        error: function (error) {
            console.log(error);
        }
    })
}

document.getElementsByName("text_input").forEach(i => i.addEventListener("keypress", (event) => { triggerDevice("textInput") }));