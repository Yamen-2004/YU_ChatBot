(make chunks file) ==> Read a file containing data.

Edit the text (remove excess spaces and adjust basic punctuation marks).

Divide the content of each record into small pieces, each about 900 characters long.

Give each piece a unique ID number + the number of the original record + a link, if available.

Save the result as JSONL (each piece on a separate line) so that it can then be stored in the database.

========================================================================================================
========================================================================================================
========================================================================================================

(Make emedding file) ==>> Loads a file that contains a list of text chunks (small parts of scraped data saved earlier).

Cleans and normalizes the text by removing extra spaces and trimming the content so it's tidy.

Uses a pre-trained embedding model to convert each chunk into a numerical vector (embedding).

Encodes only the text content into vectors efficiently, one vector per chunk.

Adds the generated vector back into each record under a new field called "embedding".

Writes the final output to a new JSON file where every chunk now has:

the cleaned text

its vector embedding

the original URL and title if they existed

Prints a small preview and the total count so you can verify the process finished.

========================================================================================================
========================================================================================================
========================================================================================================


(server.js file)  ==> NodeJS  script uploads data containing Embedding to MongoDB



Reads a JSON file full of Chunks + Vectors that I created with Python.

Checks that the file exists and is not corrupted (surprisingly, it trusts the file more than it usually trusts humans).

Connects to the database you specify.

Enters each chunk as a document into the collection.

Prints the number of records entered to make sure they arrived alive.

========================================================================================================
========================================================================================================
========================================================================================================


(search.js file )==>    This Node.js script connects to a MongoDB database, pulls a collection of documents that contain vector embeddings, 
   and runs a vector similarity search using a specific query vector. It then filters and prints out the closest matching text chunks stored in the database. Essentially, 
   it's taking your question (converted into a numeric vector), comparing it to stored vectors, retrieving the most similar document fragments, and outputting them so they can later be sent to an LLM or used in your app.


