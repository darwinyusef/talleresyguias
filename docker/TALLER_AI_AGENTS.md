# Taller: Containerización de Agentes AI (LangChain)

## Objetivo
Aprender a desplegar agentes de IA usando LangChain, LangGraph y otros frameworks en contenedores Docker.

---

## Índice
1. [Agent Simple con LangChain](#agent-simple)
2. [Multi-Agent System](#multi-agent)
3. [Agent con Vector Database](#vector-database)
4. [LangGraph Agent](#langgraph)
5. [AutoGen Multi-Agent](#autogen)

---

## Agent Simple con LangChain

### Estructura del Proyecto

```
langchain-agent/
├── app/
│   ├── agent.py
│   ├── tools.py
│   └── main.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

### agent.py

```python
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import get_tools

def create_agent():
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use tools when necessary."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    tools = get_tools()
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor

def run_agent(query: str):
    agent = create_agent()
    result = agent.invoke({"input": query})
    return result["output"]
```

### tools.py

```python
from langchain.tools import tool
import requests

@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information about a topic."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No information found")
    return "Error searching Wikipedia"

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # Simulado - en producción usar API real
    return f"Weather in {city}: Sunny, 72°F"

def get_tools():
    return [search_wikipedia, calculate, get_weather]
```

### main.py (API con FastAPI)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import run_agent
import os

app = FastAPI(title="LangChain Agent API")

class Query(BaseModel):
    input: str

class Response(BaseModel):
    output: str

@app.post("/query", response_model=Response)
async def query_agent(query: Query):
    try:
        result = run_agent(query.input)
        return Response(output=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### requirements.txt

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
langchain==0.1.0
langchain-openai==0.0.2
langchain-core==0.1.0
requests==2.31.0
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped

  # Redis para cache/memory
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

### Uso

```bash
# Crear .env
echo "OPENAI_API_KEY=tu-api-key" > .env

# Build y run
docker compose up -d

# Test
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"input": "What is the weather in Paris and what is 25 * 4?"}'
```

---

## Multi-Agent System

### Arquitectura

```
Orchestrator Agent
    │
    ├─→ Research Agent (web search, wikipedia)
    ├─→ Data Agent (SQL, calculations)
    ├─→ Writer Agent (content generation)
    └─→ Reviewer Agent (quality check)
```

### orchestrator.py

```python
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import asyncio

class MultiAgentOrchestrator:
    def __init__(self):
        self.research_agent = self._create_research_agent()
        self.data_agent = self._create_data_agent()
        self.writer_agent = self._create_writer_agent()

    def _create_research_agent(self):
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a research specialist. Find and summarize information."),
            ("human", "{input}")
        ])
        # Add research tools
        return AgentExecutor(agent=..., tools=research_tools)

    def _create_data_agent(self):
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        # Data analysis tools
        return AgentExecutor(agent=..., tools=data_tools)

    def _create_writer_agent(self):
        llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        # Writing tools
        return AgentExecutor(agent=..., tools=writing_tools)

    async def execute_workflow(self, task: str):
        # 1. Research phase
        research_results = await self.research_agent.ainvoke({
            "input": f"Research: {task}"
        })

        # 2. Data analysis
        data_results = await self.data_agent.ainvoke({
            "input": f"Analyze: {research_results['output']}"
        })

        # 3. Content generation
        final_output = await self.writer_agent.ainvoke({
            "input": f"Write article based on: {data_results['output']}"
        })

        return final_output['output']
```

### docker-compose.yml (Multi-Agent)

```yaml
version: '3.8'

services:
  orchestrator:
    build: ./orchestrator
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - RESEARCH_AGENT_URL=http://research-agent:8001
      - DATA_AGENT_URL=http://data-agent:8002
      - WRITER_AGENT_URL=http://writer-agent:8003

  research-agent:
    build: ./agents/research
    ports:
      - "8001:8001"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}

  data-agent:
    build: ./agents/data
    ports:
      - "8002:8002"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://user:pass@postgres:5432/agentdb

  writer-agent:
    build: ./agents/writer
    ports:
      - "8003:8003"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: agentdb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
