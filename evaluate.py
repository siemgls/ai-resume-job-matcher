import pandas as pd
from matcher import final_match_score
from sklearn.metrics import accuracy_score, f1_score, classification_report

DATASET_PATH = "data/hf_dataset.csv"


def evaluate_binary_classification():
    df = pd.read_csv(DATASET_PATH)

    predictions = []
    scores = []

    for _, row in df.iterrows():
        result = final_match_score(str(row["resume"]), str(row["job_description"]))
        score = result["final_score"]

        prediction = 1 if score >= 60 else 0

        scores.append(score)
        predictions.append(prediction)

    accuracy = accuracy_score(df["label"], predictions)
    f1 = f1_score(df["label"], predictions)

    print("=== Binary Classification Evaluation ===")
    print("Accuracy:", round(accuracy, 4))
    print("F1 Score:", round(f1, 4))
    print()
    print(classification_report(df["label"], predictions))

    output_df = df.copy()
    output_df["predicted_label"] = predictions
    output_df["final_score"] = scores
    output_df.to_csv("data/evaluation_results.csv", index=False)

    print("Saved detailed results to data/evaluation_results.csv")


def evaluate_ranking():
    ranking_tests = [
        {
            "job": "Looking for a data scientist with Python, SQL, machine learning, pandas, and scikit-learn.",
            "resumes": [
                ("Python developer with SQL, machine learning, pandas, and scikit-learn experience.", 1),
                ("Retail worker with cashier and customer service experience.", 0),
                ("Graphic designer with Photoshop and branding experience.", 0),
                ("Mobile developer with Flutter and Firebase experience.", 0),
            ],
        },
        {
            "job": "Hiring frontend developer with React, JavaScript, HTML, CSS, and responsive design experience.",
            "resumes": [
                ("Frontend developer with React, JavaScript, HTML, CSS, and UI design experience.", 1),
                ("Cybersecurity analyst with SIEM and incident response experience.", 0),
                ("HR assistant with payroll and onboarding experience.", 0),
                ("Backend Java developer with Spring Boot and REST APIs.", 0),
            ],
        },
        {
            "job": "Looking for DevOps engineer with Docker, Kubernetes, AWS, Linux, and CI/CD experience.",
            "resumes": [
                ("DevOps engineer with Docker, Kubernetes, AWS, Linux, and CI/CD pipelines.", 1),
                ("UX designer with Figma, wireframes, and usability testing.", 0),
                ("Marketing specialist with SEO and social media campaign experience.", 0),
                ("Data analyst with Excel, SQL, and Power BI dashboards.", 0),
            ],
        },
    ]

    top1_correct = 0
    all_results = []

    print()
    print("=== Ranking Evaluation ===")

    for i, test in enumerate(ranking_tests, start=1):
        job = test["job"]
        scored_resumes = []

        for resume_text, label in test["resumes"]:
            result = final_match_score(resume_text, job)
            score = result["final_score"]
            scored_resumes.append((resume_text, score, label))

        scored_resumes.sort(key=lambda x: x[1], reverse=True)

        if scored_resumes[0][2] == 1:
            top1_correct += 1

        print(f"\nRanking Test {i}")
        print("Job:", job)
        print("Ranked resumes:")

        for rank, (resume_text, score, label) in enumerate(scored_resumes, start=1):
            print(f"{rank}. Score: {score} | Label: {label} | Resume: {resume_text}")

            all_results.append({
                "test_id": i,
                "rank": rank,
                "job_description": job,
                "resume": resume_text,
                "score": score,
                "label": label
            })

    top1_accuracy = top1_correct / len(ranking_tests)

    print()
    print("Top-1 Ranking Accuracy:", round(top1_accuracy, 4))

    ranking_df = pd.DataFrame(all_results)
    ranking_df.to_csv("data/ranking_results.csv", index=False)

    print("Saved ranking results to data/ranking_results.csv")


if __name__ == "__main__":
    evaluate_binary_classification()
    evaluate_ranking()