from openai import OpenAI
import time
client= OpenAI()


assistant = client.beta.assistants.create(
    name = "Study Buddy",
    model = "gpt-3.5-turbo",
    instructions = "You are a study partner for students who are newer to technology. When you answer prompts, do so with simple language suitable for someone learning fundamental concepts.",
    tools=[]
)

thread = client.beta.threads.create()

user_input = input("Hello! I'm here to help. Please type your message.")

message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = user_input
)

run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id
)

while True:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id = thread.id,
        run_id = run.id
    )
    if run.status == "completed":
        break


if run.status == "completed":
    thread_messages = client.beta.threads.messages.list(
        thread_id = thread.id
    )
    message_for_user = thread_messages.data[0].content[0].text.value
    print(message_for_user)

