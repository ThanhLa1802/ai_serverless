# 📄 Serverless RAG Chatbot on AWS

A **production-ready Serverless Retrieval-Augmented Generation (RAG) system** built on AWS Lambda, API Gateway, Pinecone, and OpenAI. The system allows users to upload documents (PDF) and ask natural language questions via a ChatGPT-like web UI.

---<img width="1310" height="580" alt="rag" src="https://github.com/user-attachments/assets/5e465dd7-e0fb-449e-b372-9a6e7ed2eee6" />


## 🚀 Key Features

- 🔍 **Semantic Search (RAG)** using vector embeddings
- 📚 **PDF ingestion & chunking**
- 🧠 **LLM-based answer generation** (OpenAI)
- ⚡ **Serverless architecture** (AWS Lambda + API Gateway)
- 🐳 **Container-based Lambda (ECR)**
- 🌐 **ChatGPT-like Web UI** (pure HTML/CSS/JS)
- 🔐 Secrets managed via **GitHub Secrets**
- 📦 Infrastructure as Code with **Terraform**
- 🔄 CI/CD with **GitHub Actions**

---

## 🏗️ High-Level Architecture

```
User (Browser)
   ↓
index.html (Chat UI)
   ↓  POST /ask
AWS API Gateway
   ↓
AWS Lambda (Query Handler)
   ├─ Retrieval → Pinecone Vector DB
   └─ Generation → OpenAI Chat Model
   ↓
Answer returned to UI
```

A separate **Ingestion Lambda** is used to process and embed documents.

---

## 📂 Project Structure

```
SERVERLESS_RAG_PROJECT
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline
├── infra/                      # Terraform IaC
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── src/
│   ├── common/
│   │   └── logger.py
│   ├── ingestion/
│   │   ├── handler.py          # Document ingestion Lambda
│   │   └── service.py
│   └── retrieval/
│       ├── handler.py          # Query Lambda
│       ├── search.py
│       └── generator.py
├── index.html                  # ChatGPT-like frontend
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🧠 RAG Flow Explained

### 1️⃣ Ingestion Phase

- Upload PDF documents
- Extract text per page
- Split text into chunks
- Generate embeddings using **OpenAI Embeddings**
- Store vectors in **Pinecone**

### 2️⃣ Query Phase

- User submits a question
- Convert question to embedding
- Perform similarity search in Pinecone
- Retrieve top-K relevant chunks
- Inject context into prompt
- Generate final answer via OpenAI Chat Model

---

## 🛠️ Technology Stack

| Layer | Technology |
|-----|-----------|
| Frontend | HTML, CSS, Vanilla JS |
| API | AWS API Gateway |
| Compute | AWS Lambda (Container Image) |
| Container | Docker + Amazon ECR |
| Vector DB | Pinecone |
| Embeddings | OpenAI `text-embedding-3-small` |
| LLM | OpenAI Chat Models |
| IaC | Terraform |
| CI/CD | GitHub Actions |

---

## 🔐 Environment Variables

Configured via **GitHub Secrets** and injected by Terraform:

```env
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_INDEX_NAME=
PINECONE_NAMESPACE=default
```

> ⚠️ Changing env vars **does NOT require rebuilding Docker images** — only a redeploy.

---

## 🔄 CI/CD Pipeline (GitHub Actions)

Triggered on push to `master`:

1. Checkout code
2. Build Docker image
3. Push image to Amazon ECR
4. Run Terraform
5. Update Lambda functions

Image tagging strategy:
- `latest`
- `${GITHUB_SHA}` (immutable)

---

## 🐳 Docker & Lambda

- Base image: `public.ecr.aws/lambda/python:3.12`
- Optimized for fast cold start
- No heavy ML libraries (no `torch`, no `sentence-transformers`)

Lambda handlers:

```python
src.ingestion.handler.handler
src.retrieval.handler.handler
```

---

## 🌐 Frontend Usage

Open `index.html` in a browser and ask questions:

```json
POST /ask
{
  "query": "What is the main content of ML.pdf?"
}
```

Features:
- ChatGPT-style UI
- User / Bot message alignment
- Loading indicator
- CORS enabled

---

## 💰 Cost Considerations

- 💵 Pay-as-you-go (OpenAI)
- Pinecone: free / starter tier suitable for small docs
- AWS Lambda: extremely low cost for light usage

Example:
- 1 PDF (~6 pages): **< $0.01** embedding cost
- Typical query: **fractions of a cent**

---

## ✅ Production Best Practices Applied

- No secrets in Docker images
- Immutable image tags
- Environment-based configuration
- Stateless Lambdas
- Warm-start optimization

---

## 🚧 Future Improvements

- 🔐 Authentication (Cognito / JWT)
- 📎 Source citation in answers
- 🔄 Streaming responses
- 📊 Observability & metrics
- 🌍 Multi-language support

---

## 👤 Author

Built by **Thanh** – Backend Engineer

> Focused on AWS, Serverless, and AI-powered systems.

---

## ⭐ Summary

This project demonstrates a **clean, scalable, and production-ready RAG architecture** using modern cloud-native and AI technologies.

If you are learning **Serverless + GenAI**, this is a solid real-world reference.

