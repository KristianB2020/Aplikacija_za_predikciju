# UČITAJ TABLICE IZ BAZE I SPOJI U JEDNU LISTU
from Models import *
from Domain import *
from PreprocessingListe_final import *
from pony.orm import *
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
from imblearn.over_sampling import SVMSMOTE, SMOTE, ADASYN
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report, roc_curve, roc_auc_score, confusion_matrix, average_precision_score, f1_score, plot_confusion_matrix
import tensorflow as tf
from tensorflow import keras
from keras.metrics import Recall, Precision, BinaryAccuracy, SpecificityAtSensitivity
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau
from keras import layers

def plot_roc_curve(fpr,tpr): 
    plt.figure()
    plt.plot(fpr,tpr) 
    plt.axis([0,1,0,1]) 
    plt.xlabel('False Positive Rate') 
    plt.ylabel('True Positive Rate') 
    plt.show()  

def plotaj_matricu(cm, classes, normalize=False, title='Confusion matrica', cmap=plt.cm.Blues):
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalizirana matrica")
    else:
        print('Matrica bez normalizacije')
    print(cm)
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('Stvarni output')
    plt.xlabel('Predicirani output')
    plt.show()  

# pozovi funkciju i kreiraj listu za daljnju obradu
df = ucitaj_podatke_i_spoji()

# ucitaj iz datoteke
#df = pd.read_excel('Rezervacije_Trening.xlsx', index_col=0)

# FILTRIRANJE SUVIŠNIH REDAKA
df = df[df['broj_dana'] < 50]
df = df[df['jedinice'] < 17]
x = df.query('status_rezervacije == "F" or status_rezervacije == "N"  or status_rezervacije == "O" or status_rezervacije == "EF" or status_rezervacije == "EO" or status_rezervacije == "D"')

print("UKUPNI BROJ STORNA JE ", df['storno'].sum())

# izbaci nepotrebne kolone
df = df.drop(columns=['id','id_rezervacije', 'sif_hotela', 'sif_usluge', 'tip_ro', 'broj_osoba', 'broj_djece', 'cijena_pans_usl', 'godina', 'sif_rezervacije', 'rbr_stavke', 'vrijeme_kreiranje', 'valuta', 'tecaj', 'vrijeme_storna', 'sif_agencije', 'lead_time_dani', 'datum_do_potvrde_opcije', 'mjesec', 'datum_storna', 'vrsta_sobe_naplata', 'index_vrucine3', 'index_vrucine7', 'godina_rezervacije', 'obaveza_akontacije', 'sif_drzave'])
print("OVO JE NAKON PRVOG IZBACIVANJA")
print(df.columns)

# #podijeli datetime kolone "dan boravka" i "datum_kreiranja" na dan, mjesec...
df['dan_boravka']= pd.to_datetime(df['dan_boravka'])
df['mjesec'] = df['dan_boravka'].dt.month
df['dan_u_tjednu'] = df['dan_boravka'].dt.dayofweek
df['dan_u_godini'] = df['dan_boravka'].dt.dayofyear
df['tjedan'] = df['dan_boravka'].dt.week

df['datum_kreiranja']= pd.to_datetime(df['datum_kreiranja']) 
df['kreirano_dana_prije_dolaska'] = (df['dan_boravka'] - df['datum_kreiranja']).dt.days

df.drop('datum_kreiranja', axis=1, inplace=True)
df.drop('dan_boravka', axis=1, inplace=True)

# NUll vrijednosti zamijeni nulom u kolonama
df['iznos_akontacije'].fillna(value=0, inplace=True)

# stavi storno na kraj
dfStorno = df['storno']
df = df.drop('storno', axis='columns')
df['storno'] = dfStorno

# int to float za kolone
int_kolone = ['kreirano_dana_prije_dolaska', 'broj_dana', 'broj_soba', 'jedinice', 'dat_storna_do_dat_dolaska', 'mjesec', 'dan_u_tjednu', 'dan_u_godini', 'tjedan', 'storno']
for kolona in int_kolone:
    df[kolona] = df[kolona].astype(float)
	
# MICANJE OUTLIERA I OSTALIH SUVIŠNIH KOLONA
df = df.drop('postotak_akontacije', axis='columns')

d_oborine_mogucnost = np.percentile(df['oborine_mogucnost1'], 0) 
g_oborine_mogucnost = np.percentile(df['oborine_mogucnost1'], 99) 
df = df[df.oborine_mogucnost1.between(d_oborine_mogucnost, g_oborine_mogucnost)]

