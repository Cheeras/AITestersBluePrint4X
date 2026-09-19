RAG - has 2 parts


RAG Pipeline 

1 . Ingestion -feeding the data

2. RAG -


Phase 1:

Ingestion:

Document - can be JIRA ID,Git hub repo, pdf ,figma design,md file  are part of the documentaion

is the image and video supported 

answer is yes we need paid subscription 


Documents/Ingestion --> encodeing ( we will use embading model) they are divided into small chunks and put in vector database

now the vector DB is 

now the real thing how to retrieve information

Phase 2: - RAG

User Query - How many emp are there in your company -

where this query will go LLM or Vector DB?

LLM has no context about your company information and it will take the help of the Vector DB (Quadrant,Chroma,pgvector)

Vector DB - smart DB

what Vector DB will do , it will find the all documents that are feeded trying to find the relavent information to LLM - this is called retrival


Now LLM has 3 

User Question 

Context came from Vector DB(top k results)

LLM will agument all these content and produce the output that is called Genaration 


This is what is called RAG in simplar way
