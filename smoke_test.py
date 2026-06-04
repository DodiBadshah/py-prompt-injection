from llm_probe.runner.runner import Runner
from llm_probe.payloads.loader import load_all_payloads

payloads = load_all_payloads()
print(f"Loaded {len(payloads)} payloads")

r = Runner("anthropic")
print("Runner instantiated OK")