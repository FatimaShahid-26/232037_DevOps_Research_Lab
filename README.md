# Pakistan Forest Type Prediction System

## About the Project

This project is a machine-learning-based web application developed to predict forest-origin categories in Pakistan using geographical and environmental information.

The project combines machine learning with full-stack web development and DevOps practices. Its purpose is to demonstrate how a trained classification model can be integrated into a web application and deployed through an automated CI/CD workflow.

## Project Objectives

The main objectives of this project are:

- Train and compare different machine-learning classification algorithms.
- Develop a Flask API to serve predictions from a trained model.
- Build an Angular interface where users can enter environmental information.
- Connect the frontend and backend to create a working application.
- Use GitHub Actions to automate testing and deployment.

## Dataset

The dataset was prepared using Google Earth Engine with forest classifications from the JRC Global Forest Types 2020 dataset.

It contains **5,806 observations** collected from different sampled locations across Pakistan.

The three classification categories are:

| Class | Forest Category |
|---|---|
| 1 | Naturally Regenerating Forest |
| 10 | Primary Forest |
| 20 | Planted/Plantation Forest |

Each observation contains environmental information used to predict the forest category.

## Machine Learning Approach

Four classification algorithms were explored:

1. Decision Tree
2. Random Forest
3. K-Nearest Neighbors (KNN)
4. XGBoost

Random Forest was selected for the application based on development-validation results.

The final model accepts five environmental inputs: elevation, slope, aspect, average annual temperature, and annual precipitation.

## Application Development

**Backend — Flask**

The Flask backend loads the trained machine-learning model and provides an API that accepts environmental measurements and returns a predicted forest category.

**Frontend — Angular**

The Angular interface allows users to enter environmental values and view the predicted forest category, a short description, and the model's prediction scores.

## DevOps and Deployment

Git and GitHub were used for version control and project management.

GitHub Actions was configured to perform automated checks and build the Angular application. The frontend is deployed using GitHub Pages.

The publicly deployed website is a static demonstration. Actual predictions require the Flask backend to run locally.

## Technologies Used

Python, Pandas, Scikit-learn, XGBoost, Flask, Angular, TypeScript, HTML, CSS, Git, GitHub Actions, and GitHub Pages.

## Running the Project Locally

Install the Python requirements:

```powershell
python -m pip install -r backend\requirements.txt
```

If necessary, train the model and generate the test payload:

```powershell
python backend\train_models.py
python backend\make_payload.py
```

Start the backend:

```powershell
python backend\app.py
```

In a separate terminal, start Angular:

```powershell
cd frontend
npm install
ng serve --open --proxy-config proxy.conf.json
```

Open `http://localhost:4200` to use the application.

## Project Links

**GitHub Repository:**  
https://github.com/FatimaShahid-26/232037_DevOps_Research_Lab

**Deployed Frontend:**  
https://fatimashahid-26.github.io/232037_DevOps_Research_Lab/

## Limitations and Future Improvements

The current dataset uses forest-origin categories derived from an existing geographical classification map. The model has not been independently validated for operational forest management.

Future improvements could include additional environmental features, independently validated Pakistani ecological forest-type labels, improved geographical evaluation, and deployment of the Flask backend to support live predictions online.

---

*This application was developed as an academic project to gain practical experience with machine learning, full-stack application development, and CI/CD workflows.*