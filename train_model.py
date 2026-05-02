import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
import joblib

# ===============================
# 📊 EVALUASI TAMBAHAN
# ===============================
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
import matplotlib.pyplot as plt
import seaborn as sns

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("tiktok_shop_reviews_filtered1 (1).csv")

# ===============================
# LABEL
# ===============================
def label_sentiment(rating):
    if rating >= 4:
        return 'positif'
    elif rating >= 2:
        return 'netral'
    else:
        return 'negatif'

df['sentiment'] = df['Rating'].apply(label_sentiment)

# 🔍 CEK DISTRIBUSI
print(df['sentiment'].value_counts())

# ===============================
# FITUR
# ===============================
X = df['Comment'].astype(str)
y = df['sentiment']

# ===============================
# SPLIT
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ===============================
# 🔥 NAIVE BAYES
# ===============================
nb_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1,2))),
    ('clf', MultinomialNB())
])

classes = np.unique(y_train)
weights = compute_class_weight(class_weight='balanced', classes=classes, y=y_train)
class_weights = dict(zip(classes, weights))

sample_weights = y_train.map(class_weights)

nb_pipeline.fit(X_train, y_train, clf__sample_weight=sample_weights)

# ===============================
# 🔥 SVM
# ===============================
svm_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1,2))),
    ('clf', LinearSVC(class_weight='balanced'))
])

svm_pipeline.fit(X_train, y_train)

# ===============================
# 💾 SAVE MODEL
# ===============================
joblib.dump(nb_pipeline, "nb_model.joblib")
joblib.dump(svm_pipeline, "svm_model.joblib")

print("✅ MODEL SUDAH BALANCED & DISIMPAN")

# ===============================
# 📊 EVALUASI MODEL
# ===============================

y_pred_nb = nb_pipeline.predict(X_test)
y_pred_svm = svm_pipeline.predict(X_test)

acc_nb = accuracy_score(y_test, y_pred_nb)
acc_svm = accuracy_score(y_test, y_pred_svm)

print("\n===============================")
print("📊 HASIL AKURASI MODEL")
print("===============================")
print(f"Naive Bayes Accuracy : {acc_nb:.4f}")
print(f"SVM Accuracy         : {acc_svm:.4f}")

# ===============================
# 🏆 MODEL TERBAIK
# ===============================
if acc_nb > acc_svm:
    print("\n🏆 MODEL TERBAIK: NAIVE BAYES")
else:
    print("\n🏆 MODEL TERBAIK: SVM")

# ===============================
# 📉 CONFUSION MATRIX - NB
# ===============================
cm_nb = confusion_matrix(y_test, y_pred_nb, labels=classes)

plt.figure(figsize=(5,4))
sns.heatmap(cm_nb, annot=True, fmt='d', cmap='Blues',
            xticklabels=classes,
            yticklabels=classes)
plt.title("Confusion Matrix - Naive Bayes")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# ===============================
# 📉 CONFUSION MATRIX - SVM
# ===============================
cm_svm = confusion_matrix(y_test, y_pred_svm, labels=classes)

plt.figure(figsize=(5,4))
sns.heatmap(cm_svm, annot=True, fmt='d', cmap='Greens',
            xticklabels=classes,
            yticklabels=classes)
plt.title("Confusion Matrix - SVM")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# ===============================
# 📊 CLASSIFICATION REPORT
# ===============================
print("\n===============================")
print("📊 CLASSIFICATION REPORT NB")
print("===============================")
print(classification_report(y_test, y_pred_nb))

print("\n===============================")
print("📊 CLASSIFICATION REPORT SVM")
print("===============================")
print(classification_report(y_test, y_pred_svm))