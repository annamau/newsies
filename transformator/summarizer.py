import json, os, time, torch, transformers

start = time.time()

os.environ['HF_TOKEN'] = "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"

model_id = "microsoft/Phi-3-mini-4k-instruct"
pipeline = transformers.pipeline(
    "text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device="cuda", max_new_tokens=4000
)

with open("data/confidencial.json", "r") as f:
    conf = json.load(f)
    
text = conf["1"]["text"]

print(pipeline(f"Eres un reportero, resume este articulo en 3 lineas: \n {text}"))

end = time.time()
print(f"  - Total time to summarize: {end - start}s \n")