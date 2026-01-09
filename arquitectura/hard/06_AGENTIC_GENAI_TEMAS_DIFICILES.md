# Conocimientos Técnicos Difíciles: Agentic & GenAI Development

## Objetivo
Temas complejos del día a día de desarrollo con agentes y GenAI que un arquitecto debe dominar para apoyar efectivamente a desarrolladores de IA generativa y sistemas agénticos.

---

## CATEGORÍA 1: LLM Integration y Prompt Engineering

### 1.1 Advanced Prompt Engineering
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from anthropic import Anthropic
import openai

# 1. Few-Shot Learning con ejemplos estratégicos
def create_few_shot_prompt(task_description, examples, new_input):
    prompt = f"""{task_description}

Here are some examples:

"""
    for i, example in enumerate(examples, 1):
        prompt += f"""Example {i}:
Input: {example['input']}
Output: {example['output']}

"""

    prompt += f"""Now, process this input:
Input: {new_input}
Output:"""

    return prompt

# Uso
examples = [
    {
        'input': 'The product is amazing and works perfectly!',
        'output': 'Sentiment: Positive\nConfidence: 0.95\nKey phrases: amazing, works perfectly'
    },
    {
        'input': 'Terrible quality, broke after 2 days',
        'output': 'Sentiment: Negative\nConfidence: 0.90\nKey phrases: terrible quality, broke'
    }
]

prompt = create_few_shot_prompt(
    "Analyze the sentiment of product reviews:",
    examples,
    "It's okay, nothing special but does the job"
)

# 2. Chain of Thought (CoT) Prompting
def chain_of_thought_prompt(problem):
    return f"""Solve this problem step by step. Show your reasoning at each step.

Problem: {problem}

Let's approach this systematically:

Step 1: [Identify what we know]
Step 2: [Break down the problem]
Step 3: [Apply relevant concepts]
Step 4: [Calculate/Reason through]
Step 5: [Verify and conclude]

Solution:"""

# 3. Self-Consistency (múltiples razonamientos)
async def self_consistency_generation(client, prompt, n_samples=5):
    """
    Generate multiple reasoning paths and pick most consistent answer
    """
    responses = []

    for _ in range(n_samples):
        response = await client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.7,  # Higher for diversity
            messages=[{"role": "user", "content": prompt}]
        )
        responses.append(response.content[0].text)

    # Extract final answers
    answers = [extract_final_answer(r) for r in responses]

    # Vote for most common answer
    from collections import Counter
    most_common = Counter(answers).most_common(1)[0][0]

    return {
        'final_answer': most_common,
        'all_responses': responses,
        'confidence': Counter(answers)[most_common] / len(answers)
    }

# 4. Tree of Thoughts (exploración de múltiples caminos)
class TreeOfThoughts:
    def __init__(self, client, max_depth=3, branch_factor=3):
        self.client = client
        self.max_depth = max_depth
        self.branch_factor = branch_factor

    async def generate_thoughts(self, problem, context=""):
        """Generate possible next thoughts"""
        prompt = f"""Given this problem and current reasoning:

Problem: {problem}
Current reasoning: {context}

Generate {self.branch_factor} different possible next steps in reasoning.
Each should explore a different approach.

Format:
1. [thought 1]
2. [thought 2]
3. [thought 3]"""

        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse thoughts
        thoughts = parse_numbered_list(response.content[0].text)
        return thoughts

    async def evaluate_thought(self, problem, thought_chain):
        """Evaluate how promising a thought chain is"""
        prompt = f"""Evaluate this reasoning chain for solving the problem.
Rate from 0-10 how likely this leads to correct solution.

Problem: {problem}
Reasoning so far: {' -> '.join(thought_chain)}

Rating (0-10):"""

        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}]
        )

        rating = extract_rating(response.content[0].text)
        return rating

    async def solve(self, problem):
        """Explore tree of thoughts to find best solution"""
        best_chain = []
        best_rating = 0

        async def explore(chain, depth):
            nonlocal best_chain, best_rating

            if depth >= self.max_depth:
                rating = await self.evaluate_thought(problem, chain)
                if rating > best_rating:
                    best_rating = rating
                    best_chain = chain.copy()
                return

            thoughts = await self.generate_thoughts(problem, ' -> '.join(chain))

            for thought in thoughts:
                new_chain = chain + [thought]
                rating = await self.evaluate_thought(problem, new_chain)

                if rating > 5:  # Pruning: solo explorar caminos prometedores
                    await explore(new_chain, depth + 1)

        await explore([], 0)

        return {
            'best_chain': best_chain,
            'rating': best_rating
        }

