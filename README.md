# Predicting Delivery Time for Online Food Orders
Authors: Steven Mou, Owen Lin, Rachel Lee, Shravan Chandra

In this project, we aim to predict food delivery time based on the characteristics of the food order itself and external factors such as delivery distance, order time, weather conditions, and traffic. We also aim to determine which of these factors are the strongest predictors of delivery time.

Set-up instructions:
1. Run `uv sync` in the terminal 
2. Run the following in the terminal to download open license data from Kaggle.
```
curl -L -o “$HOME/Downloads/global-food-delivery-restaurant-market-2026.zip” \
  “https://www.kaggle.com/api/v1/datasets/download/luthfimuthathohirin/global-food-delivery-restaurant-market-2026”

unzip -o “$HOME/Downloads/global-food-delivery-restaurant-market-2026.zip” \
  -d “$HOME/Downloads/global-food-delivery-restaurant-market-2026"
```
Licenses
Global Food Delivery Restaurant Market 2026 Dataset - CC0 1.0 Universal

AI Use Statement
Code is written by a human team member with AI assistance during debugging. Ultimately, all decisions regarding what code to use were also made by a human team member.
