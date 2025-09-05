from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost
import asyncio
import os

async def main():
    # Bind to all interfaces so workers can connect
    host_address = os.environ.get("HOST_ADDRESS", "0.0.0.0:50051")
    
    host = GrpcWorkerAgentRuntimeHost(address=host_address)
    host.start()
    
    print(f"✅ Central gRPC Runtime Host started on {host_address}")
    print("📡 Waiting for workers to connect...")
    print("-" * 50)
    
    # Keep running until interrupted
    try:
        while True:
            await asyncio.sleep(10)
            print("💓 Host is alive and listening...")
    except KeyboardInterrupt:
        print("\n🛑 Shutting down host...")
        await host.stop()

if __name__ == "__main__":
    asyncio.run(main())