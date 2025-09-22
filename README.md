# A Statistical and Entropy-Based Analysis of Pseudorandom Number Generators
### Author: Shaurya Deepak Khemka

Independent Researcher

Preparing for Journal Submission

## 🔬 Project Motivation

Pseudorandom number generators (PRNGs) are a cornerstone of modern computing, critical for everything from scientific simulations to cryptography. While many PRNGs exist, practitioners often face a gap in the literature: a lack of unified, side-by-side comparisons that evaluate diverse generators under the same rigorous framework. This research addresses that gap by providing a comprehensive, reproducible analysis of seven representative PRNGs, spanning historical, modern, and experimental designs.

The goal was not just to rank generators, but to deeply understand the trade-offs between their algorithmic structure, statistical quality, and entropy. This project moves beyond simple pass/fail tests to ask a more fundamental question: What does it truly mean for an algorithmic sequence to be "random"?

The complete research paper is available here: [**Khemka_PRNG_Research_Paper.pdf**](./Khemka_PRNG_Research_Paper.pdf)

## ✨ Key Features & Contributions
This project's contribution is not just in its results, but in its methodology and original work:

  Unified Testing Framework: A from-scratch Python framework was developed to apply a consistent battery of statistical tests (Shannon entropy, Chi-Square, Runs, Autocorrelation) across all generators, ensuring a fair and balanced comparison.

  Novel Generator Design: To explore algorithmic properties, two custom PRNGs were designed and implemented:

1. A Hybrid Generator combining a Linear Congruential Generator (LCG) with XOR mixing to test if simple nonlinear transformations can mitigate known linear artifacts.
2. A Quantum-Inspired Generator that simulates a hardware quantum random number generator by using SHA-256 to whiten a pool of system entropy, providing a high-security benchmark.
3. Composite Scoring Metric (RQS): A custom metric, the Randomness Quality Score (RQS), was developed to aggregate multi-dimensional test results into a single, interpretable score, providing a clearer view of overall performance and stability.
4. Fully Reproducible Codebase: The entire project is open-source and fully documented to adhere to scientific principles of transparency and reproducibility.

## 💡 The Key Insight: Stability vs. Complexity

One of the most counter-intuitive findings of this research was the performance of the classic, "flawed" Linear Congruential Generator (LCG). While modern generators like PCG64 are statistically superior in many ways, the LCG achieved the highest average Randomness Quality Score.

This does not mean the LCG is "better." It reveals a crucial insight: our RQS metric, which rewards statistical normality, favored the LCG's monotonous consistency. More complex generators like the Mersenne Twister were capable of higher peaks of quality but also exhibited more seed-dependent variability. The LCG "won" not on quality, but on unwavering stability.

This result serves as a powerful lesson in statistical interpretation: a generator's suitability is deeply tied to the application's specific need for either stability or robust complexity.

A boxplot from the study showing the distribution of Chi-Square p-values. The LCG's narrow interquartile range demonstrates its high stability compared to other generators.

## 🚀 How to Run the Analysis

The entire benchmark can be reproduced with a few simple commands.

1.Clone the Repository

	git clone [https://github.com/](https://github.com/)sdk-exe/PRNG-Statistical-Analysis.git

	cd PRNG-Statistical-Analysis

2.Install Dependencies (It is recommended to use a virtual environment)

	pip install -r requirements.txt

3.Run the Benchmark
The script will run the full analysis on all seven generators and print the final summary table.

	python main.py

 To see detailed per-seed results, open main.py and set the VERBOSE_MODE flag to True.

 ## 📁 Repository Structure

	.
	├── LICENSE
	├── README.md
	├── Khemka_PRNG_Research_Paper.pdf
	├── requirements.txt
	├── generators.py
	├── statistical_tests.py
	└── main.py

## 🎓 Publication Information

This work has been published in the *International Organization Of Scientific Research (IOSR) - Journal of Computer Engineering (IOSR-JCE)*

Khemka, S. D. (2025). A Statistical and Entropy-Based Analysis of Randomness in Pseudorandom Number Generators (PRNGs): Are They Truly Random? *IOSR Journal of Computer Engineering (IOSR-JCE)*

**The final published version is available here:**
[Published Paper](https://www.iosrjournals.org/iosr-jce/papers/Vol27-issue3/Ser-3/J2703037791.pdf)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