# 5. Prompt Templates con variables
class PromptTemplate:
    def __init__(self, template, input_variables):
        self.template = template
        self.input_variables = input_variables

    def format(self, **kwargs):
        # Validar variables
        missing = set(self.input_variables) - set(kwargs.keys())
        if missing:
            raise ValueError(f"Missing variables: {missing}")

        return self.template.format(**kwargs)

# Ejemplo: template de análisis de código
code_review_template = PromptTemplate(
    template="""You are an expert code reviewer. Analyze this code:

Language: {language}
Context: {context}

Code:
```{language}
{code}
```

Provide:
1. Security issues (if any)
2. Performance concerns
3. Best practice violations
4. Suggestions for improvement

Focus on: {focus_areas}

Review:""",
    input_variables=['language', 'context', 'code', 'focus_areas']
)

prompt = code_review_template.format(
    language='python',
    context='FastAPI endpoint for user authentication',
    code='def login(username, password):\n    return db.query(f"SELECT * FROM users WHERE name={username}")',
    focus_areas='security, SQL injection'
)

# 6. Constrained Generation (forzar formato JSON)
def create_json_prompt(schema_description, example_output):
    return f"""Extract information and return ONLY valid JSON matching this schema:

{schema_description}

Example output format:
{example_output}

Rules:
- Return ONLY the JSON object
- No additional text before or after
- Ensure all required fields are present
- Use null for missing optional fields

Input: {{input}}

JSON Output:"""

# Uso con Claude
async def extract_structured_data(client, text, schema):
    prompt = f"""Extract structured data from this text and return as JSON:

Text: {text}

Required JSON schema:
{json.dumps(schema, indent=2)}

Return ONLY the JSON, nothing else:"""

    response = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        temperature=0,  # Deterministic
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse and validate JSON
    import json
    try:
        data = json.loads(response.content[0].text)
        return data
    except json.JSONDecodeError:
        # Retry with clearer instruction
        pass
```

---

### 1.2 Function Calling y Tool Use
**Dificultad:** ⭐⭐⭐⭐⭐

```python
import json
from typing import List, Dict, Any

# 1. Define tools/functions
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or coordinates"
                },
                "units": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "search_database",
        "description": "Search internal database for information",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "filters": {
                    "type": "object",
                    "description": "Optional filters"
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculations",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    }
]

# 2. Implement tool functions
def get_weather(location: str, units: str = "celsius") -> Dict[str, Any]:
    # Llamada a API real
    import requests
    response = requests.get(
        f"https://api.weather.com/v1/current",
        params={"location": location, "units": units}
    )
    return response.json()

def search_database(query: str, filters: Dict = None, limit: int = 10) -> List[Dict]:
    # Query a base de datos
    results = db.search(query, filters=filters, limit=limit)
    return results

def calculate(expression: str) -> float:
    # Safe eval
    import ast
    import operator

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow
    }

    def eval_expr(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](
                eval_expr(node.left),
                eval_expr(node.right)
            )
        else:
            raise ValueError(f"Unsupported operation: {node}")

    tree = ast.parse(expression, mode='eval')
    return eval_expr(tree.body)

