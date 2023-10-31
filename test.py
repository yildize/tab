from transformers import AutoModelForCausalLM, AutoTokenizer
import os

from utils.utils import ROOT_PATH

model = AutoModelForCausalLM.from_pretrained('TheBloke/Mistral-7B-Instruct-v0.1-GPTQ', device_map="cuda", cache_dir=os.path.join(ROOT_PATH, "storage", "llms"))
tokenizer = AutoTokenizer.from_pretrained('TheBloke/Mistral-7B-Instruct-v0.1-GPTQ', use_fast=True, cache_dir=os.path.join(ROOT_PATH, "storage", "llms"))

prompt = "Tell me about AI"
prompt_template=f'''<s>[INST] {prompt} [/INST]
'''

print("\n\n*** Generate:")

input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
output = model.generate(inputs=input_ids, temperature=0.7, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=512)
print(tokenizer.decode(output[0]))

from ctransformers import AutoModelForCausalLM