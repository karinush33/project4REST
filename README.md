# Run-Predictor AI System 🏃‍♂️🤖

מערכת מקצה לקצה לחיזוי זמני ריצה מבוססת למידת מכונה (Polynomial Regression). 

## 🛠 טכנולוגיות
- **Backend:** FastAPI (Python)
- **ML:** Scikit-learn, Numpy
- **Security:** JWT Authentication, Bcrypt Password Hashing
- **Database:** SQLite

## 📄 דפים במערכת
1. **דף הבית (החיזוי):** זמין בכתובת המקורית `/`. מאפשר אימון מודל אישי וביצוע חיזויים.
2. **דף ניהול משתמשים:** זמין בכתובת `/management`. מאפשר צפייה, עדכון ומחיקה של משתמשים.

## 🚀 הוראות הרצה
1. התקנת ספריות: `pip install -r requirements.txt`
2. הרצת השרת: `uvicorn app:app --reload`
3. גישה למערכת: `http://127.0.0.1:8000`