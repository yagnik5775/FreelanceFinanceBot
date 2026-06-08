# Reflection – Freelance Finance Assistant

## LLM Limitations Observed
During evaluation, the chatbot scored 4.99/5 on 20 test questions, but one limitation emerged: the answer about deducting a mixed‑use phone bill, while factually correct, did not strongly emphasize the need for a contemporaneous usage log. This reflects a common LLM weakness – the model may provide accurate information but cannot inherently prioritise the most audit‑critical details unless explicitly prompted.

Another limitation is the lack of real‑time knowledge. Tax rates (e.g., mileage deduction) and regulations change annually; the model is frozen at its training cut‑off. Without external retrieval, it cannot update itself.

## Ethical Considerations
Financial advice carries significant risk. A user might rely entirely on the chatbot and skip consulting a CPA, potentially leading to incorrect tax filings or penalties. The system prompt includes a strong disclaimer and repeatedly recommends professional advice, but user over‑reliance remains an ethical concern. The chatbot also refuses illegal requests (e.g., fake receipts) and out‑of‑scope questions, aligning with responsible AI principles. However, there is still a risk of subtle errors that a non‑expert might miss.

## Two Proposed Improvements
1. **Add retrieval‑augmented generation (RAG) with IRS publications** – Ground answers in official PDFs to reduce hallucination and ensure up‑to‑date rates and rules.
2. **Implement a “disclaimer confidence” check** – Before answering high‑stakes questions (e.g., S‑Corp election), the bot could ask: “This is complex – would you like help finding a CPA in your area?” to nudge users toward professional help.

Overall, the chatbot demonstrates strong domain knowledge and safety, but ongoing guardrails and hybrid human‑AI workflows are essential for high‑stakes domains like finance.