# 3. Agent con tool use
class ToolUseAgent:
    def __init__(self, client, tools):
        self.client = client
        self.tools = tools
        self.tool_functions = {
            'get_weather': get_weather,
            'search_database': search_database,
            'calculate': calculate
        }

    async def run(self, user_message: str, max_iterations: int = 5):
        messages = [{"role": "user", "content": user_message}]

        for iteration in range(max_iterations):
            # Call Claude con tools
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                tools=self.tools,
                messages=messages
            )

            # Check if done
            if response.stop_reason == "end_turn":
                # Extract final answer
                final_text = next(
                    (block.text for block in response.content if hasattr(block, 'text')),
                    None
                )
                return final_text

            # Process tool uses
            if response.stop_reason == "tool_use":
                # Add assistant response
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                # Execute tools
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input

                        print(f"Calling tool: {tool_name} with {tool_input}")

                        # Execute
                        try:
                            result = self.tool_functions[tool_name](**tool_input)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": json.dumps(result)
                            })
                        except Exception as e:
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": f"Error: {str(e)}",
                                "is_error": True
                            })

                # Add tool results
                messages.append({
                    "role": "user",
                    "content": tool_results
                })

        return "Max iterations reached"

# 4. Uso del agent
agent = ToolUseAgent(client, tools)

# Query compleja que requiere múltiples tools
result = await agent.run(
    "What's the weather in Tokyo? Also search our database for hotels there and calculate the total cost for 3 nights at an average of $150 per night."
)

print(result)

# 5. Parallel tool calling
async def parallel_tool_execution(client, user_message, tools):
    """Execute multiple tools in parallel when possible"""

    response = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        tools=tools,
        messages=[{"role": "user", "content": user_message}]
    )

    if response.stop_reason == "tool_use":
        # Collect all tool uses
        tool_uses = [
            block for block in response.content
            if block.type == "tool_use"
        ]

        # Execute in parallel
        import asyncio

        async def execute_tool(tool_use):
            tool_func = tool_functions[tool_use.name]
            if asyncio.iscoroutinefunction(tool_func):
                result = await tool_func(**tool_use.input)
            else:
                result = tool_func(**tool_use.input)
            return tool_use.id, result

        results = await asyncio.gather(*[
            execute_tool(tu) for tu in tool_uses
        ])

        # Format results
        tool_results = [
            {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": json.dumps(result)
            }
            for tool_id, result in results
        ]

        return tool_results
```

---

## CATEGORÍA 2: Agent Architectures

### 2.1 ReAct Pattern (Reasoning + Acting)
**Dificultad:** ⭐⭐⭐⭐⭐

```python
class ReActAgent:
    def __init__(self, client, tools, max_steps=10):
        self.client = client
        self.tools = tools
        self.max_steps = max_steps

    def create_react_prompt(self, task, scratchpad):
        tools_description = "\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in self.tools
        ])

        return f"""You are an agent that can use tools to accomplish tasks.

Available tools:
{tools_description}

Follow this pattern:
Thought: [reasoning about what to do next]
Action: [tool name]
Action Input: [tool input as JSON]
Observation: [tool result will be provided]

Repeat Thought/Action/Observation until you can provide Final Answer.

Task: {task}

{scratchpad}

Next step:"""

    async def run(self, task):
        scratchpad = ""

        for step in range(self.max_steps):
            # Generate next action
            prompt = self.create_react_prompt(task, scratchpad)

            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.content[0].text
            scratchpad += text + "\n"

            # Check if final answer
            if "Final Answer:" in text:
                final_answer = text.split("Final Answer:")[1].strip()
                return {
                    'answer': final_answer,
                    'steps': scratchpad,
                    'num_steps': step + 1
                }

            # Parse action
            if "Action:" in text and "Action Input:" in text:
                action = self.parse_action(text)

                if action:
                    # Execute tool
                    result = await self.execute_tool(action['name'], action['input'])
                    scratchpad += f"Observation: {result}\n\n"
                else:
                    scratchpad += "Observation: Failed to parse action\n\n"
            else:
                # Invalid format, prompt to continue
                scratchpad += "Observation: Please provide Action and Action Input\n\n"

        return {
            'answer': 'Max steps reached',
            'steps': scratchpad,
            'num_steps': self.max_steps
        }

    def parse_action(self, text):
        try:
            action_line = [l for l in text.split('\n') if l.startswith('Action:')][0]
            input_line = [l for l in text.split('\n') if l.startswith('Action Input:')][0]

            action_name = action_line.split('Action:')[1].strip()
            action_input = input_line.split('Action Input:')[1].strip()

            # Parse JSON input
            import json
            action_input = json.loads(action_input)

            return {
                'name': action_name,
                'input': action_input
            }
        except:
            return None

    async def execute_tool(self, tool_name, tool_input):
        # Find tool function
        if tool_name in self.tool_functions:
            try:
                result = self.tool_functions[tool_name](**tool_input)
                return str(result)
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return f"Tool '{tool_name}' not found"

