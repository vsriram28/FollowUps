/*
Function to create the code editor.
The argument to be passed is the text displayed on the code editor.
The function checks if a code editor is already available and destroys
it before creating a new one. Also the content on the text editor will
be saved in a local file.
*/
function createEditor(content) {
  // Fetch data from Flask using AJAX
  require.config({
    paths: {
      vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.26.1/min/vs',
    },
  })
  require(['vs/editor/editor.main'], function () {
    try {
      destroyEditor()
    } catch {
      console.log('no editor available')
    }
    console.log('started with the editor')
    let editor = monaco.editor.create(document.getElementById('editor'), {
      value: [content].join('\n'),
      language: 'markdown', // Use Markdown language
      theme: 'vs-dark',
      automaticLayout: true,
    })
    editor.onDidChangeModelContent(function (event) {
      // Autosave content to server
      saveContent(editor.getValue())
    })
  })
}
/*
Function to destroy the existing code editor before establishing the
 new one. This function does not take any args.
*/
function destroyEditor() {
  let editor = monaco.editor.getModels()[0]
  if (editor) {
    editor.dispose()
  }
}
/*
Function takes the code editor content and saves it as is in a local
file of suitable format.
*/
function saveContent(content) {
  fetch('/save', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'markdown_content=' + encodeURIComponent(content),
  })
}
// Calling the createEditor function when the page is initialized
window.onload = function () {
  $('#todo').click();
  loaddates()
  var dateElement = document.querySelector('.insert_dates .dateelement');
  // Check if the element exists before attempting to click it
  todays_content()
    .then(content => {
      console.log(content);
      createEditor(content) // Handle the content here
    })
    .catch(error => {
      console.error(error); // Handle errors here
    });
}
function waitForElement(selector) {
  return new Promise(function (resolve, reject) {
    var observer = new MutationObserver(function (mutations) {
      var element = document.querySelector(selector);
      if (element) {
        observer.disconnect();
        resolve(element);
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  });
}

//   Generic snippets
$("#new_date").click(function () {
  $("#new_date_child").removeClass('hidden');
})
