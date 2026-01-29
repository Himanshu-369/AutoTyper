# ⌨️ Humanized AutoTyper

A sophisticated automation tool designed to simulate realistic human typing patterns. Unlike standard autotypers that output text with robotic precision, this engine introduces intentional imperfections, cognitive pauses, and fatigue simulation to mimic a real person behind the keyboard.

![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![UI](https://img.shields.io/badge/UI-Modern%20Dark-121212?style=for-the-badge)

## ✨ Key Features

*   **🧠 Cognitive Typing Engine:** Simulates "thinking" time and word rethink pauses.
*   **🛠️ Human Imperfections:**
    *   **Auto-Corrected Typos:** Makes a mistake, realizes it, and backspaces to fix it.
    *   **Persistent Errors:** Occasional typos that are left uncorrected (human negligence).
    *   **Character Swaps:** Mimics common human errors like typing "teh" instead of "the".
    *   **Double Space Errors:** Randomly adds extra spaces between words.
*   **📈 Fatigue Simulation:** Typing speed naturally fluctuates and slows down over long sessions.
*   **👤 Behavioral Profiles:** 
    *   `Pro Typist`: Fast, accurate, minimal errors.
    *   `Lazy Student`: Slower, frequent "rethinking", more mistakes.
    *   `Tired Human`: High error rate, significant fatigue, inconsistent rhythm.
    *   `Just Type`: Pure speed, no imperfections.
*   **🎨 Modern Dark UI:** A sleek, Material-inspired interface built with Tkinter.
*   **🛡️ Safety First:** Includes an emergency fail-safe (slam mouse into any corner to stop).

## 🚀 Getting Started

### Prerequisites

*   Python 3.7+
*   Tkinter (usually included with Python)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Himanshu-369/AutoTyper.git
    cd AutoTyper
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python humanized_autotyper.py
    ```

## 📖 Usage

1.  **Input Text:** Type directly into the editor, paste from clipboard, or load a `.txt` file.
2.  **Select Profile:** Choose a preset from the dropdown or fine-tune individual settings.
3.  **Configure Logic:**
    *   **Base Speed:** Set your target Words Per Minute (WPM).
    *   **Start Delay:** Gives you time to switch to the target window (e.g., Word, Browser).
    *   **Fatigue:** Percentage speed drop as the text nears completion.
4.  **Start:** Click "Start Typing" and immediately click into your target text field.

## ⚙️ Advanced Settings

| Setting | Description |
| :--- | :--- |
| **Typos (Corrected)** | Probability of making a nearby-key mistake and fixing it. |
| **Swap Errors** | Probability of swapping common pairs (e.g., 'ei' vs 'ie'). |
| **Word Rethink** | Chance of pausing and re-typing a word entirely. |
| **Paragraph Pause** | Extended delay when encountering a newline character. |

## ⚠️ Safety Disclaimer

This tool is for educational and productivity purposes. Ensure you are not violating any terms of service of the platform you use this on. 

**Emergency Stop:** If the typing goes out of control, move your mouse cursor to **any corner of your screen** to trigger the PyAutoGUI fail-safe.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
