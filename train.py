from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import pandas as pd

df = pd.read_csv("data/sample_pairs.csv")

train_examples = []

for _, row in df.iterrows():
    train_examples.append(
        InputExample(
            texts=[row["resume"], row["job_description"]],
            label=float(row["label"])
        )
    )

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=8)
train_loss = losses.CosineSimilarityLoss(model)

model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=2,
    warmup_steps=10
)

model.save("fine_tuned_model")

print("Training complete. Model saved to fine_tuned_model/")