# Uso
agent = ReActAgent(client, tools)
result = await agent.run(
    "Find the weather in San Francisco and book a hotel if it's sunny"
)
```

---

### 2.2 Multi-Agent Systems
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from enum import Enum
from dataclasses import dataclass
from typing import List

class AgentRole(Enum):
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"
    CRITIC = "critic"
    COORDINATOR = "coordinator"

@dataclass
class Message:
    sender: AgentRole
    receiver: AgentRole
    content: str
    metadata: dict

class Agent:
    def __init__(self, role: AgentRole, client, system_prompt: str):
        self.role = role
        self.client = client
        self.system_prompt = system_prompt
        self.memory = []

    async def process(self, message: Message) -> Message:
        # Add message to memory
        self.memory.append(message)

        # Create conversation context
        context = self.build_context()

        # Generate response
        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": context}
            ]
        )

        response_text = response.content[0].text

        # Create response message
        response_msg = Message(
            sender=self.role,
            receiver=message.sender,
            content=response_text,
            metadata={"timestamp": time.time()}
        )

        self.memory.append(response_msg)
        return response_msg

    def build_context(self) -> str:
        context = f"You are a {self.role.value}.\n\n"
        context += "Conversation history:\n"

        for msg in self.memory[-5:]:  # Last 5 messages
            context += f"{msg.sender.value}: {msg.content}\n\n"

        return context

class MultiAgentSystem:
    def __init__(self, client):
        self.client = client
        self.agents = {}

        # Create specialized agents
        self.agents[AgentRole.RESEARCHER] = Agent(
            role=AgentRole.RESEARCHER,
            client=client,
            system_prompt="""You are a research specialist. Your job is to:
- Gather relevant information
- Find credible sources
- Identify key facts and data points
- Present findings clearly"""
        )

        self.agents[AgentRole.ANALYST] = Agent(
            role=AgentRole.ANALYST,
            client=client,
            system_prompt="""You are an analyst. Your job is to:
- Analyze data and findings
- Identify patterns and insights
- Draw conclusions
- Make recommendations"""
        )

        self.agents[AgentRole.WRITER] = Agent(
            role=AgentRole.WRITER,
            client=client,
            system_prompt="""You are a writer. Your job is to:
- Create clear, engaging content
- Structure information logically
- Adapt tone for audience
- Ensure clarity and coherence"""
        )

        self.agents[AgentRole.CRITIC] = Agent(
            role=AgentRole.CRITIC,
            client=client,
            system_prompt="""You are a critic. Your job is to:
- Identify weaknesses and gaps
- Suggest improvements
- Challenge assumptions
- Ensure quality"""
        )

        self.agents[AgentRole.COORDINATOR] = Agent(
            role=AgentRole.COORDINATOR,
            client=client,
            system_prompt="""You are a coordinator. Your job is to:
- Assign tasks to appropriate agents
- Manage workflow
- Synthesize outputs
- Ensure project completion"""
        )

    async def run_workflow(self, task: str):
        # Start with coordinator
        initial_msg = Message(
            sender=AgentRole.COORDINATOR,
            receiver=AgentRole.COORDINATOR,
            content=f"New task: {task}",
            metadata={}
        )

        # Workflow: Research -> Analyze -> Write -> Critique -> Revise
        workflow = [
            (AgentRole.COORDINATOR, AgentRole.RESEARCHER, "Please research this topic"),
            (AgentRole.RESEARCHER, AgentRole.ANALYST, "Here are my findings, please analyze"),
            (AgentRole.ANALYST, AgentRole.WRITER, "Based on analysis, please write a report"),
            (AgentRole.WRITER, AgentRole.CRITIC, "Please review this draft"),
            (AgentRole.CRITIC, AgentRole.WRITER, "Please revise based on feedback"),
            (AgentRole.WRITER, AgentRole.COORDINATOR, "Final version ready")
        ]

        current_msg = initial_msg

        for sender_role, receiver_role, instruction in workflow:
            print(f"\n{sender_role.value} -> {receiver_role.value}")

            # Get agent
            agent = self.agents[receiver_role]

            # Add instruction to message
            msg = Message(
                sender=sender_role,
                receiver=receiver_role,
                content=f"{instruction}\n\nPrevious output:\n{current_msg.content}",
                metadata={}
            )

            # Process
            response = await agent.process(msg)
            print(f"Response: {response.content[:200]}...")

            current_msg = response

        return current_msg.content

# Uso
system = MultiAgentSystem(client)
final_output = await system.run_workflow(
    "Write a comprehensive analysis of AI trends in 2024"
)
```

