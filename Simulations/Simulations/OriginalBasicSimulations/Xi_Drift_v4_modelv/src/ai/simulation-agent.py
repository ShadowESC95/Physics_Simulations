# src/ai/simulation_agent.py
from langchain.chains import LLMChain

class SimulationAssistant:
    def __init__(self):
        self.llm = load_quantized("Llama-3-70B-Q4_K_M.gguf")
        
    def generate_config(self, prompt):
        return self.llm(f"Create Ξχ config for {prompt} in YAML:")
