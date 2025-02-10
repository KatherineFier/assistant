from openai import OpenAI
import time
import logging
import datetime
import random

log = logging.getLogger("assistant")
logging.basicConfig(filename = "assistant.log", level = logging.INFO)

client= OpenAI()

# After uploading the file to the OpenAI platform, this block of code and print statement can be removed and the code below can be uncommented.
# flower_knowledge = client.files.create(
#     file=open("knowledge/BFF_Flower_Facts_2025_v1.pdf", "rb"),
#     purpose="assistants"
# )
# print(flower_knowledge)

def process_run(thread_id, assistant_id):
    new_run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id = assistant_id
)

    phrases = ["Thinking", "Pondering", "Dotting the i's"]

    while True:
        time.sleep(1)
        print(random.choice(phrases) + "...")
        run_check = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=new_run.id
        )
        if run_check.status in ["cancelled", "failed", "completed", "expired"]:
            return run_check

def log_run(run_status):
    if run_status in ["cancelled", "failed", "expired"]:
        log.error(str(datetime.datetime.now()) + "Run" + run_status + "\n")



assistant = client.beta.assistants.create(
    name = "Social Media Assistant",
    model = "gpt-3.5-turbo",
    # specific to Boulder Flower Farm
    instructions = """You are a social media and copywriting expert. You know how to keep the tone authentic to the Boulder Flower Farm brand.
    You can find our website at BoulderFlowerFarm.com to get a sense of our tone and instagram page at Instagram.com/BoulderFLowerFarm. We values the outdoors
    and bringing more nature and beauty in the world. That said we don't like fluff in our writing. We are direct, down to earth, and positive.
    You know everything there is to know about growing flowers.""",
    tools=[{
        "type": "file_search"
    }]
)

thread = client.beta.threads.create ()

user_input = ""

while True:
    if (user_input == ""):
        user_input = input("Hi! I'm your social media assistant. How can I help you today? You can type exit to end this chat. You: ")
    else:
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

