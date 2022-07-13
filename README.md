# Credit-Card-Default-Prediction
This is a Machine Learning Project which Predicts probability of credit default based on credit card owner's characteristics and payment history.



### Software and account Requirement.
    
    
###    1. [Github Account](https://github.com/)
###    2. [Heroku Account](https://id.heroku.com/login)
###    3. [VS Code IDE](https://code.visualstudio.com/)
###    4. [GIT cli](https://git-scm.com/downloads)   
###    5. [GIT Documentation](https://git-scm.com/docs/gittutorial)
###    6. [GITHUB Action](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)



### Creating Conda Environment

```
      1. Configure conda environment in environment variables if its not already configured
```

```
      2. conda create -p <env_name> python=3.7 -y
```

```
      3. conda activate venv/

```


```
      4. create requirements.txt and start adding required dependencies of project in it and execute this file
          To Exceute this file use command as below

          pip install -r requirements.txt
```


```
      5. create app.py file
```


```
      6. to add files to git

            git add .
            git add filename
            git add filename1 filename2
```

      7. To check versions maintained by git

```
            git log
```

      8. To check the status of git

```
            git status
```


```
      6. to add files to git

            git add .
            git add filename
            git add filename1 filename2
```

      7. To check versions maintained by git

```
            git log
```

      8. To check the status of git

```
            git status
```

#### Note : To ignoew file/folders we could add those details inside git.ignore


```
      9. To create version/commit all changes by git


            git commit -m "message"
```


```
      10.   To send version / changes to git hub

            git push origin main

            origin is a variable which consists git url https://github.com/vaibhavyaramwar/Credit-Card-Default-Prediction.git

            to check the value of origin run below command

            git remote -v
```

```

            To check remote url 

                  git remote -v
```

```
            Revert git commit

                  git revert <commit to revert>

```

```
            Create Dockerfile and provide required details
            Also create .dockerignore file , this file is required so that docker will ignore the items those are exists in this file
```

```
            Login to Heroku and Navigate to account settings Copy the API Secrete key
```

```
            Login to github and Navigate to 

                Settings -> Security -> Secrets -> Actions

                Click on New Repository secret and add below secret

                HEROKU_EMAIL
                HEROKU_API_KEY
                HEROKU_APP_NAME
```

```
            create directory .github\workflows and add main.yaml file in it and provide all required workflow event , jobs , action and runner details
```

```
            Now push changes to github and check github actions and check pipline status 
            Github action will automatically triggers deployment of the Flask Application
```

#### Now Application is up and running in Heroku and Below is application URL : 

    https://creditcarddefpred.herokuapp.com/

