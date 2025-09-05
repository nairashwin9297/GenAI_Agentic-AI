import asyncio
import os
import sys
import json
sys.path.append('/app/shared')

from messages import *
from autogen_core import MessageContext, RoutedAgent, message_handler, AgentId
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

class SQLTranslatorAgent(RoutedAgent):
    def __init__(self, name: str, api_key: str) -> None:
        super().__init__(name)
        
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o",
            api_key=api_key
        )
        
        self._assistant = AssistantAgent(
            name=name,
            model_client=model_client,
            system_message="""You are an expert SQL translator. 
            Convert natural language queries into SQL queries based on the provided database schema.
            Return only the SQL query without any explanation or markdown formatting."""
        )
    
    @message_handler
    async def handle_translation_request(self, message: SQLTranslationRequest, ctx: MessageContext) -> SQLTranslationResponse:
        print(f"[Translator] Received translation request: {message.natural_language_query}")
        
        try:
            schema_str = json.dumps(message.database_schema, indent=2)
            prompt = f"""Database Schema:
{schema_str}

Natural Language Query: {message.natural_language_query}

Generate the SQL query:"""
            
            response = await self._assistant.on_messages(
                [TextMessage(content=prompt, source="user")],
                ctx.cancellation_token
            )
            
            sql_query = response.chat_message.content.strip()
            
            response_msg = SQLTranslationResponse(
                sql_query=sql_query,
                request_id=message.request_id
            )
            
            print(f"[Translator] Sending back SQL: {sql_query}")
            return response_msg
            
        except Exception as e:
            return SQLTranslationResponse(
                sql_query="",
                request_id=message.request_id,
                error=str(e)
            )

async def main():
    host_address = os.environ.get("HOST_ADDRESS", "host:50051")
    api_key = os.environ.get("OPENAI_API_KEY")
    
    print(f"🚀 Worker 2 starting...")
    print(f"🔗 Connecting to host at {host_address}")
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        return
    else:
        print("✅ OpenAI API key found")
    
    print(f"Worker 2 starting, connecting to {host_address}")
    
    worker2 = GrpcWorkerAgentRuntime(host_address=host_address)
    worker2.add_message_serializer(SQLTranslationRequestSerializer())
    worker2.add_message_serializer(SQLTranslationResponseSerializer())
    
    await worker2.start()
    
    await SQLTranslatorAgent.register(
        worker2, 
        "sql_translator", 
        lambda: SQLTranslatorAgent("sql_translator", api_key)
    )
    
    print("Worker 2 (SQL Translator) connected and ready")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await worker2.stop()

if __name__ == "__main__":
    asyncio.run(main())