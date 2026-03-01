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

        self.model.eval()

    def generate_explanation(self, violation, rag_context):
        context_text = "\n\n".join([c["text"] for c in rag_context])

        prompt = f"""
### Instruction:
You are a senior cloud security engineer reviewing infrastructure.

### Violation:
Resource: {violation["resource"]}
Issue: {violation["issue"]}
Severity: {violation["severity"]}

### Security Context:
{context_text}

### Task:
Explain:
1. Security risk
2. Compliance impact (CIS reference if applicable)
3. Clear remediation steps

### Answer:
"""

        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=250,
                do_sample=False,      # deterministic (better for CI)
                temperature=None      # remove warning
            )

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # 🔥 Remove prompt from output
        response = decoded.split("### Answer:")[-1].strip()

        # Optional cleanup
        if "###" in response:
            response = response.split("###")[0].strip()

        return response