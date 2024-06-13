var current_date = '';
waitForElement('.insert_dates .dateelement').then(function (element) {
    element.click();
});
// fetch today's content from the mongodb collection
function todays_content() {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/api/default_content',
            type: 'GET',
            success: function (response) {
                resolve(response.content)
            },
            error: function (xhr, status, error) {
                console.log('Error:', error)
                reject('Type Your Markdown Here ...')
            },
        })
    })
}
// function to insert dates into the section
function loaddates() {
    $.ajax({
        url: '/api/date',
        type: 'GET',
        success: function (response) {
            // Handle the response from the server
            let dates = response['dates']
            let html = ''
            for (let i = 0; i < dates.length; i++) {
                if (i == 0) {
                    html += `<a href="#"
            class="dateelement text-[#007F73] p-1 rounded rounded-md shadow shadow-lg text-lg">${dates[i]}
        </a><hr>`
                } else {
                    html += `<a href="#"
            class="dateelement text-[#007F73] p-1 rounded rounded-md shadow shadow-lg text-lg">${dates[i]}
        </a><hr>`
                }
            }
            $('.insert_dates').append(html)
        },
        error: function (xhr, status, error) {
            // Handle errors
            console.error('Error:', error)
        },
    })
}

function todoadder() {
    // AJAX POST request
    $.ajax({
        type: 'POST',
        url: '/fetch_tags',
        contentType: 'application/json',
        data: JSON.stringify({ tag: 'todo' }),
        success: function (response) {
            var contents = response['todos']
            var dates = response['dates']
            let html = ``
            for (let i = 0; i < contents.length; i++) {
                html += `<div class="flex items-center justify-between bg-transparent px-4 rounded-md">
                  <!-- Checkbox -->
                  <input type="checkbox" class="mr-2 finishtask">
  
                  <!-- Date -->
                  <div class="flex-grow mr-2">
                      <p class="date w-full py-1 px-2">${dates[i]}</p>
                  </div>
  
                  <!-- Content with overflow hidden -->
                  <div class="flex-grow overflow-hidden content">
                      ${contents[i]}
                  </div>
              </div>
              `
                $('#todolist').html(html)
            }
        },
        error: function (xhr, status, error) {
            console.log('Error:', error)
        },
    })
}
function completeloader() {
    $.ajax({
        type: 'POST',
        url: '/fetch_completes',
        contentType: 'application/json',
        data: JSON.stringify({ tag: 'completed' }),
        success: function (response) {
            var contents = response['todos']
            var dates = response['dates']
            let html = ``
            for (let i = 0; i < contents.length; i++) {
                html += `<div class="flex items-center justify-between bg-transparent px-4 py-1 rounded-md">
                  <!-- Checkbox -->
                  <button class="bg-[#092635] hover:bg-red-600 text-white font-bold p-2 rounded revert">
                      Revert
                  </button>
  
                  <!-- Date -->
                  <div class="flex-grow mr-2">
                      <p class="date w-full py-1 px-2">${dates[i]}</p>
                  </div>
  
                  <!-- Content with overflow hidden -->
                  <div class="flex-grow overflow-hidden content">
                      ${contents[i]}
                  </div>
              </div>
              `
                $('#donelist').html(html)
            }
        },
        error: function (xhr, status, error) {
            console.log('Error:', error)
        },
    })
}
setInterval(todoadder, 60000);
setInterval(completeloader, 60000);
// functions to check the corresponding tabs for the tasks
$('#todo').click(function () {
    $(this).addClass('bg-[#9EC8B9]')
    $(this).addClass('text-[#1B4242]')
    $('#done').removeClass('text-[#1B4242] bg-[#9EC8B9]')
    $('#todolist').addClass('bg-[#9EC8B9]')
    $('#todolist').addClass('text-[#1B4242]')
    $('#donelist').addClass('hidden')
    $('#todolist').removeClass('hidden')
    todoadder();
})
$('#done').click(function () {
    $('#todo').removeClass('text-[#1B4242] bg-[#9EC8B9]')
    $(this).addClass('text-[#1B4242] bg-[#9EC8B9]')
    $('#donelist').addClass('text-[#1B4242] bg-[#9EC8B9]')
    $('#donelist').removeClass('hidden')
    $('#todolist').addClass('hidden')
    completeloader();
})

