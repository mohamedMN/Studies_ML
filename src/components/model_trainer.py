from catboost import CatBoostRegressor
from pkg_resources import evaluate_marker
from sklearn import preprocessing
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

import sys
import os
from src.exception import CustomException
from src.logger import logging
from src.utilis import save_object
from dataclasses import dataclass
from src.utilis import evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info('Split training and test input data')
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
                "Linear Regression": LinearRegression(),
                "Random Forest Regressor": RandomForestRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
                "Gradient Boosting Regressor": GradientBoostingRegressor(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree Regressor": DecisionTreeRegressor(),
                "XGBoost Regressor": XGBRegressor(),
                "CatBoost Regressor": CatBoostRegressor(verbose=0) 
            }

            model_report: dict = evaluate_models(
                X_train=X_train, y_train=y_train,X_test=X_test , y_test=y_test , models=models)
            
            best_model_score=max(sorted(model_report.values()))

            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model=models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found")
            logging.info("best model found on both training and testing datasets")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )


            predicted=best_model.predict(X_test)

            r2_square=r2_score(y_test,predicted)

            return r2_square
        


        except Exception as e:
            CustomException(e,sys)

