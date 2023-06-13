# Arabic Information Retrieval - README

## Overview
This project implements an Arabic Information Retrieval system that enables users to perform search queries and retrieve relevant information in the Arabic language. The core components include text preprocessing, text vectorization, and text indexing, which form the backbone of any Information Retrieval system.

The key functionality is implemented in Python, using several libraries that cater specifically to Arabic text, including PyArabic and SnowballStemmer. These are used for tasks like tokenization, stemming, and stop-word removal.

A Flask-based web application is also part of the project to expose this functionality as an API. The API has two primary endpoints; a search endpoint that accepts a query and returns the top relevant documents, and a document endpoint to retrieve the specific document's data.

The web application is hosted on [ensias-nlp.ma](http://www.ensias-nlp.ma/nlp/RechercheIinformation/). Please give it about 5 minutes to warm up when testing the application for the first time.

## How it Works

### Preprocessing
Arabic text is preprocessed before it's indexed or queried. Preprocessing involves several steps:
1. Cleaning the text to remove URLs, handles, special characters, tabs, and line breaks.
2. Removing Arabic stop words.
3. Normalizing Arabic letters to their base forms.
4. Stemming Arabic words to their root forms.

### Indexing
The ArabicTfidfVectorizer class is used to compute the TF-IDF values for the terms in the documents. This class computes a TF-IDF matrix where each row corresponds to a document and each column corresponds to a term. The indexer takes this TF-IDF matrix and creates an inverted index, where each term is mapped to a list of (document ID, TF-IDF value) tuples.

### Searching
To search the collection, a query is preprocessed and then transformed into a TF-IDF vector using the same method as when indexing the documents. This query vector is then compared with the document vectors in the index. The top N documents with the highest cosine similarity to the query vector are returned as the search results.

### Web Application
The web application exposes the indexer's functionality via two HTTP endpoints:
1. `/search`: Accepts a GET request with parameters "query" and "top_n". Returns the top N documents relevant to the given query.
2. `/document`: Accepts a GET request with parameter "doc_id". Returns the content of the document with the given ID.

## How to Use
To use the API, navigate to the hosted website on [ensias-nlp.ma](http://www.ensias-nlp.ma/nlp/RechercheIinformation/). Please note, as it is hosted on a free server, it may take up to 5 minutes to warm up and respond to the first request.

### Example:

To search for documents:
```
GET /search?query=ما هو العمر القانوني للتصويت في الولايات المتحدة؟&top_n=10
```

To get a specific document:
```
GET /document?doc_id=1
```

Note: Replace the `query` and `doc_id` parameters with your desired search query and document ID, respectively.

## Data
The data used for this project includes a variety of Arabic texts. Each document is associated with a unique identifier (doc_id), title, and raw_text, among other metadata.

## Future Improvements
Possible future improvements include integrating a more sophisticated ranking algorithm, expanding the data set, and incorporating user feedback to improve search result relevancy. 

## Contribution
Contributions to improve the functionality and efficiency of the system are welcome. Please raise an issue or submit a pull request.

## Disclaimer
Please note that the accuracy and relevancy of the results can