---

## CATEGORÍA 3: RAG (Retrieval-Augmented Generation)

### 3.1 Vector Database Integration
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorStore:
    def __init__(self, embedding_model='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(embedding_model)
        self.dimension = self.model.get_sentence_embedding_dimension()

        # FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)

        # Metadata storage
        self.documents = []
        self.metadata = []

    def add_documents(self, texts: List[str], metadata: List[dict] = None):
        # Generate embeddings
        embeddings = self.model.encode(texts, show_progress_bar=True)

        # Add to FAISS
        self.index.add(embeddings.astype('float32'))

        # Store documents
        self.documents.extend(texts)
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{}] * len(texts))

    def search(self, query: str, k: int = 5):
        # Encode query
        query_embedding = self.model.encode([query])

        # Search
        distances, indices = self.index.search(
            query_embedding.astype('float32'),
            k
        )

        # Return results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                results.append({
                    'text': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'score': float(distances[0][i])
                })

        return results

    def save(self, path: str):
        import pickle

        faiss.write_index(self.index, f"{path}/index.faiss")

        with open(f"{path}/documents.pkl", 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'metadata': self.metadata
            }, f)

    def load(self, path: str):
        import pickle

        self.index = faiss.read_index(f"{path}/index.faiss")

        with open(f"{path}/documents.pkl", 'rb') as f:
            data = pickle.load(f)
            self.documents = data['documents']
            self.metadata = data['metadata']