```

---

## Agent con Vector Database

### Dockerfile (con ChromaDB)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### requirements.txt

```
fastapi==0.104.1
uvicorn==0.24.0
langchain==0.1.0
langchain-openai==0.0.2
chromadb==0.4.22
sentence-transformers==2.2.2
```

### rag_agent.py

```python
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAGAgent:
    def __init__(self, persist_directory="./chroma_db"):
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.qa_chain = None

    def load_documents(self, directory_path):
        """Load and index documents"""
        loader = DirectoryLoader(
            directory_path,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        documents = loader.load()

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)

        # Create vectorstore
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )

        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            ),
            return_source_documents=True
        )

    def query(self, question: str):
        """Query the RAG system"""
        if not self.qa_chain:
            raise ValueError("Documents not loaded. Call load_documents first.")

        result = self.qa_chain({"query": question})
        return {
            "answer": result["result"],
            "sources": [doc.metadata for doc in result["source_documents"]]
        }
```

### docker-compose.yml (RAG System)

```yaml
version: '3.8'

services:
  rag-agent:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./documents:/app/documents
      - chroma_data:/app/chroma_db
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}

  # ChromaDB standalone (alternativa)
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/chroma/chroma

volumes:
  chroma_data:
```

---

## LangGraph Agent (State Machine)

### graph_agent.py

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI

class AgentState(TypedDict):
    messages: list
    next_action: str
    final_answer: str

def research_node(state: AgentState):
    """Research information"""
    # Perform research
    state["messages"].append("Research completed")
    state["next_action"] = "analyze"
    return state

def analyze_node(state: AgentState):
    """Analyze data"""
    # Perform analysis
    state["messages"].append("Analysis completed")
    state["next_action"] = "write"
    return state

def write_node(state: AgentState):
    """Write final answer"""
    # Generate answer
    state["final_answer"] = "Final answer generated"
    state["next_action"] = "end"
    return state

def create_agent_graph():
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("write", write_node)

    # Add edges
    workflow.add_edge("research", "analyze")
    workflow.add_edge("analyze", "write")
    workflow.add_edge("write", END)

    # Set entry point
    workflow.set_entry_point("research")

    return workflow.compile()

# Usage
app = create_agent_graph()
result = app.invoke({
    "messages": [],
    "next_action": "",
    "final_answer": ""
})
```

---

## AutoGen Multi-Agent

### autogen_system.py

```python
import autogen

config_list = [{
    "model": "gpt-4",
    "api_key": os.environ["OPENAI_API_KEY"]
}]

# Create agents
user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5
)

researcher = autogen.AssistantAgent(
    name="Researcher",
    llm_config={"config_list": config_list},
    system_message="You are a researcher. Find and summarize information."
)

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config={"config_list": config_list},
    system_message="You are a coder. Write clean, efficient code."
)

reviewer = autogen.AssistantAgent(
    name="Reviewer",
    llm_config={"config_list": config_list},
    system_message="You are a code reviewer. Check quality and suggest improvements."
)

# Create group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, researcher, coder, reviewer],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}
)

# Execute task
user_proxy.initiate_chat(
    manager,
    message="Create a Python function to calculate fibonacci numbers."
)
```

### docker-compose.yml (AutoGen)

```yaml
version: '3.8'

services:
  autogen:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./output:/app/output
```

---

## Memoria Persistente con Redis

### memory.py

```python
from langchain.memory import RedisChatMessageHistory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
import redis

class AgentWithMemory:
    def __init__(self, session_id: str):
        self.redis_client = redis.Redis(host='redis', port=6379, db=0)
        self.memory = RedisChatMessageHistory(
            session_id=session_id,
            url="redis://redis:6379/0"
        )

        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.chain = ConversationChain(
            llm=self.llm,
            memory=self.memory
        )

    def chat(self, message: str):
        return self.chain.predict(input=message)
```

---

## Mejores Prácticas

1. **API Keys seguras** - Usar variables de entorno
2. **Rate limiting** - Limitar requests al LLM
3. **Caching** - Cachear respuestas comunes
4. **Logging** - Registrar todas las interacciones
5. **Error handling** - Manejar errores de API
6. **Timeouts** - Configurar timeouts razonables
7. **Monitoring** - Monitorear uso y costos
8. **Testing** - Tests con mocks de LLM

---

## Costos y Optimización

```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = agent.run("Query")
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")
```

---

¡Los agentes de IA en contenedores permiten escalabilidad y deployment fácil!
