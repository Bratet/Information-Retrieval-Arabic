$(document).ready(function () {
    // Get the document ID from the URL query string
    const urlParams = new URLSearchParams(window.location.search);
    const docId = urlParams.get('doc_id');

    // Fetch the document data using the document ID
    $.ajax({
        url: 'http://localhost:5000/document',
        data: { doc_id: docId },
        success: function (response) {
            // Set the document title and content
            $('#document-title').text(response.title);
            $('#document-content').html(response.raw_texts);
        },
    });
});

