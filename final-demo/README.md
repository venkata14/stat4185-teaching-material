# Final Project Demo

*The live demo for this repository is here: [https://stat4185-demo.herokuapp.com/](https://stat4185-demo.herokuapp.com/)*

This repository hosts a demo for the final class project. The final class project should be something resume worthy and created with the tools you learned in class and hosted with Streamlit & Heroku. We created a demo with the MNIST dataset as it is simple to follow along with the material taught in class. Ideally, all of you should attempt to create projects for your resumes that are more applicable/practical. 

The `train_tf_model.ipynb` file contains the code to train and save the model. The `models/` folder contains the saved folders. The `data/` folder contains the processed data. And `app.py` contains the streamlit app.

*You can clone the repo and deploy it yourself with the instructions below.*

### Deploying your Streamlit App of Heroku

1. Create the `Procfile` with this code snippet. 
    - This is an app the specifies the commands to run when the app is initially loaded on the web. 

```bash
web: sh setup.sh && streamlit run app.py
```

2. Create the `setup.sh` with this code snippet. 
    - This allows you to set up the basic connections settings and configure some metadata

```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"email@uconn.edu\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

3. Create a `requirements.txt` with all the libraries needed for the project.
    - Note, if you use tensorflow for the project **you must include tensorflow-cpu, not tensorflow** in `requirements.txt`
        - tensorflow itself is too big to be run by Heroku

4. Create a `runtime.txt` with the specified python version to runn you app.

5. Initialize git with `git init`.

6. Download the Heroku CLI from [https://devcenter.heroku.com/articles/heroku-cli#download-and-install](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

7. Log into the Heroku CLI with `heroku login`.

8. Deploy the project with this code snippet. 

```bash
git add .
git commit -m “My first commit”
heroku create
git remote -v
git push heroku master
```

- The last command deploys the project.

9. Rename your app and test it out!

```bash
heroku apps:rename <project-name>
```

You can now access your app from project-name.herokuapp.com!