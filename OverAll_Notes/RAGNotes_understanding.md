# RAG (Retrieval-Augmented Generation) — Detailed Understanding Notes

> A comprehensive textual deep-dive into RAG pipelines, architecture, and best practices — without diagrams.

---

## 1. What is RAG?

RAG stands for **Retrieval-Augmented Generation**. It is a technique that enhances Large Language Models (LLMs) by providing them with relevant external knowledge retrieved from a knowledge base at query time, rather than relying solely on the model's internal (static) training data.

The core idea is simple: instead of asking an LLM to answer from memory alone (which may be outdated or incomplete), we first search a database of relevant documents, retrieve the most useful pieces, and feed them into the LLM as context. The LLM then generates an answer grounded in that retrieved information.

### Without RAG vs With RAG

**Without RAG:** The LLM answers purely from its training data. It has no access to your private documents, JIRA tickets, internal wikis, or any information created after its training cutoff date. It may hallucinate facts when it doesn't know the answer.

**With RAG:** The LLM receives the user's question PLUS relevant context retrieved from your own knowledge base. It can cite sources, answer accurately about private data, and stay current without retraining.

---

## 2. Why RAG? — The Problem It Solves

LLMs are trained on a static snapshot of public internet data. This creates several problems:

- They do not know your private data — JIRA tickets, internal docs, codebases, HR policies, etc.
- They can be outdated because their training has a cutoff date.
- They hallucinate when guessing unknown facts, producing confident but wrong answers.
- They cannot reliably cite sources, making verification difficult.

RAG solves all of these by retrieving relevant documents at query time and injecting them into the LLM's prompt as context. This grounds the LLM's answer in verifiable, up-to-date information.

---

## 3. RAG Pipeline Overview

The RAG pipeline consists of two major phases:

### Phase 1: Ingestion (Data Feeding)
This is the offline/background phase where you prepare your knowledge base. Raw documents are loaded, split into smaller chunks, converted into numerical vectors using an embedding model, and stored in a vector database.

### Phase 2: Retrieval + Generation (RAG)
This is the runtime phase that happens when a user asks a question. The user's query is converted into a vector, the vector database is searched for the most similar chunks, those chunks are retrieved, and they are fed into the LLM along with the original question to generate a grounded answer.

---

## 4. Phase 1: Ingestion — Detailed Breakdown

Ingestion is the process of preparing and storing your knowledge base so it can be searched later. It involves four steps:

### 4.1 Document Loading

Documents can come from many sources. The supported document types include:

- **JIRA Tickets** — exported via API or CSV
- **GitHub Repositories** — cloned and parsed for code and documentation
- **PDF Files** — text extracted via OCR or PDF parsers
- **Markdown Files (.md)** — natively supported
- **Figma Designs** — via Figma API or plugins
- **HTML / Web Pages** — via web scraping
- **Confluence Pages** — via Confluence API
- **Notion Docs** — via Notion API
- **Word and Excel Documents** — via document parsers

### 4.2 Chunking

Documents are typically too large to feed directly into an LLM because of context window limits. They must be split into smaller, manageable pieces called chunks.

**Common chunking strategies include:**

- **Fixed-size chunking:** Split by a fixed number of tokens (e.g., 512 tokens per chunk). Simple but may cut sentences in half.
- **Recursive chunking:** Split by paragraphs first, then sentences, then words. More intelligent than fixed-size.
- **Semantic chunking:** Split by meaning or topic boundaries. The most intelligent but also the most complex.
- **Document-specific chunking:** Split by natural boundaries in the document format, such as headers in Markdown or sections in HTML.

**Chunk size trade-offs:**

- **Small chunks (128-256 tokens):** High precision retrieval because each chunk is very focused. However, they may lack surrounding context needed to understand the information fully.
- **Medium chunks (512-1024 tokens):** A good balance between precision and context. This is the most commonly used range.
- **Large chunks (2048+ tokens):** Full context is retained, but the chunk may contain noise (irrelevant information) and costs more tokens to process.

**Overlap strategy:** Chunks often overlap by a small amount (e.g., 10-20%) to avoid cutting sentences or ideas in half. For example, chunk 1 might end with "cannot authenticate" and chunk 2 might start with "cannot authenticate with valid credentials" so the meaning is preserved regardless of which chunk is retrieved.

