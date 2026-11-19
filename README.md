# Predicting Delivery Time for Online Food Orders
## Authors: Steven Mou, Owen Lin, Rachel Lee, Shravan Chandra

In this project, we aim to predict food delivery time based on the characteristics of the food order itself and external factors such as delivery distance, order time, weather conditions, and traffic. We also aim to determine which of these factors are the strongest predictors of delivery time.

Set-up instructions:
1. Run `uv sync` in the terminal 
2. From the root of the repository, run the following in the terminal to download the Food Delivery Dataset from Kaggle into `data/raw/Food_Delivery_Dataset/`. It uses Kaggle's official `kagglehub` package (installed by `uv sync`); the dataset is public, so no Kaggle account or API token is needed. The same command works on Windows, macOS and Linux.
```
uv run python scripts/download_data.py
```
3. Clean the data. This removes duplicate rows and rows without an order date or delivery time, fixes formatting and data types, marks invalid coordinates as missing, and writes the result to `data/processed/food_delivery_clean.csv`.
```
uv run python scripts/clean_data.py
```


Food Delivery Dataset (Gaurav Malik, https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset) - Kaggle lists the license as "Other (specified in description)", but the description does not state any terms. We use it only for non-commercial, educational purposes and do not redistribute the raw data in this repository; run `scripts/download_data.py` (step 2 above) to download it from Kaggle.

*Limitations*
- The original source of the Food Delivery Dataset is not documented; it may be partly or fully synthetic.
- 91 rows have impossible values (courier age 15 or 50, rating 1 or 6 on a 1-5 scale). They are kept in the cleaned data so they can be examined, and should be removed before modeling.
- The data covers a short period (February to April 2022, with gaps from 19-28 February and on 22 March).

AI Use Statement
Code is written by a human team member with AI assistance during debugging. Ultimately, all decisions regarding what code to use were also made by a human team member.