# 2. Advanced RAG with reranking
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class AdvancedRAG:
    def __init__(self, vector_store, client, reranker_model='cross-encoder/ms-marco-MiniLM-L-6-v2'):
        self.vector_store = vector_store
        self.client = client

        # Reranker for better relevance
        self.reranker_tokenizer = AutoTokenizer.from_pretrained(reranker_model)
        self.reranker_model = AutoModelForSequenceClassification.from_pretrained(reranker_model)

    def rerank(self, query: str, documents: List[str], top_k: int = 3):
        # Compute cross-encoder scores
        pairs = [[query, doc] for doc in documents]

        inputs = self.reranker_tokenizer(
            pairs,
            padding=True,
            truncation=True,
            return_tensors='pt',
            max_length=512
        )

        with torch.no_grad():
            scores = self.reranker_model(**inputs).logits.squeeze()

        # Sort by score
        scores = scores.cpu().numpy()
        sorted_indices = np.argsort(scores)[::-1][:top_k]

        return [documents[i] for i in sorted_indices]

    async def query(self, question: str, top_k: int = 10, rerank_k: int = 3):
        # 1. Retrieve candidates
        results = self.vector_store.search(question, k=top_k)
        documents = [r['text'] for r in results]

        # 2. Rerank
        if len(documents) > rerank_k:
            documents = self.rerank(question, documents, top_k=rerank_k)

        # 3. Build context
        context = "\n\n---\n\n".join([
            f"Document {i+1}:\n{doc}"
            for i, doc in enumerate(documents)
        ])

        # 4. Generate answer
        prompt = f"""Answer the question based on the provided context.

Context:
{context}

Question: {question}

Instructions:
- Only use information from the context
- If the context doesn't contain the answer, say so
- Cite which document(s) you're using

Answer:"""

        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            'answer': response.content[0].text,
            'sources': documents
        }

# 3. Chunking strategies
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """Chunk text with overlap to preserve context"""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

def semantic_chunking(text: str, model, threshold: float = 0.5):
    """Chunk based on semantic similarity"""
    sentences = text.split('. ')
    embeddings = model.encode(sentences)

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        # Compute similarity with previous sentence
        similarity = np.dot(embeddings[i], embeddings[i-1])

        if similarity < threshold:
            # Start new chunk
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = [sentences[i]]
        else:
            current_chunk.append(sentences[i])

    chunks.append('. '.join(current_chunk) + '.')
    return chunks

# 4. Hybrid search (keyword + semantic)
class HybridRAG:
    def __init__(self, vector_store, client):
        self.vector_store = vector_store
        self.client = client

        # BM25 for keyword search
        from rank_bm25 import BM25Okapi
        self.bm25 = BM25Okapi([doc.split() for doc in vector_store.documents])

    def hybrid_search(self, query: str, k: int = 10, alpha: float = 0.5):
        """
        Combine semantic and keyword search
        alpha: weight for semantic search (1-alpha for BM25)
        """
        # Semantic search
        semantic_results = self.vector_store.search(query, k=k*2)
        semantic_scores = {
            r['text']: 1 / (1 + r['score'])  # Convert distance to similarity
            for r in semantic_results
        }

        # BM25 search
        bm25_scores = self.bm25.get_scores(query.split())
        bm25_results = {
            self.vector_store.documents[i]: score
            for i, score in enumerate(bm25_scores)
        }

        # Combine scores
        all_docs = set(semantic_scores.keys()) | set(bm25_results.keys())
        combined_scores = {}

        for doc in all_docs:
            sem_score = semantic_scores.get(doc, 0)
            bm25_score = bm25_results.get(doc, 0)

            # Normalize and combine
            combined = alpha * sem_score + (1 - alpha) * bm25_score
            combined_scores[doc] = combined

        # Sort and return top k
        sorted_docs = sorted(
            combined_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:k]

        return [doc for doc, score in sorted_docs]
```

---

## Resumen Prioridades Agentic/GenAI

| Tema | Dificultad | Criticidad | Frecuencia | Prioridad |
|------|------------|------------|------------|-----------|
| Prompt Engineering | 5 | 5 | 5 | **CRÍTICA** |
| Function Calling | 5 | 5 | 5 | **CRÍTICA** |
| RAG Implementation | 5 | 5 | 4 | **CRÍTICA** |
| Agent Architectures | 5 | 4 | 4 | **ALTA** |
| Multi-Agent Systems | 5 | 4 | 3 | **ALTA** |
| Vector Databases | 4 | 5 | 4 | **ALTA** |
