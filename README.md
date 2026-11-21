# Predicting Delivery Time for Online Food Orders

**Authors:** Steven Mou, Owen Lin, Rachel Lee, Shravan Chandra

## Summary

In this project, we examine whether food delivery time can be predicted from order details and external conditions. Using a tuned decision tree, we predicted delivery times on held-out orders with a Mean Absolute Error (MAE) of 3.37 minutes with an R² of 0.80 compared to a linear regression baseline with MAE 4.77 minutes with an R² of 0.60. Using permutation importance, we find that weather and traffic density were the most important inputs to our delivery time model, followed by distance and courier rating. This suggests delivery platforms could improve delivery time estimates by adjusting for weather and traffic, and a consumer at home should be prepared to wait a little longer for orders on days with cloudy or foggy weather and/or poor traffic conditions.

## How to run the analysis

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

## Dependencies

- [uv](https://docs.astral.sh/uv/getting-started/installation/), which installs the Python packages listed in `pyproject.toml`
- [Quarto](https://quarto.org/docs/get-started/), to render the report

## Contributing and community guidelines

- [Contributing guidelines](CONTRIBUTING.md): how to report issues and suggest changes
- [Code of conduct](CODE_OF_CONDUCT.md): expected behaviour in this project

## Licenses

- Report and other non-code materials: CC BY-NC-ND 4.0
- Code: MIT
- [Food Delivery Dataset](https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset) (Gaurav Malik): Kaggle lists the license as "Other (specified in description)", but the description does not state any terms. We use it only for non-commercial, educational purposes and do not redistribute the raw data in this repository; rendering the report (step 3 above) downloads it from Kaggle.

Full license terms can be viewed [here](LICENSE.md).

## Limitations

- The original source of the Food Delivery Dataset is not documented; it may be partly or fully synthetic.
- 91 rows have impossible values (courier age 15 or 50, rating 1 or 6 on a 1-5 scale). They are kept in the cleaned data so they can be examined, and are removed before modeling.
- The data covers a short period (February to April 2022, with gaps from 19-28 February and on 22 March).

## AI use statement

Code is written by a human team member with AI assistance during debugging. Ultimately, all decisions regarding what code to use were also made by a human team member.

## Rendered report

View the full report [here](https://ubc-mds-2026-27.github.io/DSCI-522-Group-18-Predicting-food-delivery-time/analysis/food-delivery-time-regression.html).