d_oborine_mogucnost = np.percentile(df['oborine_mogucnost3'], 0) 
g_oborine_mogucnost = np.percentile(df['oborine_mogucnost3'], 99) 
df = df[df.oborine_mogucnost3.between(d_oborine_mogucnost, g_oborine_mogucnost)]

d_oborine_mogucnost = np.percentile(df['oborine_mogucnost7'], 0) 
g_oborine_mogucnost = np.percentile(df['oborine_mogucnost7'], 99) 
df = df[df.oborine_mogucnost7.between(d_oborine_mogucnost, g_oborine_mogucnost)]

d_temp_min = np.percentile(df['temp_min1'], 0) 
g_temp_min = np.percentile(df['temp_min1'], 99) 
df = df[df.temp_min1.between(d_temp_min, g_temp_min)]

d_iznos_akontacije = np.percentile(df['iznos_akontacije'], 0) 
g_iznos_akontacije = np.percentile(df['iznos_akontacije'], 98) 
df = df[df.iznos_akontacije.between(d_iznos_akontacije, g_iznos_akontacije)]


df.reset_index(drop=True, inplace=True)

# PODJELA NA INPUT I OUTPUT & PIPELINE ZA IMPUTER, SCALER, TARGET ENCODING 
y = df.storno
X = df.drop(columns= ['storno', 'broj_dana', 'p_tlak_zraka_31', 'jedinice', 'iznos_bruto', 'p_tlak_zraka_73', 'p_temp_max_73', 'p_oborine_mogucnost73', 'p_brzina_vjetra_31', 'mjesec', 'dan_u_tjednu', 'dan_u_godini', 'tjedan', 'kreirano_dana_prije_dolaska', 'p_oblaci_pokrice_31', 'p_oblaci_pokrice_73', 'iznos_akontacije', 'nocenja', 'prognoza3', 'prognoza1', 'prognoza7', 'dat_storna_do_dat_dolaska', 'temp_prosjek3', 'temp_max3', 'temp_min3', 'brzina_vjetra3', 'tlak_zraka3', 'oblaci_pokrice3', 'oborine_mogucnost3', 'temp_prosjek7', 'temp_max7', 'temp_min7', 'brzina_vjetra7', 'tlak_zraka7', 'oblaci_pokrice7', 'oborine_mogucnost7'], axis='columns')


# - FOLD------------------------------------------------------------------------------------------------------------
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=7)

