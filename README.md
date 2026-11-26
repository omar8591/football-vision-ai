# Football Vision AI

A Streamlit app for football image and video detection using YOLO.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

The app loads model weights from `best.pt`. The optional example comparison
videos are read from `examples\before.mp4` and `examples\after.mp4`.

## Deploy with Streamlit Community Cloud

1. Push this project to a GitHub repository, including `best.pt` and the
   `examples` folder.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with
   GitHub.
3. Choose **Create app**, then select the repository, branch, and `app.py`.
4. Deploy. Streamlit Cloud installs the packages from `requirements.txt` and
   redeploys when new commits are pushed to the selected branch.

For `omar8591/football-vision-ai`, the GitHub remote is:

```text
https://github.com/omar8591/football-vision-ai.git
```

## Push from this folder

Create the private repository on GitHub first, then run these commands from
the project folder:

```powershell
git init
git branch -M main
git add app.py requirements.txt README.md .gitignore best.pt examples
git commit -m "Initial Football Vision AI app"
git remote add origin https://github.com/omar8591/football-vision-ai.git
git push -u origin main
```

Git will use your configured identity and GitHub sign-in for the commit and
push. The generated `.video_cache`, Python bytecode, editor settings, and
Streamlit secrets are excluded by `.gitignore`.