### 4.3 Embedding

Each chunk of text is converted into a numerical vector (a list of floating-point numbers) using an embedding model. This vector represents the semantic meaning of the text.

For example, the sentence "Bug in login page" might be converted into a 768-dimensional vector like `[0.234, -0.567, 0.891, ...]`.

**Popular embedding models include:**

- **text-embedding-3-small** (OpenAI) — 512 to 1536 dimensions, general purpose, cost-effective
- **text-embedding-3-large** (OpenAI) — 256 to 3072 dimensions, high accuracy
- **BGE (Base/Large)** (BAAI) — 768 to 1024 dimensions, open-source, good multilingual support
- **all-MiniLM-L6-v2** (Sentence-Transformers) — 384 dimensions, lightweight, runs locally
- **mxbai-embed-large** (Mixedbread) — 1024 dimensions, open-source, high quality
- **nomic-embed-text** (Nomic) — 768 dimensions, open-source, supports long context

**Local vs Cloud Embeddings:**

- **Local embeddings** run on your own machine. They are free and private but slower and use smaller models.
- **Cloud embeddings** are API-based. They are paid per token but fast and use large, powerful models.

### 4.4 Vector Database Storage

The embeddings are stored in a vector database along with the original text and metadata (such as source document name, page number, date, etc.).

Each record in a vector database contains:
- A unique ID
- The vector (list of numbers)
- Metadata (source, page, original text, date, etc.)

---

## 5. Phase 2: Retrieval + Generation — Detailed Breakdown

This is the runtime phase that executes when a user asks a question.

### 5.1 The Three Components of RAG

At query time, the LLM has three inputs:

1. **User Question** — what the user wants to know
2. **Context from Vector DB** — the Top-K most relevant document chunks retrieved from the vector database
3. **System Instructions** — guidelines on how to use the context (e.g., "Answer only from the provided context")

The LLM augments (combines) all of these and produces the output — this is called **Generation**.

### 5.2 Step-by-Step Query Flow

**Step 1 — Embed the User Query:** The user's question is converted into a vector using the same embedding model that was used during ingestion.

**Step 2 — Search the Vector Database:** The query vector is compared against all vectors in the database using a similarity metric. The database returns the Top-K most similar chunks (e.g., the top 5 most relevant pieces of text).

**Step 3 — Retrieve Top-K Results:** The most relevant chunks are retrieved along with their metadata.

**Step 4 — Construct the Augmented Prompt:** A prompt is built that includes:
- System instructions (e.g., "Answer based ONLY on the provided context")
- The retrieved context chunks
- The user's original question

**Step 5 — Send to LLM:** The augmented prompt is sent to the LLM.

**Step 6 — Generate Answer:** The LLM generates an answer grounded in the provided context. If the context does not contain the answer, the LLM should say "I don't have that information" rather than hallucinating.

### 5.3 Example Walkthrough

**User Query:** "How many employees are in the company?"

The LLM has no context about the company's employee count from its training data. So the RAG system:

1. Embeds the query into a vector
2. Searches the vector database (which contains HR documents, company wikis, etc.)
3. Retrieves chunks like: "The company has 1,247 employees as of Q4 2025" and "Engineering department has 450 employees"
4. Builds a prompt with these chunks as context
5. Sends to the LLM
6. LLM responds: "Based on our HR documents, the company has 1,247 employees as of Q4 2025."

---

## 6. Vector Databases — Explained in Detail

### 6.1 What is a Vector Database?

A vector database is a specialized database designed to store and search vector embeddings efficiently. Unlike traditional databases that search by exact matches or SQL conditions, vector databases search by semantic similarity.

**Traditional Database:** You query "WHERE name = 'login'" and get only exact matches for the word "login".

**Vector Database:** You query with the vector for "authentication issue" and get semantically similar results like "login problem", "sign-in bug", "SSO error" — even though none of those contain the exact words "authentication issue".

### 6.2 How Vector Search Works

Vector search works by measuring the distance (or similarity) between the query vector and every vector in the database. The vectors that are closest in the vector space are considered the most semantically similar.

### 6.3 Similarity Metrics

