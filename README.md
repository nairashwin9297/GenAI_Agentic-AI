# Agentic-AI

# AutoGen Distributed SQL Translation System

## Introduction

This project demonstrates AutoGen as a multi-agent orchestration framework for building distributed AI systems. AutoGen enables networks of specialized agents to communicate and collaborate across different machines, bringing microservices architecture to AI applications.

The implementation showcases:
- **Distributed agents**: SQL requester and translator agents running on separate Docker containers with unique IPs
- **gRPC communication**: AutoGen's message-passing system handles all inter-agent communication
- **LLM integration**: SQL translator agent uses OpenAI GPT-4 for natural language to SQL conversion
- **Production-ready architecture**: Hub-and-spoke design with central message broker for scalability

AutoGen abstracts away the complexity of distributed systems, handling message routing, serialization, and fault tolerance automatically. This allows developers to focus on agent logic rather than infrastructure.

## Overview

This project demonstrates how to build a distributed agent system where:
- Agent 1 (SQL Requester) sends natural language queries with database schema
- Agent 2 (SQL Translator) uses OpenAI to generate SQL queries
- Communication happens via gRPC through a central host
- Each component runs in isolated Docker containers with unique IP addresses

## Architecture

```
Worker 1 (172.20.0.11)     →     Host (172.20.0.10:50051)     ←     Worker 2 (172.20.0.12)
SQL Requester (Client)           gRPC Server (Router)               SQL Translator (Client)
```

### Key Components

1. **Central Host**: gRPC server that routes messages between agents
2. **SQL Requester Agent**: Sends translation requests with database schema
3. **SQL Translator Agent**: Uses OpenAI GPT-4 to generate SQL from natural language
4. **Message Types**: Custom serializable types for request/response

## Prerequisites

- Docker and Docker Compose
- OpenAI API key
- Python 3.11+ (for local development)

## Project Structure

```
autogen-sql-distributed/
├── docker-compose.yml          # Docker orchestration
├── .env                       # Environment variables (create this)
├── shared/
│   └── messages.py           # Message types and serializers
├── host/
│   ├── Dockerfile
│   └── run_host.py          # Central gRPC host
├── worker1/
│   ├── Dockerfile
│   └── run_worker1.py       # SQL Requester agent
└── worker2/
    ├── Dockerfile
    └── run_worker2.py       # SQL Translator agent
```

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd autogen-sql-distributed
```

### 2. Create environment file
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Run the system
```bash
docker-compose up --build
```

## How It Works

1. **Startup**: 
   - Host starts on port 50051
   - Workers connect as clients to the host
   - Each container gets a unique IP address

2. **Message Flow**:
   - Worker 1 sends a `SQLTranslationRequest` with natural language query and schema
   - Host routes the message to Worker 2
   - Worker 2 uses OpenAI to generate SQL
   - Worker 2 returns `SQLTranslationResponse` with the SQL query
   - Host routes the response back to Worker 1

3. **Example Translation**:
   - Input: "Show me all users who placed orders in the last 30 days"
   - Output: `SELECT DISTINCT u.* FROM users u JOIN orders o ON u.id = o.user_id WHERE o.order_date >= CURRENT_DATE - INTERVAL '30 days';`

## Viewing Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f host
docker-compose logs -f worker1
docker-compose logs -f worker2

# Check container status
docker-compose ps

# Inspect network
docker network inspect autogen-sql-distributed_autogen_net
```

## Technical Details

### AutoGen gRPC Architecture
- Uses hub-and-spoke model (not peer-to-peer)
- Workers are clients, only the host is a server
- All communication routes through the central host

### Message Serialization
- Custom `MessageSerializer` implementations for type-safe communication
- JSON serialization for cross-language compatibility

### Docker Networking
- Private network with subnet 172.20.0.0/24
- Each container has a fixed IP address
- Simulates distributed deployment on different machines

## Extending the System

- Add more agent types by creating new worker directories
- Implement different LLM providers in translator agents
- Add persistent storage for translation history
- Scale horizontally by running multiple instances of workers

## Dependencies

- `autogen-core`: Core AutoGen framework
- `autogen-agentchat`: Chat agent implementations
- `autogen-ext`: Extensions including gRPC runtime
- `grpcio`: gRPC Python implementation
- `openai`: OpenAI API client
- `tiktoken`: Token counting for OpenAI

## Acknowledgments

Built with AutoGen 0.6 by Microsoft Research
