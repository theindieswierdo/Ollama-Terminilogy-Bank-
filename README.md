# Ollama-Terminilogy-Bank-
A small, privacy-first word definition web application powered by a locally running LLM through Ollama.

Enter a word to receive its definition and an example sentence, then save words locally so they can be revisited later.

**Privacy:** The application is designed to run locally. The LLM request is sent to your local Ollama instance rather than a cloud AI API.

**Features**

- 🔍 Look up definitions for words
- ✍️ Generate a short example sentence for each word
- 💾 Save words, meanings and examples locally
- 📖 View a dedicated saved-words page
- 🗑️ Delete individual saved words
- 🧹 Clear the complete saved-word list
- ❤️ Health check for the local Ollama service
- 🔒 No API key or cloud LLM service required
- 📚 FastAPI's automatically generated API documentation

**Technologies Used**

<div class="joplin-table-wrapper"><table><tbody><tr><th><p><strong>Technology</strong></p></th><th><p><strong>Purpose</strong></p></th></tr><tr><td><p>Python 3.10+</p></td><td><p>Application/backend language</p></td></tr><tr><td><p>FastAPI</p></td><td><p>REST API and web server framework</p></td></tr><tr><td><p>Uvicorn</p></td><td><p>ASGI server used to run FastAPI</p></td></tr><tr><td><p>Pydantic</p></td><td><p>Request/response data validation</p></td></tr><tr><td><p>Requests</p></td><td><p>HTTP communication with Ollama</p></td></tr><tr><td><p>Ollama</p></td><td><p>Local LLM runtime</p></td></tr><tr><td><pre><code>llama3.2:3b</code></pre></td><td><p>Local language model used for definitions</p></td></tr><tr><td><p>HTML</p></td><td><p>Frontend structure</p></td></tr><tr><td><p>JavaScript</p></td><td><p>Frontend interaction and API requests</p></td></tr><tr><td><p>JSON</p></td><td><p>Local persistence for saved words</p></td></tr></tbody></table></div>

The original project uses plain HTML and JavaScript rather than a CSS framework. The saved-word data is stored in words_history.json.