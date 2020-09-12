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
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import auc, classification_report, roc_curve, roc_auc_score, confusion_matrix, average_precision_score, f1_score, plot_confusion_matrix, precision_recall_curve
from sklearn.dummy import DummyClassifier
from xgboost import XGBClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.calibration import calibration_curve
import pickle
import os

# ------------- PLOTANJE KRIVULJA
# ROC-AUC
def plot_roc_curve(y_test, naive_vjerojatnosti, model_vjerojatnosti):
	# plotaj dummy
	fpr1, tpr1, _1 = roc_curve(y_test, naive_vjerojatnosti)
	plt.plot(fpr1, tpr1, linestyle='--', label='Dummy')
	# plotaj model
	fpr2, tpr2, _2 = roc_curve(y_test, model_vjerojatnosti)
	plt.plot(fpr2, tpr2, marker='.', label='XGBoost')
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.legend()
	plt.show()

# # PRECISION - RECALL 
def plot_pr_curve(y_test, model_vjerojatnosti, ix):
    # no_skill = len(y_test[y_test==1]) / len(y_test)
    no_skill = sum(y_test) / len(model_vjerojatnosti)
    plt.plot([0, 1], [no_skill, no_skill], linestyle='--', label='Dummy', zorder=3)
    precision, recall, _ = precision_recall_curve(y_test, model_vjerojatnosti, pos_label=1)
    plt.plot(recall, precision, marker='.', label='XGBoost', c='green', zorder=2)
    # plt.scatter(recall[ix], precision[ix], marker'o', c='black', zorder=1, label='Najbolji T')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend()
    plt.show()

# PRESCJECANJE PRECISION I RECALL KRIVULJA 

def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    plt.figure(figsize=(8, 8))
    plt.title("Precision and Recall rezultati kao funkcija praga odluke (Threshold-a)")
    plt.plot(threshold, precision[:-1], "b--", label="Precision")
    plt.plot(threshold, recall[:-1], "g-", label="Recall")
    plt.ylabel("Rezultat")
    plt.xlabel("Prag odluke")
    plt.legend(loc='best')
    plt.show()

# Pripoji svakoj predikciji klase njezin threshold
def to_labels(klase, threshold):
	return (klase >= threshold).astype('int')

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

