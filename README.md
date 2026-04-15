# AI Talent Assessment System

> A production-oriented AI recruitment evaluation system with multi-model fallback, designed for scalable, reliable, and structured candidate assessment.

---

## Overview

AI Talent Assessment System is a lightweight yet extensible platform that automates resume screening and candidate evaluation using large language models.

It enables recruiters and hiring managers to:

* Upload multiple candidate resumes (Word format)
* Define custom evaluation criteria per role
* Perform structured, multi-dimensional assessments
* Rank candidates automatically
* Generate decision-ready summaries
* Export polished reports in Word format

The system is built with a modular architecture and incorporates a **multi-model fallback mechanism** to ensure high availability in real-world usage scenarios.

---

## Key Features

### Structured Candidate Evaluation

* Multi-dimensional scoring (skills, experience, education, potential, communication)
* Strengths, weaknesses, and missing signals detection
* Explicit identification of “not mentioned in resume” capabilities

### Custom Evaluation Criteria

* Fully user-defined hiring standards
* Role-specific scoring logic
* Flexible prompt-driven evaluation

### Batch Processing & Ranking

* Upload multiple resumes simultaneously
* Automated ranking based on total score
* Comparative analysis across candidates

### Multi-Model Resilience Layer

* Primary model: Qwen (Alibaba Cloud)
* Fallback model: DeepSeek
* Automatic retry and failover mechanism
* Zero user disruption during model failure

### Clean Output (Non-JSON)

* Human-readable structured reports
* Clear hierarchy and formatting
* Designed for direct HR consumption

### Report Export

* One-click Word (.docx) report generation
* Includes:

  * Candidate ranking
  * Individual analysis
  * Global summary

---

## Architecture

```
User Interface (Streamlit)
          │
          ▼
     Core Layer
 (Analysis / Scoring / Ranking / Summary)
          │
          ▼
   Model Router Layer
 (Retry + Fallback Strategy)
      ┌───────────────┬───────────────┐
      ▼               ▼
   Qwen API       DeepSeek API
          │
          ▼
     Output Layer
 (UI Display + Word Export)
```

---

## Project Structure

```
ai-talent-assessment/
├── app/
│   └── main.py                 # Streamlit UI
│
├── core/
│   ├── analyzer.py            # Candidate evaluation logic
│   ├── scorer.py              # Score extraction
│   ├── ranker.py              # Ranking logic
│   └── summarizer.py          # Global summary generation
│
├── services/
│   ├── qwen_client.py         # Qwen API client
│   ├── deepseek_client.py     # DeepSeek API client
│   └── model_router.py        # Multi-model routing & fallback
│
├── utils/
│   ├── file_parser.py         # Word parsing
│   ├── text_cleaner.py        # Text preprocessing
│   └── docx_exporter.py       # Report generation
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Multi-Model Strategy

The system implements a **model abstraction layer** to decouple business logic from model providers.

### Routing Logic

1. Attempt Qwen (primary)
2. Retry on transient failures
3. Fallback to DeepSeek
4. Return graceful degradation message if all fail

### Benefits

* Improved system reliability
* Vendor independence
* Easy extensibility for future models

---

## Getting Started

### 1. Clone the Repository

```
git clone https://github.com/your-username/ai-talent-assessment.git
cd ai-talent-assessment
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file based on `.env.example`:

```
DASHSCOPE_API_KEY=your_qwen_api_key
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus

DEEPSEEK_API_KEY=your_deepseek_api_key
```

---

### 4. Run the Application

```
streamlit run app/main.py
```

---

## Usage Workflow

1. Enter job title
2. Paste job description (JD)
3. Define evaluation criteria
4. Upload multiple `.docx` resumes
5. Click “Start Analysis”
6. Review results in UI
7. Export Word report if needed

---

## Design Principles

### Separation of Concerns

* UI, business logic, model access, and utilities are fully decoupled

### Model Abstraction

* All LLM calls routed through a unified interface

### Prompt Engineering First

* Evaluation driven by structured prompts rather than hardcoded rules

### HR-Oriented Output

* No raw JSON
* Clear, readable, decision-ready content

---

## Future Enhancements

* Multi-role evaluation pipeline
* Scoring weight configuration system
* Candidate database & history tracking
* Visualization (radar charts / comparison dashboards)
* Async processing for large-scale batches
* API service layer for integration

---

## Resume-Ready Highlights

* Designed and implemented a multi-model AI evaluation system with automatic failover
* Built modular architecture with clear separation of concerns
* Integrated Qwen and DeepSeek via OpenAI-compatible interfaces
* Developed structured prompt-based evaluation pipeline for HR scenarios
* Delivered production-style UI and exportable reporting system

---

## License

This project is for educational and portfolio purposes.

---

## Acknowledgements

* Alibaba Cloud Qwen API
* DeepSeek API
* Streamlit framework
* python-docx library

---
