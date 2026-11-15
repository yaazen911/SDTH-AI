import csv
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# 1) قراءة البيانات من الملف
X = []  # المدخلات (الميزات)
y = []  # الإجابة الصحيحة (0 آمن، 1 خطر)
with open('training_data.csv') as f:
    for row in csv.DictReader(f):
        X.append([int(row['avg_speed']), int(row['max_speed']),
                  int(row['hard_brakes']), int(row['sharp_turns'])])
        y.append(int(row['label']))

# 2) تقسيم: 80% تدريب و20% اختبار
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3) تدريب الموديل
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4) تقييم الموديل على بيانات ما شافها
predictions = model.predict(X_test)
print('Accuracy:', accuracy_score(y_test, predictions))
print('Confusion matrix:')
print(confusion_matrix(y_test, predictions))

# 5) أهمية كل ميزة
names = ['avg_speed', 'max_speed', 'hard_brakes', 'sharp_turns']
for name, score in zip(names, model.feature_importances_):
    print(name, round(score, 3))

# 6) حفظ الموديل لاستخدامه لاحقاً بالنظام
joblib.dump(model, 'model.pkl')
print('تم حفظ الموديل بملف model.pkl')