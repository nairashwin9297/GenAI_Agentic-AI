from dataclasses import dataclass
from autogen_core._serialization import MessageSerializer, JSON_DATA_CONTENT_TYPE
import json

@dataclass
class SQLTranslationRequest:
    natural_language_query: str
    database_schema: dict
    request_id: str

@dataclass
class SQLTranslationResponse:
    sql_query: str
    request_id: str
    error: str = None

class SQLTranslationRequestSerializer(MessageSerializer[SQLTranslationRequest]):
    @property
    def data_content_type(self) -> str:
        return JSON_DATA_CONTENT_TYPE
    
    @property
    def type_name(self) -> str:
        return "SQLTranslationRequest"
    
    def serialize(self, message: SQLTranslationRequest) -> bytes:
        data = {
            "natural_language_query": message.natural_language_query,
            "database_schema": message.database_schema,
            "request_id": message.request_id
        }
        return json.dumps(data).encode('utf-8')
    
    def deserialize(self, payload: bytes) -> SQLTranslationRequest:
        data = json.loads(payload.decode('utf-8'))
        return SQLTranslationRequest(
            natural_language_query=data["natural_language_query"],
            database_schema=data["database_schema"],
            request_id=data["request_id"]
        )

class SQLTranslationResponseSerializer(MessageSerializer[SQLTranslationResponse]):
    @property
    def data_content_type(self) -> str:
        return JSON_DATA_CONTENT_TYPE
    
    @property
    def type_name(self) -> str:
        return "SQLTranslationResponse"
    
    def serialize(self, message: SQLTranslationResponse) -> bytes:
        data = {
            "sql_query": message.sql_query,
            "request_id": message.request_id,
            "error": message.error
        }
        return json.dumps(data).encode('utf-8')
    
    def deserialize(self, payload: bytes) -> SQLTranslationResponse:
        data = json.loads(payload.decode('utf-8'))
        return SQLTranslationResponse(
            sql_query=data["sql_query"],
            request_id=data["request_id"],
            error=data.get("error")
        )