<button></button>
function setData(){
    const tableData = document.getElementById('tableData')
    fetch('{% url "dashboard" %}', {
        method : 'POST',
        headers : {
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'Data':'Hello'}),
    }).then((res) => res.json())
    .then((data) => {
        console.log(data)
        if data.length == 0 {
            console.log('table-div')
            tableData.innerHTML = "<h1>No Data To Display</h1>"
        }
        else{
            displayTable(data,tableData)
        }
    })
}

$.ajax({
    type: 'POST',
    url: "{% url 'deleteData' %}",
    data: {
        id:id,
        csrfmiddlewaretoken:csrftoken
    },
    dataType: 'json',
    success: function(data) {
        alert(data.result)
    }
});


const xhr = new XMLHttpRequest()
        const method = 'GET'
        const url = "{% url 'deleteData' %}"
        const responseType = 'json'
        xhr.responseType = responseType
        xhr.open(method, url)
        xhr.onload = () => {
            console.log(xhr.result)
        }
        xhr.send()
    }
        
    // $.ajax({
    //     type: 'POST',
    //     url: "{% url 'deleteData' %}",
    //     data: {
    //         id:id,
    //         csrfmiddlewaretoken:csrftoken
    //     },
    //     headers : {
    //         'Content-type':'application/json',
    //         'X-CSRFToken':csrftoken,
    //     },
    //     dataType: 'json',
    //     success: function(data) {
    //         alert(data.result)
    //     }
    // });