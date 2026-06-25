# CHINESE OPEN SOURCE ARTIFICIAL INTELLIGENCE MODELS AS AN ASYMMETRIC RESPONSE TO U.S. EXPORT RESTRICTIONS

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Grade](https://img.shields.io/badge/Grade-Excellent-brightgreen)
![Institution](https://img.shields.io/badge/ISU-IR_2026-orange)

[[Russian version](README.md)]

This research demonstrates that U.S. sanctions against the Chinese AI industry have paradoxically accelerated its development. We developed three original Python analytical modules for quantitative and qualitative assessment of Chinese AI release dynamics and real-world API querying of 5 state-of-the-art LLMs. The findings show China establishing sovereign software ecosystems to counter hardware constraints.

---

## 📊 Key Results

| Metric | Value | Context / Details |
| :--- | :--- | :--- |
| **Median Innovation Lag** | **4.0 months** | Across the entire dataset (33 releases, 2019–2026) |
| **Lag Reduction** | **7 mo. (2023) → 1–2 mo. (2025)** | Transition from reactive to proactive model |
| **DeepSeek-R1 Training Cost** | **<$6 million** | Compared to GPT-4 (~$78M) and Gemini (~$191M) |
| **Qwen's Share on Hugging Face** | **39%** | Base model for fine-tuning (H1 2025) |
| **LLM Survey Scope** | **5 models / 12 prompts** | 120 responses (DeepSeek V3, Qwen3, Kimi K2, GPT-5 mini, Gemini Flash) |

---

## 💡 Original Concepts

> [!NOTE]
> The study defines four theoretical concepts describing the dynamics of the Chinese response to external restrictions:

*   **Counter-chokepoints** — software nodes of global dependency that China creates symmetrically in response to U.S. hardware control.
*   **Coercive Opening** — hardware isolation forces the publication of open-weight models, unintentionally driving global dependency on Chinese codebase.
*   **Technology Echo Effect** — a systemic pattern where every sanctions strike is followed by a wave of model releases with a shrinking lag.
*   **Discursive Dependency** — Global South nations adopting Chinese LLMs receive not just technology, but also an embedded system of geopolitical interpretations.

---

## 🗂 Repository Structure

The project is divided into three analytical modules:

*   **`data/module1/` (ChronoDB):** Database of sanctions packages and Chinese model releases (2019–2026). Includes innovation lag calculations.
*   **`data/module2/` (API Survey):** Protocols and results of questioning leading LLMs (DeepSeek-V3, Qwen3, Kimi K2, GPT-5, Gemini) across 12 geopolitical topics.
*   **`data/module3/` (Classification and Audit):** Results of automated classification of responses by tone, sanction framing, and refusal types.
*   **`src/module1/`:** Scripts for collecting sanctions and models data, calculating innovation lags, and building the basic timeline ([timeline_builder.py](file:///c:/Users/Admin/Desktop/Geopolitical_LLM_Analysis/src/module1/timeline_builder.py), [visualize.py](file:///c:/Users/Admin/Desktop/Geopolitical_LLM_Analysis/src/module1/visualize.py)).
*   **`src/module2/`:** Program interface for automated API-polling of selected LLMs using OpenRouter API ([main.py](file:///c:/Users/Admin/Desktop/Geopolitical_LLM_Analysis/src/module2/main.py)).
*   **`src/module3/`:** Python-based software suite for data processing, auditing ([audit_data.py](file:///c:/Users/Admin/Desktop/Geopolitical_LLM_Analysis/src/module3/audit_data.py)), classification ([classifier.py](file:///c:/Users/Admin/Desktop/Geopolitical_LLM_Analysis/src/module3/classifier.py)), and visualization generation ([visualize.py](file:///c:/Users/Admin/Desktop/Geopolitical_LLM_Analysis/src/module3/visualize.py)).
*   **`output/`:** Final graphical reports and visualized research results.
*   **`docs/BIBLIOGRAPHY.md`:** Comprehensive list of sources and literature.

---

## 📈 Visualizations

### Sanctions and Releases Timeline
![Sanctions Timeline](output/module1_sanctions_timeline.png)

### Annual Distribution of Model Releases
![Releases Bar Chart](output/module1_releases_bar.png)

### Innovation Lags Dynamics by Wave
![Innovation Lags by Wave](output/module1_lags_by_wave.png)

### LLM Narrative Analysis and Cognitive Positioning
![Narrative Analysis](output/module3_narrative_analysis.png)

---

## ⚙️ Tech Stack

*   **Programming Language:** Python 3.11
*   **Data Analysis:** pandas
*   **Visualization:** Plotly, Matplotlib
*   **LLM Integration:** OpenRouter API, OpenAI SDK
*   **Database:** Supabase
*   **Platforms & Sources:** GitHub, Hugging Face, arXiv

---

## 🚀 Quick Start

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
    *   Create a `.env` file in the root directory.
    *   Add your API key:
        ```env
        OPENROUTER_API_KEY=your_openrouter_api_key_here
        ```

### Running Analysis

To generate up-to-date visualizations (appendices for the term paper):
```bash
python src/module3/visualize.py
```

---

## Methodology (Module 3: Cognitive Dimension)

Comparative analysis is conducted along three axes:
1.  **Tone:** `pro_CN` / `neutral` / `pro_US`.
2.  **Sanction Frame:** `threat` / `stimulus` / `necessity`.
3.  **Refusal Type:** `hard_refusal` / `soft_refusal` / `no_refusal`.

The mitigation of "hallucinations" is achieved through statistical processing of multiple API requests and cross-verification using LLM classifiers.

---

**Interdisciplinary Term Paper (2026)**  
*Topic:* "Chinese Open Source Artificial Intelligence Models as an Asymmetric Response to U.S. Export Restrictions" (Grade: **Excellent**)  
*Student:* Zakhar E. Matveichuk (Group 07331-DB, Major: 41.03.05 "International Relations")  
*Institution:* Irkutsk State University (ISU), Faculty of History  
*Supervisor:* Prof. S. I. Kuznetsov  
*Irkutsk, 2026*
