from Models import *
from Domain import *
from pony.orm import *
from PreprocessingDf_FINAL import *
import pandas as pd
import requests
import numpy as np
import psycopg2
from uuid import uuid4 as gid, UUID
from openpyxl.workbook import Workbook
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import itertools  
from pandas import read_csv
from collections import Counter
from imblearn.combine import SMOTEENN, SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, StratifiedKFold, RepeatedStratifiedKFold, GridSearchCV
from sklearn.metrics import auc, classification_report, roc_curve, roc_auc_score, confusion_matrix, average_precision_score, f1_score, plot_confusion_matrix, precision_recall_curve
from sklearn.dummy import DummyClassifier
from xgboost import XGBClassifier
import pickle
import os


# ucitaj obrađeni dataset
X,y = procesirani_df()

# napravi kopiju inputa i targeta te napravi pipeline koji će se koristiti za obradu podataka u svim foldovima u jednakom rasponu vrijednosti 
X2, y2 = X, y
# definiraj vrste atributa za daljnju obradu
numericke = ['index_vrucine1', 'temp_prosjek1', 'broj_soba', 'temp_max1', 'temp_min1', 'brzina_vjetra1', 'tlak_zraka1', 'oblaci_pokrice1', 'oborine_mogucnost1', 'p_temp_min_31', 'p_temp_min_73', 'p_temp_max_31',  'p_oborine_mogucnost31', 'p_brzina_vjetra_73']
kategoricke = ['nacin_rezervacije', 'status_rezervacije', 'vrsta_sobe', 'kanal', 'tip_garancije']
# Pipeline
NumPipeline_tot = Pipeline([('impute', SimpleImputer(strategy='mean', missing_values=np.nan)), ('scale', StandardScaler())])
KatPipeline_tot = Pipeline([('impute', SimpleImputer(strategy='most_frequent', missing_values=np.nan)), ('encode', TargetEncoder()), ('scale', StandardScaler())])
FinalPipeline_tot = ColumnTransformer([('prep_numericke', NumPipeline_tot, numericke), ('prep_kategoricke', KatPipeline_tot, kategoricke)], remainder='passthrough')
X_train_sve = FinalPipeline_tot.fit_transform(X2, y2)

# Spremi pipeline s vrijednostima
filename = 'Pipeline_Total.pkl'
direktorij = './Pipeline/'
putanja = os.path.join(direktorij, filename)
pickle.dump(FinalPipeline_tot, open(putanja, 'wb'))
print("Pipeline Total spremljen !!")

kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=7)
brojac = 1
for train, test in kfold.split(X,y):
    model = XGBClassifier(objective='binary:logistic')                      
    X_train, y_train = X.iloc[train], y.iloc[train]
    X_test, y_test = X.iloc[test], y.iloc[test]
    print("Ovo je broj ne-storna / storna u testu", np.bincount(y_test))

    # PROCESIRANJE PODATAKA
    # DEFINIRAJ LISTE ZA NUMERIČKE I ZA KATEGORIČKE VARIJABLE
    numericke = ['index_vrucine1', 'temp_prosjek1', 'broj_soba', 'temp_max1', 'temp_min1', 'brzina_vjetra1', 'tlak_zraka1', 'oblaci_pokrice1', 
                 'oborine_mogucnost1', 'p_temp_min_31', 'p_temp_min_73', 'p_temp_max_31',  'p_oborine_mogucnost31', 'p_brzina_vjetra_73']
    kategoricke = ['nacin_rezervacije', 'status_rezervacije', 'vrsta_sobe', 'kanal', 'tip_garancije']

    #UCITAJ PIPELINE SA VRIJEDNOSTIMA SVOJSTVENIM ZA CIJELI DATASET
    PrepPipeline = pickle.load(open('./Pipeline/Pipeline_Total.pkl', 'rb'))

    # OBRADI PODATKE 
    X_train_fit = PrepPipeline.transform(X_train)
    X_test_fit = PrepPipeline.transform(X_test)

    # Validacija
    eval_set = [(X_train_fit, y_train), (X_test_fit, y_test)]

    # PARAMETRI
    params = {
            'learning_rate':[0.01, 0.1, 0.2],
            'min_child_weight': [0.75, 1, 3],        
            'gamma': [0.001, 0.1, 0.8, 1],              
            'subsample': [0.5, 0.8],               
            'colsample_bytree':[0.8, 1],       
            'max_depth': [4,6,8],                 
            'n_estimators': [100, 200, 350],  
            'scale_pos_weight': [0.06, 1, 5, 15, 30]
    }

    # GRID 
    grid = GridSearchCV(estimator=model, param_grid=params, scoring='f1', verbose=3)
    grid.fit(X_train_fit, y_train, early_stopping_rounds=15, eval_set=eval_set, eval_metric="error", verbose=2)

    print(grid.best_params_)
    print(grid.best_score_)