# K FOLD------------------------------------------------------------------------------------------------------------
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=7)
brojac = 1
for train, test in kfold.split(X,y):
    # model = XGBClassifier(objective='binary:logistic', learning_rate=0.05, max_depth=12, 
    #                       n_estimators=1000, subsample=1, colsample_bytree=0.9, gamma=0.5, scale_pos_weight=2)
    model = XGBClassifier(objective='binary:logistic', learning_rate=0.05, max_depth=6, 
                          n_estimators=1000, subsample=1, colsample_bytree=0.9, gamma=0.5, scale_pos_weight=2)                      
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

    # SET ZA EVALUACIJU
    eval_metrics = ["auc", "aucpr", "map", "error", "logloss"]
    eval_set = [(X_train_fit, y_train), (X_test_fit, y_test)]

    # TRENIRAJ MODEL
    model.fit(X_train_fit, y_train, early_stopping_rounds=15, eval_metric=eval_metrics, eval_set=eval_set, verbose=2)

    # plot metrike treninga 
    rezultati = model.evals_result()
    epohe = len(rezultati['validation_0']['error'])
    x_axis = range(0, epohe)
    # Mean avg
    fig, ax = plt.subplots()
    ax.plot(x_axis, rezultati['validation_0']['map'], label='Train')
    ax.plot(x_axis, rezultati['validation_1']['map'], label='Test')
    ax.legend()
    plt.xlabel('Epohe')
    plt.ylabel('Mean average error')
    plt.title('XGBoost - Mean average error')
    plt.show()
    # Log loss
    fig, ax = plt.subplots()
    ax.plot(x_axis, rezultati['validation_0']['logloss'], label='Train')
    ax.plot(x_axis, rezultati['validation_1']['logloss'], label='Test')
    ax.legend()
    plt.xlabel('Epohe')
    plt.ylabel('Log loss')
    plt.title('XGBoost Log loss')
    plt.show()
    # pogreška klasifikacije
    fig, ax = plt.subplots()
    ax.plot(x_axis, rezultati['validation_0']['error'], label='Train')
    ax.plot(x_axis, rezultati['validation_1']['error'], label='Test')
    ax.legend()
    plt.xlabel('Epohe')
    plt.ylabel('Class error')
    plt.title('XGBoost Class error')
    plt.show()

    # Prikaz input kolona prema važnosti
    importance_data = sorted(list(zip(X.columns, model.feature_importances_)), key=lambda tpl:tpl[1],reverse=True)
    xs = range(len(importance_data))
    labels = [x for (x,_) in importance_data]
    ys = [y for (_,y) in importance_data]

    plt.figure()
    plt.bar(xs,ys,width=0.5)
    plt.xticks(xs,labels, rotation=90)
    plt.show()

    # Classification report
    y_pred = model.predict(X_test_fit)
    report = classification_report(y_test, y_pred)
    print(report)

    # DUMMY MODEL ZA KOMPARACIJU KRIVULJA
    model_dummy = DummyClassifier(strategy='stratified')
    model_dummy.fit(X_train_fit, y_train)
    yhat = model_dummy.predict_proba(X_test_fit)
    naive_vjerojatnosti = yhat[:, 1]
    roc_auc = roc_auc_score(y_test, naive_vjerojatnosti)

    # CONFUSION MATRICA
    class_names = ['nije_storno', 'storno']
    titles_options = [("Confusion matrica, apsolutne vrijednosti", None),
                  ("Normalizirana confusion matrica u %", 'true')]
    for title, normalize in titles_options:
        disp = plot_confusion_matrix(model, X_test_fit, y_test,
                                    display_labels=class_names,
                                    cmap=plt.cm.Blues,
                                    normalize=normalize)
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)
        plt.show()

    # ROC I AUC
    y_hat = model.predict_proba(X_test_fit)
    model_vjerojatnosti = y_hat[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, model_vjerojatnosti)
    # IZRAČUNAJ NAJBOLJI THRESHOLD ZA ROC KRIVULJU- prema Youden's J 
    J = tpr - fpr
    ix = np.argmax(J)
    najbolji_thresh = thresholds[ix]
    print('Najoptimalnija vrijednost za ROC =%f' % (najbolji_thresh))
    roc_auc = roc_auc_score(y_test, model.predict(X_test_fit))
    print('ROC AUC SCORE: %.3f' % roc_auc)
    # PLOTAJ ROC KRIVULJU
    plot_roc_curve(y_test, naive_vjerojatnosti, model_vjerojatnosti)

    # PR CURVE 
    # DUMMY
    precision, recall, threshold = precision_recall_curve(y_test, naive_vjerojatnosti)
    auc_score = auc(recall, precision)
    print('DUMMY PR AUC: %.3f' % auc_score)
    # XGBOOST
    precision, recall, threshold = precision_recall_curve(y_test, model_vjerojatnosti, pos_label=1)
    auc_score = auc(recall, precision)
    auprc = average_precision_score(y_test, model_vjerojatnosti)
    print('XGBoost PR AUC: %.3f' % auc_score)
    print('XGBoost AVG SCORE: %.3f' % auprc)
    fscore = (2 * precision * recall) / (precision + recall)
    ix = np.argmax(fscore)
    print('Najoptimalniji Threshold za PR=%f, F-Score=%.3f' % (threshold[ix], fscore[ix]))
    # plotaj precision-recall krivulju
    plot_pr_curve(y_test, model_vjerojatnosti, ix)

    # IZRAČUNAJ OPTIMALNI THRESHOLD KOD PREDIKCIJE POZITIVNE KLASE (1)
    # PROVJERI SVE PRAGOVE OD 0 DO 1, POVEĆAJ SVAKU ITERACIJU ZA 0.001
    thresholds = np.arange(0, 1, 0.001)
    # ispiši F score za svaki threshold
    rezultati = [f1_score(y_test, to_labels(model_vjerojatnosti, t)) for t in thresholds]
    # ISPIŠI NAJBOLJI THRESHOLD
    ix = np.argmax(rezultati)
    print('Threshold=%.3f, F-Score=%.5f' % (thresholds[ix], rezultati[ix]))

    # crtaj krivulju presjecanja
    plot_precision_recall_vs_threshold(precision, recall, threshold)

    # crtaj calibration krivulju
    fop, mpv = calibration_curve(y_test, model_vjerojatnosti)
    # crtaj savršeno kalibrirani model
    plt.figure()
    plt.plot([0, 1], [0, 1], linestyle='--')
    # crtaj trenutni model
    plt.plot(mpv, fop, 'm', marker='.')
    plt.title('Nekalibrirano')
    plt.show()

    # Spremi model nakon treninga
    filename = 'Model_CV_' + str(brojac) +'.pkl'
    direktorij = './Modeli/'
    putanja = os.path.join(direktorij, filename)
    pickle.dump(model, open(putanja, 'wb'))
    print("Model spremljen !!")
    
    # uvećaj za jedan za naziv modela u sljedećem foldu
    brojac += 1

# FINALNI MODEL

numericke = ['index_vrucine1', 'temp_prosjek1', 'broj_soba', 'temp_max1', 'temp_min1', 'brzina_vjetra1', 'tlak_zraka1',
             'oblaci_pokrice1', 'oborine_mogucnost1',  'p_temp_min_31', 'p_temp_min_73', 'p_temp_max_31',  'p_oborine_mogucnost31', 'p_brzina_vjetra_73']
kategoricke = ['nacin_rezervacije', 'status_rezervacije', 'vrsta_sobe', 'kanal', 'tip_garancije']

#UCITAJ PIPELINE SA VRIJEDNOSTIMA SVOJSTVENIM ZA CIJELI DATASET
PrepPipeline = pickle.load(open('./Pipeline/Pipeline_Total.pkl', 'rb'))

# OBRADI PODATKE 
X_fit = PrepPipeline.transform(X)

# FINALNI MODEL
final_model = XGBClassifier(objective='binary:logistic', learning_rate=0.15, max_depth=6, min_child_weight=5, n_estimators=1000,
                            subsample=1, colsample_bytree=0.9, gamma=0.5, scale_pos_weight=2)
final_model.fit(X_fit, y, verbose=1)

# Spremi model nakon treninga
filename = 'Model_Final.pkl'
direktorij = './Modeli/'
putanja = os.path.join(direktorij, filename)
pickle.dump(model, open(putanja, 'wb'))
print("Model spremljen !!")


