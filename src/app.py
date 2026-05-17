import requests as rq
import json

llm_url = "http://127.0.0.1:11434/api/generate"

print("--------AI Q&A bot---------\n")

print("Type 'exit' to quit.\n")

while True:
    question = input("Enter your question: ")
    if question.lower() == "exit":
        print("Bye!!")
        break
    
    payload = {
        "model" : "llama3.2",
        "prompt" : question
    }
    try:
        response = rq.post(url=llm_url, stream=True, json=payload, timeout=15)
        response.raise_for_status()
        answer = ""
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode("utf-8"))
                text = chunk.get("response", "")
                print(text, end="", flush=True)
                answer += text
                if chunk.get("done") is True:
                    print("")
                    break
    except rq.exceptions.ConnectionError as e:
        print(f"Unable to connect to the model server: {e}")
    except rq.exceptions.ConnectTimeout as e:
        print(f"Connection timedout: {e}")
    except rq.exceptions.Timeout as e:
        print(f"Model took too long to respond: {e}")
    except rq.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except rq.exceptions.JSONDecodeError as e: 
        print(f"The response was not valid JSON: {e}")
    except rq.exceptions.RequestException as e:
        print(f"Some other request error happened: {e}")



