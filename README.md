# Predicting Delivery Time for Online Food Orders
## Authors: Steven Mou, Owen Lin, Rachel Lee, Shravan Chandra

In this project, we aim to predict food delivery time based on the characteristics of the food order itself and external factors such as delivery distance, order time, weather conditions, and traffic. We also aim to determine which of these factors are the strongest predictors of delivery time.

Dependencies:
- [uv](https://docs.astral.sh/uv/getting-started/installation/), which installs the Python packages listed in `pyproject.toml`
- [Quarto](https://quarto.org/docs/get-started/), to render the report

How to run the analysis:
1. Clone this repository and open a terminal in its root folder.
2. Install the Python environment:
```
uv sync
```
3. Render the report:
```
uv run quarto render analysis/food-delivery-time-regression.qmd
```
This runs the whole analysis and writes `analysis/food-delivery-time-regression.html`. The report downloads the Food Delivery Dataset from Kaggle into `data/raw/Food_Delivery_Dataset/` with Kaggle's official `kagglehub` package; the dataset is public, so no Kaggle account or API token is needed. It then writes the cleaned data and the training and test sets to `data/processed/`. The same commands work on Windows, macOS and Linux.


Food Delivery Dataset (Gaurav Malik, https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset) - Kaggle lists the license as "Other (specified in description)", but the description does not state any terms. We use it only for non-commercial, educational purposes and do not redistribute the raw data in this repository; rendering the report (step 3 above) downloads it from Kaggle.

*Limitations*
- The original source of the Food Delivery Dataset is not documented; it may be partly or fully synthetic.
- 91 rows have impossible values (courier age 15 or 50, rating 1 or 6 on a 1-5 scale). They are kept in the cleaned data so they can be examined, and should be removed before modeling.
- The data covers a short period (February to April 2022, with gaps from 19-28 February and on 22 March).

AI Use Statement
Code is written by a human team member with AI assistance during debugging. Ultimately, all decisions regarding what code to use were also made by a human team member.
