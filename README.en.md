# CHINESE OPEN SOURCE ARTIFICIAL INTELLIGENCE MODELS AS AN ASYMMETRIC RESPONSE TO U.S. EXPORT RESTRICTIONS

[[Russian version](README.md)]


**Interdisciplinary Term Paper (2026)**
**Student:** Zakhar E. Matveichuk
**Major:** 41.03.05 "International Relations", group 07331-DB
**Institution:** Irkutsk State University (ISU), Faculty of History
**Supervisor:** Prof. S. I. Kuznetsov

---

## Project Description

This repository contains the software code, data, and methodological materials for an interdisciplinary study focusing on the techno-economic and foreign policy analysis of Chinese open-weight LLMs in the context of U.S. sanctions pressure.

The research views the release of models (DeepSeek, Qwen, Kimi) not merely as import substitution, but as an **asymmetric tool for bypassing computing power shortages** through algorithmic optimization and global community crowdsourcing.

## Key Research Objectives

1.  **Sanctions Systematization:** Analysis of the escalation of U.S. export controls (2019–2025).
2.  **PRC Strategy Analysis:** Studying the responses of AI laboratories (DeepSeek, Alibaba, Moonshot) to hardware constraints.
3.  **Innovation Lag Calculation:** Identifying time delay patterns between sanctions and model releases (original ChronoDB).
4.  **Cognitive Analysis:** Comparative questioning of models (via API) on sensitive geopolitical triggers to identify political biases.
5.  **Foreign Policy Evaluation:** Analyzing the impact of Chinese Open Source on the Global South and U.S. digital hegemony.

---

## Repository Structure

The project is divided into three analytical modules:

*   **`data/module1/` (ChronoDB):** Database of sanctions packages and Chinese model releases (2019–2026). Includes innovation lag calculations.
*   **`data/module2/` (API Survey):** Protocols and results of questioning leading LLMs (DeepSeek-V3, Qwen3, Kimi K2, GPT-5, Gemini) across 12 geopolitical topics.
*   **`data/module3/` (Classification and Audit):** Results of automated classification of responses by tone, sanction framing, and refusal types.
*   **`src/module3/`:** Python-based software suite for data processing, OpenRouter API integration, and visualization generation (heatmaps, charts).
*   **`output/`:** Final graphical reports and visualized research results.
*   **`docs/BIBLIOGRAPHY.md`:** Comprehensive list of sources and literature.

---

## Technical Instructions

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Nek1yZakhar/Geopolitical_LLM_Analysis.git
    cd Geopolitical_LLM_Analysis
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Configure access keys (for running survey modules):
    *   Create a `.env` file.
    *   Add `OPENROUTER_API_KEY` or alternative keys.

### Running Analysis

To generate up-to-date visualizations (appendices for the term paper):
```bash
python src/module3/visualize.py
```

---

## Methodology (Module 3: Cognitive Dimension)

Comparative analysis is conducted along three axes:
1.  **Tone:** pro_CN / neutral / pro_US.
2.  **Sanction Frame:** threat / stimulus / necessity.
3.  **Refusal Type:** hard_refusal / soft_refusal / no_refusal.

The mitigation of "hallucinations" is achieved through statistical processing of multiple API requests and cross-verification using LLM classifiers.

---
*Irkutsk, 2026*
