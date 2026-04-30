import pandas as pd
from matcher import final_match_score
from sklearn.metrics import accuracy_score, f1_score, classification_report

DATASET_PATH = "data/hf_dataset.csv"


def get_scores(df):
    scores = []

    for _, row in df.iterrows():
        result = final_match_score(str(row["resume"]), str(row["job_description"]))
        scores.append(result["final_score"])

    return scores


def find_best_threshold(labels, scores):
    best_threshold = 0
    best_f1 = 0

    for threshold in range(20, 91, 5):
        predictions = [1 if score >= threshold else 0 for score in scores]
        f1 = f1_score(labels, predictions)

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold

    return best_threshold, best_f1


def evaluate_binary_classification():
    df = pd.read_csv(DATASET_PATH)

    labels = df["label"].tolist()
    scores = get_scores(df)

    best_threshold, best_f1 = find_best_threshold(labels, scores)

    predictions = [1 if score >= best_threshold else 0 for score in scores]

    accuracy = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions)

    print("=== Binary Classification Evaluation ===")
    print("Best Threshold:", best_threshold)
    print("Accuracy:", round(accuracy, 4))
    print("F1 Score:", round(f1, 4))
    print()
    print(classification_report(labels, predictions))

    output_df = df.copy()
    output_df["final_score"] = scores
    output_df["predicted_label"] = predictions
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
    top3_correct = 0
    all_results = []

    print()
    print("=== Ranking Evaluation ===")

    for i, test in enumerate(ranking_tests, start=1):
        scored_resumes = []

        for resume_text, label in test["resumes"]:
            score = final_match_score(resume_text, test["job"])["final_score"]
            scored_resumes.append((resume_text, score, label))

        scored_resumes.sort(key=lambda x: x[1], reverse=True)

        if scored_resumes[0][2] == 1:
            top1_correct += 1

        if any(item[2] == 1 for item in scored_resumes[:3]):
            top3_correct += 1

        print(f"\nRanking Test {i}")
        for rank, (resume_text, score, label) in enumerate(scored_resumes, start=1):
            print(f"{rank}. Score: {score} | Label: {label} | Resume: {resume_text}")

            all_results.append({
                "test_id": i,
                "rank": rank,
                "job_description": test["job"],
                "resume": resume_text,
                "score": score,
                "label": label
            })

    top1_accuracy = top1_correct / len(ranking_tests)
    top3_accuracy = top3_correct / len(ranking_tests)

    print()
    print("Top-1 Ranking Accuracy:", round(top1_accuracy, 4))
    print("Top-3 Ranking Accuracy:", round(top3_accuracy, 4))

    pd.DataFrame(all_results).to_csv("data/ranking_results.csv", index=False)
    print("Saved ranking results to data/ranking_results.csv")


if __name__ == "__main__":
    evaluate_binary_classification()
    evaluate_ranking()