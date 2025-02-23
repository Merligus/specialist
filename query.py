# chat
from QWEN import ChatQWEN
from langchain_core.prompts import ChatPromptTemplate

# prompt chat
prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are Qwen, created by Alibaba Cloud. You are a helpful assistant that translates {input_language} to {output_language}.",
        ),
        ("human", "{input}"),
    ]
)

# model creation
llm = ChatQWEN()

# pipeline
chain = prompt | llm

# query
print(
    chain.invoke(
        {
            "input_language": "English",
            "output_language": "German",
            "input": "I love programming",
        }
    ).content
)
