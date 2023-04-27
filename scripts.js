$(document).ready(function () {
    $("#search-form").submit(function (event) {
        event.preventDefault();
        var query = $("#search-input").val();
        $.ajax({
            url: "http://localhost:5000/search",
            data: { query: query },
            success: function (response) {
                var results = response.results;
                console.log(results);
                var resultsContainer = $("#results-container");
                resultsContainer.empty();
                for (var i = 0; i < results.length; i++) {
                    var result = results[i];
                    var documentElement = $('<div class="document"></div>');
                    var contentElement = $('<div class="content"></div>');
                    var rankingElement = $('<span class="ranking"></span>').text((i + 1) + ".");
                    var documentLinkElement = $('<a class="document-link"></a>')
                        .attr("href", "document.html?doc_id=" + result.doc_id)
                        .attr("data-doc-id", result.doc_id)
                        .text(result.titles);

                    var descriptionElement = $('<p class="description"></p>').text(result.description);
                    contentElement.append(documentLinkElement)
                    contentElement.append(descriptionElement)
                    documentElement.append(rankingElement);
                    documentElement.append($('<br>'));
                    documentElement.append(contentElement);
                    documentElement.append($('<br>'));
                    documentElement.append($('<br>'));
                    resultsContainer.append(documentElement);

                    // Add animation delay
                    documentElement.css("transition-delay", (i * 0.1) + "s");

                    // Make the document visible after a short delay
                    setTimeout(function (elem) {
                        elem.addClass("visible");
                    }, i * 100, documentElement);
                }
            },
        });
    });
});
