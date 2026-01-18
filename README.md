# ARCADE Analysis Code

This repository contains analysis code used in the research paper  
**ARCADE: Arabic Radio Corpus for Audio Dialect Evaluation**.

ARCADE is a city-scale corpus of Arabic radio speech designed for fine-grained dialect identification. The dataset includes 6,907 annotations covering 3,790 unique audio segments from radio streams across 58 cities in 19 Arab countries.

## Download dataset
To downlaod the dataset you need to use `datasets` and `torchcodec` libraries 
```bash
pip install datasets torchcodec
```
Then you can use 
```python
from datasets import load_dataset

ds = load_dataset("riotu-lab/ARCADE-full")
```

## Files

- **`comprehensive_analysis.py`**  
  Python script for combining ARCADE annotation CSV files, cleaning and deduplicating entries, adding geographic coordinates, and generating statistical analyses, figures, and summary reports used in the paper.

- **`plots_and_graphs.ipynb`**  
  Jupyter Notebook for exploratory data analysis and visualization of the ARCADE annotations.

## Data

The CSV files used in the analysis are provided separately and are required to reproduce the results.

## Citation

If you use this code or the ARCADE dataset, please cite:

```bibtex
@misc{nacar2026arcadecityscalecorpusfinegrained,
  title={ARCADE: A City-Scale Corpus for Fine-Grained Arabic Dialect Tagging},
  author={Omer Nacar and Serry Sibaee and Adel Ammar and Yasser Alhabashi and Nadia Samer Sibai and Yara Farouk Ahmed and Ahmed Saud Alqusaiyer and Sulieman Mahmoud AlMahmoud and Abdulrhman Mamdoh Mukhaniq and Lubaba Raed and Sulaiman Mohammed Alatwah and Waad Nasser Alqahtani and Yousif Abdulmajeed Alnasser and Mohamed Aziz Khadraoui and Wadii Boulila},
  year={2026},
  eprint={2601.02209},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2601.02209}
}