- **Cosine Similarity:** Measures the angle between two vectors. Range is -1 to 1 (higher = more similar). This is the most common metric for text.
- **Dot Product:** Measures both the angle and magnitude. Used when vectors are normalized.
- **Euclidean Distance:** Measures the straight-line distance between two vectors. Smaller distance = more similar.
- **Manhattan Distance:** Sum of absolute differences across all dimensions. Used for high-dimensional sparse data.

### 6.4 Popular Vector Databases

- **Qdrant:** A dedicated vector database designed for production use. Supports self-hosting and cloud. High performance.
- **Chroma:** An embedded vector database that runs in-process. Best for prototyping and small projects. Open-source.
- **pgvector:** A PostgreSQL extension that adds vector support. Best when you are already using PostgreSQL.
- **Pinecone:** A fully managed cloud vector database. No operations overhead but not self-hostable.
- **Weaviate:** A dedicated vector database with hybrid search and GraphQL support. Supports self-hosting and cloud.
- **Milvus:** A distributed vector database designed for large-scale deployments (billion+ vectors).
- **FAISS:** A library (not a full database) from Facebook for fast similarity search. Runs locally.

### 6.5 How to Choose a Vector Database

- **Small scale / prototyping:** Use Chroma or FAISS.
- **Large scale / production:** Use Milvus or Qdrant.
- **Self-hosted:** Use Qdrant or Weaviate.
- **Fully managed / no ops:** Use Pinecone.
- **Already using PostgreSQL:** Use pgvector.

---

## 7. Retrieval Techniques

### 7.1 Simple Vector Search (Naive RAG)

The simplest approach: embed the query, search the vector database, retrieve Top-K results, feed to LLM. This works well for many use cases but can miss relevant results that use different vocabulary.

### 7.2 Hybrid Search (Vector + Keyword)

Combines vector search (semantic) with keyword search (BM25 or TF-IDF, which matches exact words). The results from both searches are merged and reranked. This is more robust because it catches both semantic similarities and exact keyword matches.

### 7.3 Multi-Query Retrieval

The original query is expanded into multiple variations using an LLM. For example, "login bugs" might be expanded to "authentication errors", "sign-in issues", "SSO problems". Each variation is searched separately, and the results are merged and deduplicated. This increases coverage.

### 7.4 Reranking

After initial retrieval (which is fast but approximate), a reranker model scores the results more accurately. The reranker is slower but more precise. Typical flow: initial search returns 50 results, the reranker scores them, and the top 5 are sent to the LLM.

---

## 8. Image and Video Support

### Images

Images are supported but require a paid subscription to a multimodal model (such as GPT-4V or Claude 3.5). The process works by using a multimodal LLM to extract text or descriptions from the image, then embedding that text description. The image itself is not stored in the vector database — only the textual description.

### Videos

Videos are also supported but require a paid subscription. The typical approach is to transcribe the audio track, chunk the transcript, and embed the text. Alternatively, key frames can be extracted and processed as images using a multimodal model.

**Important:** Free and open-source RAG setups typically handle text only. Image and video support requires a paid subscription to a multimodal model provider.

---

## 9. RAG vs Fine-Tuning

### RAG

**Advantages:**
- No training required — just load documents into the vector database
- Always up-to-date — just re-index documents when they change
- Provides source citations — answers are verifiable
- Low hallucination risk — answers are grounded in retrieved context

**Disadvantages:**
- Higher latency — retrieval adds time to each query
- Higher cost per query — more tokens are used (context + question)
- Requires a vector database infrastructure

### Fine-Tuning

**Advantages:**
- Low latency — no retrieval step needed
- No external dependency — the model knows everything internally
- Lower cost per query — fewer tokens used

**Disadvantages:**
- Expensive to train — requires GPU time and expertise
- Static knowledge — retraining is needed to update information
- Can still hallucinate — no source grounding
- No source citations — cannot show where information came from

### When to Use Which

- **Use RAG** when you need factual accuracy, up-to-date information, private data access, and source citations.
- **Use Fine-Tuning** when you need to change the model's behavior, tone, style, or response format consistently.

They can also be combined — fine-tune for behavior and use RAG for knowledge.

---

## 10. Common Challenges and Solutions

