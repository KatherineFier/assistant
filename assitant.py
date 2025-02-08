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

while True:
    time.sleep(1)