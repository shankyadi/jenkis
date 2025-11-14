import torch
from torchtext.datasets import IMDB
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader
from torch import nn

# Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load dataset
train_iter = IMDB(split='train')
tokenizer = get_tokenizer("basic_english")

# Build vocabulary
def yield_tokens(data_iter):
    for label, line in data_iter:
        yield tokenizer(line)

vocab = build_vocab_from_iterator(yield_tokens(train_iter), specials=["<pad>"])
vocab.set_default_index(vocab["<pad>"])

# Encoding and batching
def encode(text):
    return torch.tensor(vocab(tokenizer(text)), dtype=torch.long)

def collate_batch(batch):
    text_list, label_list = [], []
    for label, text in batch:
        text_tensor = encode(text)
        text_list.append(text_tensor)
        label_list.append(1 if label == 'pos' else 0)
    text_list = pad_sequence(text_list, batch_first=True, padding_value=vocab["<pad>"])
    return text_list, torch.tensor(label_list, dtype=torch.long)

# RNN model
class SentimentRNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, output_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.RNN(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        embedded = self.embedding(x)
        output, hidden = self.rnn(embedded)
        return self.fc(hidden.squeeze(0))  # Final hidden state

# Model, loss, optimizer
model = SentimentRNN(len(vocab), embed_dim=64, hidden_dim=128, output_dim=2).to(device)
train_iter = IMDB(split='train')
train_loader = DataLoader(list(train_iter), batch_size=32, shuffle=True, collate_fn=collate_batch)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(5):
    model.train()
    total_loss, correct, total = 0, 0, 0
    for texts, labels in train_loader:
        texts, labels = texts.to(device), labels.to(device)
        optimizer.zero_grad()
        output = model(texts)
        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

        predicted = torch.argmax(output, dim=1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)
    
    accuracy = correct / total
    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}, Accuracy: {accuracy:.4f}")

# Predict custom input
def predict_sentiment(text):
    model.eval()
    with torch.no_grad():
        encoded = encode(text).unsqueeze(0).to(device)
        output = model(encoded)
        prediction = torch.argmax(output, dim=1).item()
        return "positive" if prediction == 1 else "negative"

# Test
print(predict_sentiment("This movie was amazing!"))
print(predict_sentiment("It was a terrible film."))


