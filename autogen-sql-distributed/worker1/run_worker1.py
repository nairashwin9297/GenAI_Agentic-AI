import asyncio
import os
import sys
sys.path.append('/app/shared')

from messages import *
from autogen_core import MessageContext, RoutedAgent, message_handler, AgentId
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime

class SQLRequesterAgent(RoutedAgent):
    def __init__(self, translator_agent_id: AgentId) -> None:
        super().__init__("SQLRequesterAgent")
        self.translator_agent_id = translator_agent_id
        self.pending_requests = {}
    
    @message_handler
    async def handle_sql_response(self, message: SQLTranslationResponse, ctx: MessageContext) -> None:
        print(f"[Requester] Received SQL response for request {message.request_id}")
        
        if message.error:
            print(f"[Requester] Error: {message.error}")
        else:
            print(f"[Requester] Generated SQL: {message.sql_query}")

async def main():
    # Get host address from environment
    host_address = os.environ.get("HOST_ADDRESS", "host:50051")
    

    
    print(f"🚀 Worker 1 starting...")
    print(f"🔗 Connecting to host at {host_address}")
    
    worker1 = GrpcWorkerAgentRuntime(host_address=host_address)
    worker1.add_message_serializer(SQLTranslationRequestSerializer())
    worker1.add_message_serializer(SQLTranslationResponseSerializer())
    
    await worker1.start()
    
    translator_id = AgentId("sql_translator", "default")
    
    await SQLRequesterAgent.register(
        worker1, 
        "sql_requester", 
        lambda: SQLRequesterAgent(translator_id)
    )
    
    print("Worker 1 (SQL Requester) connected and ready")
    
    # Send a test request after a delay
    await asyncio.sleep(5)  # Wait for other worker to be ready
    
    sample_schema = {
        "tables": {
            "users": {
                "columns": {
                    "id": "INTEGER PRIMARY KEY",
                    "name": "VARCHAR(100)",
                    "email": "VARCHAR(255)",
                    "created_at": "TIMESTAMP"
                }
            },
            "orders": {
                "columns": {
                    "id": "INTEGER PRIMARY KEY",
                    "user_id": "INTEGER",
                    "product_name": "VARCHAR(200)",
                    "amount": "DECIMAL(10,2)",
                    "order_date": "DATE"
                }
            }
        }
    }
    
    request = SQLTranslationRequest(
        natural_language_query="Show me all users who placed orders in the last 30 days",
        database_schema=sample_schema,
        request_id="test-001"
    )
    
    print("Sending SQL translation request...")
    await worker1.send_message(request, translator_id)
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await worker1.stop()

if __name__ == "__main__":
    asyncio.run(main())