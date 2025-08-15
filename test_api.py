import uuid
from langgraph_sdk import get_client as get_client_sdk
from langchain_core.messages import HumanMessage

client = get_client_sdk(url="http://localhost:8001")
# client = get_client_sdk(url="http://172.16.251.149:9062/openapi/v2/graph/api/v1.0/graphApp/62996c31ef3a34563602a1a0820ea505")
graph_id = "agent"
thread_id = str(uuid.uuid4())
async def test_stream_run():
    thread = await client.threads.create(thread_id=thread_id)
    print(f"thread_id: {thread_id}")
    input_data = {
        "messages": [
            {
                "role": "user",
                "content": "创建一个9月1日开会的日程"
            }
        ]
    }
    assistant = await client.assistants.create(
        graph_id=graph_id,
        name="Test Assistant"

    )
    
    # 使用stream模式
    async for chunk in client.runs.stream(
        thread_id,
        assistant["assistant_id"],
        input=input_data,
        stream_mode=["updates"]

    ):
        print(chunk)

    search_thread_res = await client.threads.search()
    print("#"*30)
    print("search thread result:", search_thread_res)

async def run_tests():
    print("stream run start" + "#"*100)
    await test_stream_run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_tests())
