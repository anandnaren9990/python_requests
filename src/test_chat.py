import requests as rq
import json
import time

llm_url="http://127.0.0.1:11434/api/chat"

print("----------AI Q&A Bot -----------\n")

time.sleep(0.08)

print("Enter quit to stop.\n")
messages = [{
    "role" : "system",
    "content" : f"""
            You are an AI Q&A assistant. Explain the answer to the question assuming that the user is a beginner. 
            Keep the out put concise, do not assume things and explain."""
}]

while True:
    question = input("Enter your question: ")

    if question.lower() == "exit":
        print("Bye!!")
        break

    messages.append(
        {
            "role" : "user",
            "content" : question
        }
    )

    recent_messages = messages[:1] + messages[-10:]

    payload = {
        "model" : "llama3.2",
        "messages" : recent_messages,
        "stream" : True
    }

    try:
        response = rq.post(url=llm_url, stream=True, json=payload, timeout=15)
        response.raise_for_status()

        full_answer = ""
        
        for line in response.iter_lines():
            if not line:
                continue

            chunk = json.loads(line.decode("utf-8"))
            text = chunk.get("message",{}).get("content","")
            print(text, end="", flush=True)
            time.sleep(0.08)
            full_answer += text
            if chunk.get("done") is True:
                print("")
                break
        messages.append(
            {
                "role" : "assistant",
                "content" : full_answer
            }
        )
    except rq.exceptions.ConnectionError as e:
        print(f"Error in connecting to model: {e}")
    except rq.exceptions.ConnectTimeout as e:
        print(f"Model took long time to respond: {e}")
    except rq.exceptions.HTTPError as e:
        print(f"Http Error: {e}")
    except rq.exceptions.JSONDecodeError as e: 
        print(f"The response was not valid JSON: {e}")
    except rq.exceptions.RequestException as e:
        print(f"Some other request error happened: {e}")
