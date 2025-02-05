# Sensitive Information Detection System Documentation

## Overview
This system is designed to analyze documents in various formats (PDF, DOCX, TXT) and identify sensitive information such as Personally Identifiable Information (PII), Financial Data, Health Information, and Confidential Business Data. The system evaluates the risk level associated with the detected information and provides a detailed report.

## Architecture
The system consists of the following components:

1. **Document Processing Pipeline**: Handles different file formats and extracts text content.
2. **NER Model**: Uses Natural Language Processing (NLP) to detect sensitive information.
3. **Risk Assessment**: Assigns a risk score to each detected piece of information.
4. **Report Generation**: Generates a detailed report summarizing the findings.

## Key Algorithms and Techniques
- **NER Model**: Utilizes spaCy or Hugging Face Transformers for entity recognition.
- **Risk Scoring**: Implements a rule-based system to assess the sensitivity of detected information.
- **Document Parsing**: Employs PDFPlumber, python-docx, and built-in libraries for text extraction.

## Installation Instructions
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the server using `uvicorn src.app:app --reload`.

## Usage Examples
- Upload a document to the `/process-document/` endpoint.
- Receive extracted text content with identified sensitive information.
- Use the report to assess and mitigate risks.

## Future Enhancements
- **Anomaly Detection**: Identify unusual patterns in sensitive information.
- **Multi-Language Support**: Detect sensitive information in non-English documents.
- **UI Interface**: Develop a web-based interface for easier interaction.

## Contributing
Contributions are welcome! Fork the repository, make changes, and submit a pull request.
