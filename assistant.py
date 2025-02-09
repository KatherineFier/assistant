from openai import OpenAI
import time
client= OpenAI()

def process_run(thread_id, assistant_id):
    new_run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id = assistant_id
)

    while True:
        time.sleep(1)
        run_check = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=new_run.id
        )
        if run_check.status in ["cancelled", "failed", "completed", "expired"]:
            return run_check


assistant = client.beta.assistants.create(
    name = "Study Buddy",
    model = "gpt-3.5-turbo",
    instructions = "You are a study partner for students who are newer to technology. When you answer prompts, do so with simple language suitable for someone learning fundamental concepts.",
    tools=[]
)

thread = client.beta.threads.create()

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        exit()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    run = process_run(thread.id, assistant.id)

    if run.status == "completed":
        thread_messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )

        print("\nAssistant: " + thread_messages.data[0].content[0].text.value + "\n")

    if run.status in ["cancelled", "failed", "expired"]:
        print("\nAssistant: An error has occurred, please try again.\n")


    # if run_check.status == "completed":
    #     thread_messages = client.beta.threads.messages.list(
    #         thread_id = thread.id
    #     )
    #     message_for_user = thread_messages.data[0].content[0].text.value
    #     print(message_for_user)