brojac = 1
for train, test in kfold.split(X_fit,y):
    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape=(brojInputa,), name='PrviSloj'))
    model.add(keras.layers.Dense(16, activation=tf.nn.relu, name='DrugiSloj'))
    model.add(keras.layers.Dense(8, activation=tf.nn.relu, name='TreciSloj'))
    model.add(keras.layers.Dense(4, activation=tf.nn.relu, name='CetvrtiSloj'))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid, name='Izlaz'))

    #opt_adam = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=10e-08, decay=0.0)
    model.compile(optimizer='adam',
                    loss='binary_crossentropy',
                    metrics=[Recall(), Precision(), BinaryAccuracy(threshold=0.5), SpecificityAtSensitivity(0.5)])

    # zaustavi treniranje modela ako n epoha nema poboljšanja u metrici
    callback_early_stopping = EarlyStopping(monitor='val_precision',
                                        patience=20, verbose=1)

    # upisuj u log tijekom treniranja
    callback_tensorboard = TensorBoard(log_dir='./Logovi/',
                                   histogram_freq=0,
                                   write_graph=False)
    # zabilježi svaki checkpoint
    path_checkpoint = 'Checkpoint.keras'
    callback_checkpoint = ModelCheckpoint(filepath=path_checkpoint,
                                          monitor='val_precision',
                                          verbose=1,
                                          save_weights_only=True,
                                          save_best_only=True)
    
    # smanji learning rate za faktor 0.1 ako se validation-loss u zadnjih n epoha nije poboljšao 
    callback_reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                          factor=0.1,
                                          min_lr=1e-4,
                                          patience=20,
                                          verbose=1)

    stopovi = [callback_early_stopping,
                callback_checkpoint,
                callback_tensorboard,
                callback_reduce_lr]

    X_train, y_train = X.iloc[train], y.iloc[train]
    X_test, y_test = X.iloc[test], y.iloc[test]
    

    # PROCESIRANJE PODATAKA
    # DEFINIRAJ LISTE ZA NUMERIČKE I ZA KATEGORIČKE VARIJABLE
    numericke = ['index_vrucine1', 'temp_prosjek1', 'broj_soba', 'temp_max1', 'temp_min1', 'brzina_vjetra1', 'tlak_zraka1', 'oblaci_pokrice1', 'oborine_mogucnost1',
                 'p_temp_min_31', 'p_temp_min_73', 'p_temp_max_31',  'p_oborine_mogucnost31', 'p_brzina_vjetra_73']
    kategoricke = ['nacin_rezervacije', 'status_rezervacije', 'vrsta_sobe', 'kanal', 'tip_garancije']

    NumPipeline = Pipeline([('impute', SimpleImputer(strategy='mean', missing_values=np.nan)), ('scale', StandardScaler())])
    KatPipeline = Pipeline([('impute', SimpleImputer(strategy='most_frequent', missing_values=np.nan)), ('encode', TargetEncoder()), ('scale', StandardScaler())])

    FinalPipeline = ColumnTransformer([('prep_numericke', NumPipeline, numericke), ('prep_kategoricke', KatPipeline, kategoricke)], remainder='passthrough')

    X_train_fit = FinalPipeline.fit_transform(X_train, y_train)
    X_test_fit = FinalPipeline.transform(X_test)

    # Spremi pipeline
    filename = 'Pipeline_CV_keras' + str(brojac) + '.pkl'
    direktorij = './Pipeline/'
    putanja = os.path.join(direktorij, filename)
    pickle.dump(FinalPipeline, open(putanja, 'wb'))
    print("Pipeline CV spremljen !!")

    print("Ovo je stvarni broj ne-storna / storna u testu", np.bincount(y_test))
    # SMOTE + Edited Nearest Neighbors Undersampling
    over = SMOTETomek(random_state=40, sampling_strategy=1)
    X_train_fit, y_train = over.fit_resample( X_train_fit, y_train)
    print("OVO SU NOVE VRIJEDNOSTI NAKON OVERSAMPLINGA", y_train.value_counts(), np.bincount(y_train))

    history = model.fit(X_train, y_train, epochs=50, batch_size=10)
    try:
        model.load_weights(path_checkpoint)
    except Exception as error:
        print("Pogreska kod učitavanja checkpoint-a.")
        print(error)

    # Recall, Precision
    plt.figure()
    plt.plot(history.history['recall_' + str(brojac)])
    plt.plot(history.history['precision_'+ str(brojac)])
    plt.title('Recall & Precision')
    plt.ylabel('Postotak')
    plt.xlabel('epoha')
    plt.legend(['Recall', 'Precision'], loc='upper left')
    plt.show()
    # # Loss
    # plt.figure()
    # plt.plot(history.history['loss'])
    # plt.plot(history.history['val_loss'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    # plt.show()

    test_loss, test_recall, test_precision, test_bin_acc, test_SvS = model.evaluate(X_test, y_test)
    print("REZULTATI EVALUACIJE:")
    print('Test Loss:', test_loss)
    print('Test Recall:', test_recall)
    print('Test Precision:', test_precision)
    print('Test Binary Acc:', test_bin_acc)
    print('Test SvS:', test_SvS)

    # ROC & AUC 
    y_vjerojatnosti = model.predict_proba(X_test)
    fpr, tpr, thresholds = roc_curve(y_test, y_vjerojatnosti)
    auc_score = roc_auc_score(y_test, y_vjerojatnosti)
    print("AUC SCORE : ", auc_score)
    plot_roc_curve(fpr,tpr) 

    # CLASSIFICATION REPORT
    y_klase = model.predict_classes(X_test)
    print(classification_report(y_test, y_klase))

    # # PLOT MATRICE KONFUZIJE
    y_predikcije = model.predict_classes(X_test)
    cm = confusion_matrix(y_true=y_test, y_pred=y_predikcije)
    cm_plot_nazivi = ['nije_storno','storno']
    plotaj_matricu(cm=cm, classes=cm_plot_nazivi, title='Confusion Matrica')

    # Spremi model nakon treninga
    model.save("Model_keras"+str(brojac)+".h5")
    print(model.summary())
    
    # uvećaj za jedan za naziv modela u sljedećem foldu
    brojac += 1
