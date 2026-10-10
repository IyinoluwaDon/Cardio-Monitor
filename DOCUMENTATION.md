# Cardio Monitor: Full Project Documentation

---

## Table of contents

1. [What is Cardio Monitor?](#1-what-is-cardio-monitor)
2. [Who is it for?](#2-who-is-it-for)
3. [How a person uses it](#3-how-a-person-uses-it)
4. [The 13 questions explained](#4-the-13-questions-explained)
5. [How the prediction works](#5-how-the-prediction-works)
6. [The data behind it](#6-the-data-behind-it)
7. [How accurate is it?](#7-how-accurate-is-it)
8. [How the project was built (the process)](#8-how-the-project-was-built-the-process)
9. [What each file does](#9-what-each-file-does)
10. [Privacy and safety](#10-privacy-and-safety)
11. [Limitations and honest warnings](#11-limitations-and-honest-warnings)
12. [Frequently asked questions](#12-frequently-asked-questions)

---

## 1. What is Cardio Monitor?

Cardio Monitor is a small website that gives an **estimate of a person's risk of heart disease**.

You type in 13 health details, such as age, blood pressure and cholesterol. The site compares your details with records of 303 real patients and tells you whether your profile looks closer to people with **low risk** or **high risk**. It then shows two charts comparing your numbers to the typical low-risk person.

It also has an "About heart disease" page that explains the types of heart disease, symptoms, risk factors and ways to prevent it.

**What it is not:** it is not a doctor and it does not diagnose anything. It is a learning project that shows how a computer can find patterns in medical data.

## 2. Who is it for?

- **Students and teachers** who want a clear example of machine learning on real data.
- **Curious visitors** who want to see how data can be used to estimate health risk.
- **Developers** who want a simple, database-free Streamlit app they can study or reuse.

## 3. How a person uses it

1. Open the website.
2. On the **Predict** page, fill in the form (name is optional and only used to greet you).
3. Press **Predict**.
4. Read the result:
   - A **green message** means your profile resembles low-risk patients.
   - A **red message** means your profile resembles high-risk patients and you should speak to a doctor.
5. Look at the **percentage** shown. It tells you how strongly the model leans toward "low risk".
6. Look at the **two charts** to see where your numbers differ from the typical low-risk person.
7. Use the sidebar to open **About heart disease** for general education.

## 4. The 13 questions explained

Doctors use short names for these measurements. Here is what each one means in everyday words.

| Question (short name) | What it means in simple terms |
|---|---|
| **Age** | Your age in years. Risk generally rises with age. |
| **Sex** | Male or female. In the data, men had more heart disease cases. |
| **Chest pain type** (cp) | The kind of chest pain you feel: typical angina (classic heart-related pain), atypical angina, non-anginal pain (probably not the heart), or none at all (asymptomatic). |
| **Resting blood pressure** (trestbps) | Blood pressure while sitting calmly, in mm Hg. High numbers strain the heart. |
| **Serum cholesterol** (chol) | The amount of cholesterol in the blood, in mg/dl. Too much can clog arteries. |
| **Fasting blood sugar over 120** (fbs) | Whether your blood sugar, after not eating, is above 120 mg/dl. This is linked to diabetes. |
| **Resting ECG** (restecg) | The result of an ECG (a heart electrical recording) taken at rest: normal, a wave abnormality, or signs of a thickened heart wall. |
| **Maximum heart rate** (thalach) | The highest heartbeat rate reached during an exercise test. |
| **Exercise induced angina** (exang) | Whether exercise causes chest pain. |
| **ST depression** (oldpeak) | How much a certain part of the ECG line drops during exercise compared to rest. Bigger drops can signal a heart under stress. |
| **Slope of the ST segment** (slope) | The direction that ECG line moves at peak exercise: up, flat, or down. |
| **Major vessels colored** (ca) | The number (0 to 3) of main blood vessels that show up on a special X-ray scan. |
| **Thalassemia result** (thal) | A heart scan result: normal, a fixed defect (damage that stays the same), or a reversible defect (blood flow problem that shows up only during exercise). |

**Note:** several of these (ST depression, vessels colored, thalassemia, resting ECG) come from tests done at a hospital. Most people will need a doctor's report to fill them in.

## 5. How the prediction works

### The idea in one sentence

The computer finds the **7 past patients most similar to you** and goes with the majority.

### An everyday analogy

Imagine you move to a new town and want to know if a restaurant is good. You ask the 7 people whose tastes are most like yours. If 5 of them loved it, you will probably love it too.

Cardio Monitor does the same thing:

1. It stores 303 patient records, each marked "low risk" or "high risk".
2. When you enter your details, it measures how close you are to every patient.
3. It picks the **7 closest patients**.
4. If most of them are low risk, you get a low-risk result. If most are high risk, you get a high-risk result.

This method is called **K-Nearest Neighbors**, or **KNN**. The "K" is the number of neighbors asked. Here, K = 7.

### Why the percentage looks the way it does

The percentage is simply how many of the 7 neighbors were low risk. So it can only be 0%, 14%, 29%, 43%, 57%, 71%, 86% or 100%. For example, 6 out of 7 gives 86%.

This is a vote count, not a medical probability. Treat it as "how clear-cut the vote was".

### Making the comparison fair (scaling)

Cholesterol numbers are in the hundreds, but "number of vessels" is 0 to 3. If the computer compared them directly, cholesterol would drown out everything else.

To fix this, every measurement is squeezed onto the same 0-to-1 scale before comparing. This is called **min-max scaling**. It is like converting every test score to a percentage so that a 20-mark quiz and a 200-mark exam can be compared fairly.

### Teaching and testing the model

1. The 303 records were split: **80% (242 patients)** to learn from and **20% (61 patients)** hidden for testing.
2. The model learned from the 242 and was then tested on the 61 it had never seen. This gives an honest accuracy score.
3. After testing, the model is retrained on **all 303** records so the live app uses every bit of data.

This all happens automatically in a fraction of a second when the app starts. Nothing is saved to a database.

## 6. The data behind it

- **File:** `heart.csv`
- **Size:** 303 patients, 13 measurements each, plus a label.
- **Source:** the well-known UCI Heart Disease dataset (Cleveland hospital collection), widely used for teaching.
- **Label split:** 165 patients are marked low risk and 138 high risk.
- **Sex split:** 207 male and 96 female patients.

Because the data is small, old and mostly from one place, results should be seen as a demonstration (see section 11).

## 7. How accurate is it?

On the 61 hidden test patients, the model got about **90%** right (55 out of 61).

What that means in plain terms:

- Roughly 9 out of 10 test patients were classified correctly.
- 61 patients is a small test group, so the real-world figure could be higher or lower.
- A computer being right 9 times out of 10 on old hospital records does **not** mean it is right 9 times out of 10 for you.

## 8. How the project was built (the process)

### Where it started

The original project was a **Flask** website (Flask is a tool for building websites with Python). It had several moving parts:

- A set of separate HTML page templates
- A **MongoDB database** that stored visitors' details and counted page visits
- Saved ("pickled") model files
- Several Python files that had to work together

### What was asked for

Rewrite the project to run on **Streamlit**, remove the database, show the new owner's authorship in the README, and make everything work properly.

### The steps taken

**Step 1: Read and understand everything.**
Every file was read first: the Flask app, the database code, the model-training code, the prediction code, the chart code, the HTML pages and the dataset.

**Step 2: Test what was already there.**
The two saved model files were tested. They **failed to load** on current versions of the scikit-learn library, because they were saved with a much older version. This decided the approach: instead of fixing old files, the model now trains fresh from the CSV when the app starts.

**Step 3: Choose the model settings.**
Different settings were compared on the data. Min-max scaling with 7 neighbors gave the best result (about 90%) and matched the original project's design, so it was kept.

**Step 4: Check the data against the original code.**
This found real bugs in the old app (see next section). The new app uses the codes that match the dataset.

**Step 5: Build the new app.**
Two Python files replaced the old collection of files:
- `model.py` holds the data, the question-to-number codes, training and prediction.
- `app.py` holds everything the user sees.

**Step 6: Remove what is no longer needed.**
The database code, the HTML templates, the old prediction and chart files, the saved model files and the server config were deleted.

**Step 7: Test it.**
- The app was run with an automated tester to check both pages load with no errors.
- A clearly high-risk profile and a clearly low-risk profile were submitted. The first gave a high-risk result and the second a low-risk result, as expected.
- The real Streamlit server was started and confirmed running.

**Step 8: Write the documentation.**
The README (quick start) and this document (full explanation) were written, and a license file with both authors' names was added.

### Bugs found and fixed in the old version

| Problem in the old app | Why it mattered | Fix |
|---|---|---|
| The form sent "Male" but the code looked for "male" | Every user was treated as female, which skewed all predictions | Sex is now matched correctly |
| Thalassemia answers were converted to numbers (6, 7, 2.31) that do not exist in this dataset | The model received values it had never seen | Now uses the dataset's real codes (1, 2, 3) |
| Chest pain "asymptomatic" was coded as 3 in one file and 2 in another | The prediction and the chart disagreed | One shared set of codes in `model.py` |
| The chart's "Normal Value" was actually the average of the high-risk group | The chart was mislabeled and misleading | Now compares to the low-risk group average and says so |
| Saved model files break on current software | The app could not start | Model trains from the CSV at launch |
| Database login details were written inside a code file | A security risk | The database and that file are gone |

### Why these design choices?

- **No database:** the project does not need to remember anyone. Removing it makes the app simpler, free to host and better for privacy.
- **Train at startup instead of saving a model file:** it avoids version-mismatch breakage, and with only 303 rows it takes a fraction of a second.
- **Streamlit instead of Flask:** a Streamlit app is one Python file with no HTML to write, which makes the project much easier to read, change and deploy.
- **Keep KNN:** it is easy to explain, needs no tuning tricks and performs well on this small dataset.

## 9. What each file does

```
Cardio-Monitor/
├── app.py                # The website: pages, form, results, charts
├── model.py              # The brain: data, codes, training, prediction
├── heart.csv             # The 303 patient records
├── requirements.txt      # List of software the project needs
├── README.md             # Quick-start guide
├── DOCUMENTATION.md      # This document
├── LICENSE               # Usage rights and credits
├── .gitignore            # Files Git should not upload
├── .streamlit/
│   └── config.toml       # Colour theme (teal)
├── static/
│   ├── heartlogo.png     # Logo
│   ├── about.jpg         # Image (kept from the original project)
│   └── corousal/         # Slides shown on the About page
└── heart disease prediction/
                          # Original research notebooks
```

### `app.py` in plain words

- Sets up the page title, logo and layout.
- Shows a sidebar menu with two pages: **Predict** and **About heart disease**.
- Builds the form and checks that numbers stay in sensible ranges (for example, age 1 to 120).
- When Predict is pressed, packages the answers, asks the model for a result, and shows the message, percentage and charts.
- Shows a footer crediting the author and the original project.

### `model.py` in plain words

- Loads the CSV.
- Holds the "translation tables" that turn dropdown choices (like "Typical angina") into the numbers the data uses (like 0).
- Trains the model, measures its accuracy, then retrains on all data.
- Calculates the average low-risk values used in the charts.
- Provides the function that turns one person's answers into a result.

### `requirements.txt`

The shopping list of software: Streamlit (the website framework), pandas and NumPy (handling data), scikit-learn (the machine learning), and Matplotlib (the charts).

## 10. Privacy and safety

- **Nothing is stored.** There is no database, no log of answers and no user accounts.
- Answers exist only while you view your result and disappear when you close the page.
- The name field is only used to say hello.
- No secrets, passwords or keys are used anywhere in the project.

## 11. Limitations and honest warnings

Please read these before trusting any result.

1. **It is not medical advice.** Only a doctor can assess heart health.
2. **Small dataset.** 303 patients is tiny by modern standards. A real clinical tool would use many thousands.
3. **Old and narrow data.** The records come from one hospital collection from decades ago. Populations, lifestyles and treatments have changed.
4. **Unbalanced groups.** There are more men than women in the data, so predictions may be less reliable for women.
5. **Missing risk factors.** The model does not ask about smoking, weight, diet, family history, exercise habits or stress, all of which matter.
6. **Hospital-only inputs.** Several questions need medical test results most people do not have.
7. **Simple method.** KNN does not weigh features by importance or explain exactly why it chose a result.
8. **A high-risk result is not a diagnosis, and a low-risk result is not a clean bill of health.** If you have symptoms such as chest pain, shortness of breath or fainting, seek medical care regardless of what this app says.

## 12. Frequently asked questions

**Does it store my health details?**
No. There is no database and nothing is saved.

**Can I rely on the result?**
No. It is an educational estimate, not medical advice.

**Why do I get a different percentage than I expected?**
The percentage is a vote among 7 neighbors, so it only takes a few fixed values (0%, 14%, 29%, and so on).

**Why does it ask for things I do not know, like thalassemia?**
Those come from hospital tests and are part of the original dataset. If you do not have them, ask a doctor or treat the app as a demo.

**Why was the database removed?**
The app does not need to remember anyone. Removing it makes the project simpler, cheaper and safer for privacy.

**Why does the app train the model every time it starts?**
The dataset is small, so training takes a moment, and it avoids the version-breakage problem that saved model files have.

**Can I use or modify this project?**
Yes, under the MIT license in the `LICENSE` file. Keep the copyright notices.
