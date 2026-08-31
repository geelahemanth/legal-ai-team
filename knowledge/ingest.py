from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from knowledge.vector_store import get_vector_store
from retrieval.bm25_retriever import create_bm25_retriever
from retrieval.bm25_store import save_bm25_retriever

def ingest_pdf(pdf_path: str):
   """ Load a PDF, Split it into chunks, and store it in Chroma vector store. """
   
   #load pdf 
   loader = PyPDFLoader(pdf_path)
   documents = loader.load()
   print("======================================")
   #print(documents)  # Print the first 500 characters of the first page for verification
   
   # Split into chunks
   splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
   print(f"Splitting {len(documents)} documents into chunks...")
   chunks = splitter.split_documents(documents)

   bm25 = create_bm25_retriever(chunks)  # Create a BM25 retriever from the chunks
   save_bm25_retriever(bm25)
   # print("IDF>>>>>>>>>>>>>>", bm25.vectorizer.idf)
   print("Number of chunks indexed:", len(bm25.docs))

   print("\n========== BM25 VOCABULARY ==========")
   print("Total unique terms:", len(bm25.vectorizer.idf))
   print("First 30 terms:")
   print(list(bm25.vectorizer.idf.keys())[:30])

   results = bm25.invoke("What is the termination notice period?")

   # print("\n========== BM25 RESULTS ==========")
   
   # for i, doc in enumerate(results, 1):
   #  print(f"\nResult {i}")
   #  print("Page:", doc.metadata.get("page_label"))
   #  print("Content:")
   #  print(doc.page_content[:500])
   
   #get vector store
   vector_store = get_vector_store()
   vector_store.reset_collection()  # Clear existing collection before adding new documents
   
   #store chunks in vector store
   vector_store.add_documents(chunks)
   print(f"Successfully ingested {len(chunks)} chunks from {pdf_path} into the vector store.")