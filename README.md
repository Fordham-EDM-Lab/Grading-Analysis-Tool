# Grading Analysis Tool

This tool was created by **[Mario Marku](https://www.linkedin.com/in/mario-marku-384732247/)** with advisement from **[Dr. Gary Weiss](https://storm.cis.fordham.edu/~gweiss/)** and **[Dr. Daniel Leeds](https://storm.cis.fordham.edu/leeds/)** to simplify grading data analysis for educators without requiring programming or data analytics skills. Its intuitive interface streamlines the process of exploring student and course performance data.

The Tools offical Manual can be found **[here](https://docs.google.com/document/d/1gPt0qbNTj5_9tArIpUflvuOl0yOItwcN9cgwobPswDY/edit?usp=sharing)** alongisde an extensive Data Dictionary found **[here](https://docs.google.com/spreadsheets/d/1ACtguaegP0V97QovjSUgXp3LoO648-M-nUrQ_6GN7mQ/edit?usp=sharing)** detailing how this tool is used.

---
## Prerequisites

1.  **Install Python 3**
    * **Windows**: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
    * **macOS**: [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)
    * **Linux**: Use your distro’s package manager or download from [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **(Recommended) Create a Virtual Environment**
    * This prevents conflicts with system-wide packages:
        ```bash
        python3 -m venv venv
        # On Windows:
        venv\Scripts\activate
        # On macOS/Linux:
        source venv/bin/activate
        ```
    * If you **choose not** to use a virtual environment (not recommended), you can install system-wide.
        If pip refuses to install due to potential conflicts, add:
        ```bash
        pip install -e . --break-system-packages
        ```
        This **overrides** pip’s default protections, and may affect system packages.

---

## Installation

1.  **Clone or Download this Repository**
    ```bash
    git clone [https://github.com/Fordham-EDM-Lab/Grading-Analysis-Tool](https://github.com/Fordham-EDM-Lab/Grading-Analysis-Tool)
    ```
2.  **Install Dependencies (Inside the Virtual Environment, if created)**
    ```bash
    pip install -e .
    ```
    Or (if you want to bypass warnings about system packages):
    ```bash
    pip install -e . --break-system-packages
    ```

## After Installation

Simply run:

```bash
grade-analysis
```

Or

```bash
python3 -m src.gradeAnalysisGUI
```
