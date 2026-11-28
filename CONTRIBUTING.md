# Contributing

Contributions are greatly appreciated! Please read the instructions below if you would like to report a problem or propose a change.

### Reporting a bug

If something is broken or does not work as expected, please first check the existing issues to see whether the problem has already been reported. If not, open a new issue with a short, descriptive title. List the steps that reproduce the problem and include your operating system and the versions of the tools you used. Then describe the problem in as much detail as possible, so that our team can resolve it quickly.

### Suggesting a change

If you would like to propose a new idea or change, please open an issue before you start coding. As with bug reports, please describe what you would like to change and why. The team appreciates new ideas and may contact you to discuss them before you start working.

### Submitting changes

Please refer to the [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) workflow if you would like to submit changes.

1. Open an issue describing the change
2. Start from an up-to-date `main` in this repository. Do not commit directly to `main`.
3. Create a new branch with a short, descriptive name
4. Make your changes and commit them with clear, meaningful commit messages
5. Push your branch to GitHub and open a pull request into the `main` branch. In the description, explain what you changed and why.

Your pull request will be reviewed by the project team. It must be approved by all team members before it can be merged.

### Setting up the project

We develop in the same Docker container that users run the analysis in,
so everyone uses the same software and package versions.
First follow the [Run with Docker Compose section of the README](README.md#run-with-docker-compose)
(install Docker, clone the repository, make an ssh key, and download the image).
Run all the commands below from the root of this repository.

### Working in the container

We edit and run the code inside the container, by connecting Positron to it over ssh.
Your project folder is shared with the container at `/workspace`,
so a file you change there changes on your computer too.

<details>
<summary><strong>Once, before your first connection</strong></summary>

1. Install [Positron](https://positron.posit.co/download.html) on your computer.
   Its **Remote SSH** feature, which connects to the container, comes built in,
   so you don't need to install an extension.
2. Make sure you followed the [Run with Docker Compose section of the README](README.md#run-with-docker-compose):
   you have an ssh key at `~/.ssh/id_ed25519.pub` and you ran `docker compose pull`.
3. Check that Git knows who you are on your computer:

   ``` bash
   git config --global user.email
   ```

   It should print the email of your GitHub account.
   If it prints nothing, set your name and email:

   ``` bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

   `docker-compose.yml` shares your `~/.gitconfig` with the container,
   so the commits you make there count as yours.

</details>

<details>
<summary><strong>Each time you work on the project</strong></summary>

1. In a terminal, in the root of this repository, start the container in the background:

   ``` bash
   docker compose up -d
   ```

   `docker compose ps` should list `analysis-env` as running.
2. In Positron, open the Command Palette
   (`Cmd+Shift+P` on Mac, `Ctrl+Shift+P` on Windows).
3. Type and run **Remote SSH: Show Remote Menu**, then pick **Connect to Host**.
4. Type `root@localhost:2222` and press Enter. A new Positron window opens.
   * If it asks for the platform of the remote host, pick **Linux**.
   * If it asks whether you trust the host (a "fingerprint"), click **Continue**.
   * The first time, Positron installs its server inside the container. This takes a few minutes.
5. **Open the project folder.**
   The bottom left corner now shows `SSH: localhost:2222`,
   but the Explorer says **No folder opened** and the terminal starts in `/root`,
   which has no project files. That is normal.
   * Click **Open Folder** in the Explorer.
   * Delete what is in the path box at the top of the window, type `/workspace`, and click "ok" (you may need to click "ok" a few times before this works).
   * The window reloads, and the Explorer shows **WORKSPACE [SSH: LOCALHOST:2222]** with the project files.
6. **Pick the Python interpreter** (check this every time).
   * Click the interpreter button at the top right of the window.
     The **Running Interpreter Sessions** menu only lists sessions that are already running
     (such as `/usr/bin/python3`, the container's system Python: not this one).
   * Click **New Console Session...** and pick
     **Python 3.x (uv: dsci-522-group-18-predicting-food-delivery-time)**,
     with the path `/opt/venv/bin/python`. This is the environment built from `uv.lock`.
   * If it isn't in the list, run **Python: Select Interpreter** from the Command Palette,
     choose **Enter interpreter path...** and type `/opt/venv/bin/python`.
   * Don't pick `/workspace/.venv`: that is an environment from your own computer,
     and it doesn't run in the container.
   * To check, run `import sys; print(sys.executable)` in the Console.
     It should print `/opt/venv/bin/python`.
7. Work as usual. The Terminal, the Console and the **Render** button all run inside the container.
8. When you are done, close the Positron window,
   then stop and remove the container in a terminal on your computer:

   ``` bash
   docker compose down
   ```

</details>

<details>
<summary><strong>If it doesn't connect</strong></summary>

* **`~/.ssh/id_ed25519.pub` is a folder:** Docker made it because the key didn't exist yet.
  Run `docker compose down`, delete that folder, make the key
  (see the [README](README.md#run-with-docker-compose)), and start again.
* **`~/.gitconfig` is a folder, or Git in the container doesn't know your name:**
  the same thing happened with your Git settings.
  Run `docker compose down`, delete that folder, set your name and email (see above), and start again.
* **It asks for a password:** the container can't see your key.
  Check that your key is named `id_ed25519.pub`, or change the key path in `docker-compose.yml`.
* **"Remote host identification has changed":** you are using a new image.
  Run `ssh-keygen -R "[localhost]:2222"`, then connect again.
* **GitHub asks you to sign in when you push from the container:**
  sign in once in the browser window Positron opens. Positron remembers it.
* **Linux laptops:** ssh refuses the key because the file belongs to you, not `root`.
  Remove the `#` from the `StrictModes no` line in the `Dockerfile` and push,
  so the workflow publishes a fixed image.
* **Windows laptops:** ssh refuses the key because Docker Desktop shares the file
  so that anyone can write to it. The same `StrictModes no` line in the `Dockerfile` fixes this.
* **Port 2222 is already in use:** change the first `2222` in `docker-compose.yml`
  to another number (e.g. `2223`), and connect to that port instead.

More detail: [Working in a container over ssh with Positron](https://ubc-dsci.github.io/reproducible-and-trustworthy-workflows-for-data-science/lectures/containers-ssh-positron.html).

</details>

To re-run the analysis and render the report without opening the container:

``` bash
docker compose run --rm analysis-env uv run quarto render
```

### Adding or updating a package

On a new branch, add the package with `uv add <package>==<version>`
(this pins the version in `pyproject.toml` and updates `uv.lock`),
then commit the changed `pyproject.toml` and `uv.lock` together and push them.
GitHub Actions then builds and publishes a new image on Docker Hub,
and commits the new `sha-` tag to the `image:` line of `docker-compose.yml`
on your branch.
When the workflow finishes,
get that commit and download the new image:

``` bash
git pull
docker compose pull
```

Then merge the branch into `main` in a pull request.

### Publishing the report

The report on GitHub Pages is a copy of the rendered report in `docs/index.html`.
Each time you re-render the report, copy it there again, commit and push:

``` bash
cp analysis/food-delivery-time-regression.html docs/index.html
```

### Use of generative AI

Contributors may use generative AI tools (e.g., ChatGPT, Copilot, or Claude) when contributing to this project, as long as they follow the rules below.

Allowed uses:
- Brainstorming ideas, explaining errors or learning new methods
- Checking grammar and clarity in writing
- Writing and debugging code that you review and understand

Not allowed:
- Using generative AI tools to open issues, open or review pull requests, or merge pull requests. These must be done by a human contributor.
- Submitting AI-generated code that you have not reviewed, tested or understood
- Adding AI-generated references to the project without checking that they exist and citing them properly

If generative AI wrote a considerable part of your contribution, please declare this in your pull request description (e.g. the name of the AI tool and a brief explanation of how you used it).

You are fully responsible for the code or writing you submit. Reviewers may ask you to explain any part of your contribution.

### Questions

If you have a question that is not covered in the sections above, please open an issue and we will respond as soon as we can.

### Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

### Attribution

Parts of this document were adapted from the AI fairness research paper, available at https://github.com/skysheng7/AI_bias_in_farming/blob/main/CONTRIBUTING.md

The sections on setting up the project, working in the container, adding or updating a package and publishing the report were adapted from the [Breast Cancer Predictor project's contributing guidelines](https://github.com/UBC-MDS/DSCI_522_project-template-breast-cancer-predictor/blob/1.0.0/CONTRIBUTING.md).