### Poor Chunk Quality
**Problem:** Irrelevant or poorly structured chunks are retrieved.
**Solution:** Improve the chunking strategy. Use semantic chunking instead of fixed-size. Add overlap between chunks.

### Low Relevance of Retrieved Results
**Problem:** The Top-K results are not useful for answering the question.
**Solution:** Use hybrid search (vector + keyword) instead of pure vector search. Add a reranker step.

### Hallucination Despite RAG
**Problem:** The LLM ignores the provided context and makes up an answer.
**Solution:** Strengthen the system prompt with explicit instructions (e.g., "Only answer from the provided context. If the context doesn't contain the answer, say you don't know."). Lower the LLM's temperature setting.

### High Latency
**Problem:** Retrieval + generation takes too long.
**Solution:** Cache frequent queries and their answers. Use a smaller/faster embedding model. Use a smaller LLM for simple queries.

### High Cost
**Problem:** Too many tokens consumed per query.
**Solution:** Optimize chunk size (smaller chunks = fewer tokens). Cache embeddings to avoid recomputing. Use a cheaper LLM for retrieval.

### Stale Data
**Problem:** The vector database contains outdated information.
**Solution:** Set up a regular re-indexing schedule (daily or weekly). Use change detection to re-index only changed documents.

### Missing Context
**Problem:** The retrieved chunks don't contain enough context to answer the question.
**Solution:** Increase chunk size. Add overlap between chunks. Retrieve more chunks (increase Top-K).

---

## 11. Use Cases in QA and Testing

RAG is particularly powerful for QA Engineers and SDETs:

- **Bug Triage:** Retrieve similar past bugs to automatically classify new bugs by severity, priority, and component.
- **Test Case Generation:** Retrieve similar test cases from history to generate new test cases for a feature.
- **Regression Analysis:** Find all related bugs and test cases for a feature before a release.
- **Knowledge Base Q&A:** Ask questions like "How do we test login functionality?" and get SOPs from documentation.
- **Release Notes:** Summarize all fixed bugs from JIRA for a release, grouped by component.
- **Root Cause Analysis:** Find similar past incidents and their resolutions to speed up debugging.

---

## 12. Glossary of Key Terms

| Term | Definition |
|---|---|
| **RAG** | Retrieval-Augmented Generation — combining document retrieval with LLM generation |
| **Embedding** | Converting text into a numerical vector representation |
| **Vector** | A list of numbers representing the semantic meaning of text |
| **Vector Database** | A database optimized for storing and searching vectors by similarity |
| **Chunk** | A small piece of a larger document |
| **Chunking** | The process of splitting documents into smaller pieces |
| **Top-K** | The number of most relevant results to retrieve from the vector database |
| **Similarity Search** | Finding vectors closest to a query vector in the vector space |
| **Cosine Similarity** | A metric measuring the angle between two vectors (range: -1 to 1) |
| **Reranker** | A model that re-scores retrieved results for better relevance |
| **Hybrid Search** | Combining vector search with keyword search (BM25/TF-IDF) |
| **Multimodal** | Models that can process text, images, and audio together |
| **Hallucination** | When an LLM generates false or unsupported information |
| **Augmentation** | Adding retrieved context to the LLM prompt before generation |
| **Generation** | The LLM producing the final answer based on context and question |
| **Ingestion** | The process of loading, chunking, embedding, and storing documents |
| **Metadata** | Additional information stored alongside vectors (source, date, page, etc.) |
| **Context Window** | The maximum number of tokens an LLM can process in a single request |

---

## 13. Quick Summary

RAG is a two-phase process:

**Phase 1 — Ingestion:** Take your documents (JIRA, PDF, GitHub, Markdown, etc.), split them into chunks, convert each chunk into a vector using an embedding model, and store everything in a vector database.

**Phase 2 — Retrieval + Generation:** When a user asks a question, convert the question into a vector, search the vector database for the most similar chunks, retrieve the Top-K results, build a prompt with those chunks as context, and send it to an LLM to generate a grounded answer.

The result is an LLM that can answer questions about your private data, cite its sources, stay up-to-date without retraining, and hallucinate far less than a standalone LLM.

---

> **Created for:** AITesters BluePrint 4X  
> **Topic:** RAG (Retrieval-Augmented Generation) — Understanding Notes  
> **Last Updated:** 2026-09-19