const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const getDetails =(id)=> {
    const csrftoken = getCookie('csrftoken')
    console.log(csrftoken)
    console.log('hello ' + id)

    $.ajax({
        type: 'POST',
        url: "{% url 'deleteData' %}",
        data: {
            id:id,
            csrfmiddlewaretoken:csrftoken
        },
        headers : {
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        dataType: 'json',
        success: function(data) {
            alert(data.result)
        }
    }) 
}
