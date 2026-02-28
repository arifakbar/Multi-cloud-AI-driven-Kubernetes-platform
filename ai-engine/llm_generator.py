import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = os.getenv(
    "LLM_MODEL",
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)


class LLMGenerator:
    def __init__(self):
        print(f"Loading model: {MODEL_NAME}")

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float32,
            device_map="cpu"
        )

    def generate_explanation(self, violation, rag_context):
        context_text = "\n\n".join([c["text"] for c in rag_context])

        prompt = f"""
You are a cloud security expert.

Violation:
Resource: {violation["resource"]}
Issue: {violation["issue"]}
Severity: {violation["severity"]}

Security Context:
{context_text}

Explain risk, compliance impact, and remediation.
"""

        inputs = self.tokenizer(prompt, return_tensors="pt")

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.2
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)