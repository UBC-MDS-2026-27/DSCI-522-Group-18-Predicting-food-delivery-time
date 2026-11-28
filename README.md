# Predicting Delivery Time for Online Food Orders

**Authors:** Steven Mou, Owen Lin, Rachel Lee, Shravan Chandra

## Summary

In this project, we examine whether food delivery time can be predicted from order details and external conditions. Using a tuned decision tree, we predicted delivery times on held-out orders with a Mean Absolute Error (MAE) of 3.37 minutes with an R² of 0.80 compared to a linear regression baseline with MAE 4.77 minutes with an R² of 0.60. Using permutation importance, we find that weather and traffic density were the most important inputs to our delivery time model, followed by distance and courier rating. This suggests delivery platforms could improve delivery time estimates by adjusting for weather and traffic, and a consumer at home should be prepared to wait a little longer for orders on days with cloudy or foggy weather and/or poor traffic conditions.

## How to run the analysis

### Clone the repository

Install [Git](https://git-scm.com/install). On the project’s GitHub page, select **Code**, choose **HTTPS**, and copy the repository URL. Open a command-line shell (PowerShell on Windows, Terminal on macOS, or your usual shell on Linux). From the folder where you want to keep the project, paste the URL after `git clone` and then enter the new project folder.

```sh
git clone https://github.com/UBC-MDS-2026-27/DSCI-522-Group-18-Predicting-food-delivery-time.git
cd DSCI-522-Group-18-Predicting-food-delivery-time
```

Run the remaining commands from that folder.

### Run with Docker Compose

Install and start [Docker Desktop](https://www.docker.com/products/docker-desktop/), which includes Docker Compose. The project image supplies Quarto, uv, and the Python environment from [`uv.lock`](uv.lock).

1. Check that `~/.ssh/id_ed25519.pub` is a file. If you need a key, run the following command and press Enter at each prompt to accept the defaults. Docker mounts this public key. If you run the container before creating the key, Docker can create a directory at that path. Remove the empty directory before generating the key.

   ```sh
   ssh-keygen -t ed25519
   ```

   Compose also mounts `~/.gitconfig`. If the file is missing, create an empty file at that path before starting the container. On Windows, `~` here means your user profile folder.

2. Download the project image from Docker Hub. Docker Compose reads the image tag from `docker-compose.yml`.

   ```sh
   docker compose pull
   ```

3. Run the analysis and render the report.

   ```sh
   docker compose run --rm analysis-env uv run quarto render
   ```

   Docker removes the one-off container when the command exits. The rendered HTML stays in your project folder.

Rendering writes `analysis/food-delivery-time-regression.html`. It requires internet access to retrieve the public Food Delivery Dataset using `kagglehub`. The source CSVs go to `data/raw/` and the cleaned training and test CSVs go to `data/processed/`. You can download the dataset without a Kaggle account or API token.

## Contributing and community guidelines

- [Contributing guidelines](CONTRIBUTING.md): how to report issues and suggest changes
- [Code of conduct](CODE_OF_CONDUCT.md): expected behaviour in this project

## Licenses

- Report and other non-code materials: CC BY-NC-ND 4.0
- Code: MIT
- [Food Delivery Dataset](https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset) (Gaurav Malik): Kaggle lists the license as "Other (specified in description)", but the description does not state any terms. We use it only for non-commercial, educational purposes. Rendering the report downloads it from Kaggle.

Full license terms can be viewed [here](LICENSE.md).

## Limitations

- The original source of the Food Delivery Dataset is not documented; it may be partly or fully synthetic.
- 91 rows have impossible values (courier age 15 or 50, rating 1 or 6 on a 1-5 scale). They are kept in the cleaned data so they can be examined, and are removed before modeling.
- The data covers a short period (February to April 2022, with gaps from 19-28 February and on 22 March).

## AI use statement

Code is written by a human team member with AI assistance during debugging. Ultimately, all decisions regarding what code to use were also made by a human team member. Claude was used to correct grammar during writing. No AI instruction files were used. Example prompts are as follows:

Grammar:
> Given the following sentence, are there any errors in grammar? Identify where but make no changes to the writing. "sentence"

Debugging:
> Why is this code giving a "[error message]" error? "code"

@shravnchandr: I used Claude Code (Opus 5.5) to assist with implementing and integrating the data downloading, cleaning, and splitting code into Quarto, cross-checking outputs against project requirements, and debugging errors.

Example prompts *(no instruction file like `CLAUDE.md` was used)*:

> Why does the report fail to render on Windows? Make no code changes.

> Cross-check the numbers and metrics in the Quarto report against the script outputs.

## Rendered report

[Read the published report on GitHub Pages](https://ubc-mds-2026-27.github.io/DSCI-522-Group-18-Predicting-food-delivery-time/).
