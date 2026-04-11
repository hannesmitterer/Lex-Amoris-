# Aggiungi questo a monitoring/resonance_check.py per gestire i diversi provider

class ProviderAdapter:
    """Adattatore per mappare le risposte dei diversi modelli al protocollo NSR."""
    
    @staticmethod
    def extract_content(response: dict, provider: str) -> str:
        if provider == "openai":
            return response['choices'][0]['message']['content']
        elif provider == "anthropic":
            return response['content'][0]['text']
        elif provider == "gemini":
            return response.candidates[0].content.parts[0].text
        return str(response)

# Integrazione nel ciclo di test
def run_resonance_suite(prompts: list, provider: str):
    """Esegue la suite di test e calcola il Sentimento Rhythm globale."""
    results = []
    for p in prompts:
        raw_resp = call_provider(p, provider)
        content = ProviderAdapter.extract_content(raw_resp, provider)
        
        # Calcolo metriche deterministiche (NSR-Shielded)
        metrics = SentimentoMetrics(
            semantic_entropy=calculate_semantic_entropy([content]), # Trials logic here
            boilerplate_rate=detect_patterns(content, BOILERPLATE_PATTERNS),
            refusal_rate=detect_patterns(content, REFUSAL_PATTERNS),
            soil_moisture=get_realtime_moisture()
        )
        
        oracle = compute_sentimento(metrics)
        results.append(oracle)
        
    return summarize_sroi(results)
