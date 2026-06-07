from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
import pandas as pd

DATASET_PATH = "data/hf_dataset.csv"

df = pd.read_csv(DATASET_PATH)

train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

test_df.to_csv("data/hf_test.csv", index=False)

print(f"Train size: {len(train_df)}")
print(f"Test size:  {len(test_df)}")
print(f"Train label distribution:\n{train_df['label'].value_counts()}")
print(f"Test label distribution:\n{test_df['label'].value_counts()}")

train_examples = []
for _, row in train_df.iterrows():
    train_examples.append(
        InputExample(
            texts=[str(row["resume"]), str(row["job_description"])],
            label=float(row["label"])
        )
    )

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=8)
train_loss = losses.CosineSimilarityLoss(model)

model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=2,
    warmup_steps=100
)

model.save("fine_tuned_model")

print("Training complete. Model saved to fine_tuned_model/")
