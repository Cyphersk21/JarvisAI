# import os
# import openai
#
# from config import apikey
#
# openai.api_key = apikey
#
# response = openai.Completion.create(
#   model="gpt-3.5-turbo-instruct",
#   prompt="Write an email application to company for software developer fresher position",
#   temperature=1,
#   max_tokens=256,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0
# )
# print(response)
import os
import openai
from config import ChatGPT_apikey
openai.api_key = ChatGPT_apikey

response = openai.Completion.create(
  model="gpt-3.5-turbo-instruct",
  prompt="write an email application to a company for software developer fresher",
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print(response)
