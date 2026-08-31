from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config.settings import OPENAI_API_KEY, OPENAI_CHAT_MODEL, OPENAI_EMBEDDING_MODEL


#Shared Chat Model
llm = ChatOpenAI(
    model=OPENAI_CHAT_MODEL,
    api_key=OPENAI_API_KEY,
    temperature=0,
    streaming=True,
)


#Shared Embeddings Model
embeddings = OpenAIEmbeddings(
    model=OPENAI_EMBEDDING_MODEL,
    api_key =OPENAI_API_KEY
)