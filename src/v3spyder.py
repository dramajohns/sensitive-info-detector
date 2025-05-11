import torch
import re
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# Configuration
model_path = "C:/STUDY/deepseek-coder-6.7/deepseek-coder-6.7b-base"
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

# Load model
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=quant_config,
    device_map="auto"
).eval()

# Comprehensive regex patterns
SENSITIVE_PATTERNS = {
    'Email': (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'email'),
    'Phone': (r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', 'phone'),
    'ID Number': (r'\b\d{6,12}\b', 'identification'),
    'Date': (r'\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12][0-9]|3[01])[/-](?:\d{4}|\d{2})\b|\b\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4}\b', 'date'),
    'Location': (r'\b(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b.+?\b(?:[A-Z]{2}\s\d{5}|\w+\s\w+)\b', 'address')
}

def contains_sensitive_info(text):
    """LLM-based detection (fast binary check)"""
    prompt = f"""Does this text contain sensitive information (emails, phones, IDs, etc.)?
    : {text[:2000]}
    Answer format: YES|NO|MAYBE"""
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens=5,

        do_sample=False
    )
    
    response = tokenizer.decode(outputs[0]).split('|')[0].strip().lower()
    return response in ('yes', 'maybe')

def extract_with_regex(text):
    """Enhanced extraction with context"""
    findings = {}
    for data_type, (pattern, context) in SENSITIVE_PATTERNS.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        findings[data_type] = [{
            'value': m.group(),
            'start': m.start(),
            'end': m.end(),
            'context': context
        } for m in matches]
    return {k: v for k, v in findings.items() if v}

def generate_report(findings, redacted_text):
    """Detailed markdown report"""
    report = ["# Sensitive Data Analysis Report\n"]
    
    # Summary section
    report.append("## Summary")
    report.append(f"- Total findings: {sum(len(v) for v in findings.values())}")
    for data_type, matches in findings.items():
        report.append(f"- {data_type}: {len(matches)} detected")
    
    # Detailed findings
    report.append("\n## Detailed Findings")
    for data_type, matches in findings.items():
        report.append(f"\n### {data_type}")
        report.append("| Value | Context | Position |")
        report.append("|-------|---------|----------|")
        for m in matches:
            report.append(f"| {m['value']} | {m['context']} | {m['start']}-{m['end']} |")
    
    # Redaction preview
    report.append("\n## Redaction Preview")
    report.append("```")
    report.append(redacted_text[:500] + ("..." if len(redacted_text) > 500 else ""))
    report.append("```")
    
    return '\n'.join(report)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if not contains_sensitive_info(text):
        return {"status": "clean", "report": "No sensitive data detected"}
    
    findings = extract_with_regex(text)
    redacted = redact_text(text, findings)
    
    # Save outputs
    base_name = file_path.rsplit('.', 1)[0]
    with open(f"{base_name}_REDACTED.txt", 'w') as f:
        f.write(redacted)
    
    report = generate_report(findings, redacted)
    with open(f"{base_name}_REPORT.md", 'w') as f:
        f.write(report)
    
    return {
        "status": "sensitive_data_found",
        "findings_count": sum(len(v) for v in findings.values()),
        "report": report[:1000] + ("..." if len(report) > 1000 else "")
    }
# Example Usage
filepath = "C:/Users/fedib/Desktop/extra.txt"
result = process_file(filepath)
print(result['report'])