// functions to change the state of activities
$(document).on('click', '.finishtask', function () {
    // Check if the checkbox is checked
    if ($(this).is(':checked')) {
        // Checkbox is checked
        // Perform your desired action here
        let text = $(this).parent().find('.content').text()
        let date = $(this).parent().find('.date').text()
        text = text.trim()
        date = date.trim()
        $.ajax({
            type: 'POST',
            url: '/finish_task',
            contentType: 'application/json',
            data: JSON.stringify({ date: date, text: text }),
            success: function (response) {
                if (response == 'successful') {
                    // window.location.reload()
                    todoadder();
                    completeloader();
                    if (current_date == date) {
                        $.ajax({
                            type: 'POST',
                            url: '/get_date_text',
                            contentType: 'application/json',
                            data: JSON.stringify({ date: date }),
                            success: function (response) {
                                eraser()
                                $('#current_date_selection').text(date)
                                createEditor(response['text'])
                            },
                            error: function (xhr, status, error) {
                                console.log('Error:', error)
                            },
                        })
                    }
                }
            },
            error: function (xhr, status, error) {
                console.log('Error:', error)
            },
        })
    }
})
$(document).on('click', '.revert', function () {
    // Perform your desired action here
    let text = $(this).parent().find('.content').text()
    let date = $(this).parent().find('.date').text()
    text = text.trim()
    date = date.trim()
    $.ajax({
        type: 'POST',
        url: '/revert_task',
        contentType: 'application/json',
        data: JSON.stringify({ date: date, text: text }),
        success: function (response) {
            if (response == 'successful') {
                if (response == 'successful') {
                    // window.location.reload()
                    todoadder();
                    completeloader();
                    if (current_date == date) {
                        $.ajax({
                            type: 'POST',
                            url: '/get_date_text',
                            contentType: 'application/json',
                            data: JSON.stringify({ date: date }),
                            success: function (response) {
                                eraser()
                                $('#current_date_selection').text(date)
                                createEditor(response['text'])
                            },
                            error: function (xhr, status, error) {
                                console.log('Error:', error)
                            },
                        })
                    }
                }
            }
        },
        error: function (xhr, status, error) {
            console.log('Error:', error)
        },
    })
})
// function to get the data based on current date
$(document).on('click', '.dateelement', function () {
    let date = $(this).text().trim()
    current_date = date;
    alert(`I called this function for the date : ${date}`)
    $.ajax({
        type: 'POST',
        url: '/get_date_text',
        contentType: 'application/json',
        data: JSON.stringify({ date: date }),
        success: function (response) {
            eraser()
            $('#current_date_selection').text(date)
            createEditor(response['text'])
        },
        error: function (xhr, status, error) {
            console.log('Error:', error)
        },
    })
})

function eraser() {
    var elements = document.querySelectorAll('a.dateelement')

    // Loop through each element
    elements.forEach(function (element) {
        // Check if the element has class 'dummy'
        if (element.classList.contains('bg-[#F0F3FF]')) {
            // Remove the class 'dummy'
            element.classList.remove('bg-[#F0F3FF]')
        }
    })
}
var regex = /^(0[1-9]|1[0-2])\/(0[1-9]|1\d|2\d|3[01])\/(19|20)\d{2}$/;
$("#add_new_date").click(function () {
    let new_date = $("#new_date_input").val();
    if (regex.test(new_date)) {
        $.ajax({
            type: 'POST',
            url: '/add_new_date',
            contentType: 'application/json',
            data: JSON.stringify({ date: new_date }),
            success: function (response) {
                if (response == 'Successfully Added Document') {
                    // Select all elements with the class 'dateelement' inside elements with the class 'insert_dates'
                    var dateElements = document.querySelectorAll('.insert_dates .dateelement');

                    // Loop through each selected element and remove it
                    dateElements.forEach(function (element) {
                        element.parentNode.removeChild(element);
                    });
                    $("#new_date_child").addClass('hidden');
                    loaddates()
                }
                else if (response == 'Record Already Exists') {
                    alert(response);
                }
            },
            error: function (xhr, status, error) {
                console.log('Error:', error)
            },
        })
    }
    else alert('invalid date format');
})