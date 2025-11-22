# Example PyTorch training script with GPU support
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

# Check for GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

# Simple neural network
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Create dummy data (replace with real dataset)
print("Generating training data...")
X_train = torch.randn(10000, 784).to(device)
y_train = torch.randint(0, 10, (10000,)).to(device)

# Initialize model
model = SimpleNet().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
print("Starting training...")
losses = []
batch_size = 64
epochs = 10

start_time = time.time()

for epoch in range(epochs):
    epoch_loss = 0
    for i in range(0, len(X_train), batch_size):
        batch_X = X_train[i:i+batch_size]
        batch_y = y_train[i:i+batch_size]

        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()

    avg_loss = epoch_loss / (len(X_train) / batch_size)
    losses.append(avg_loss)
    print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")

training_time = time.time() - start_time
print(f"Training completed in {training_time:.2f} seconds")

# Plot training loss
plt.figure(figsize=(10, 6))
plt.plot(losses)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss Over Time')
plt.grid(True)
plt.savefig('training_loss.png', dpi=150, bbox_inches='tight')
print("Saved training_loss.png")

# Save model
torch.save(model.state_dict(), 'model.pth')
print("Saved model.pth")

# Save training log
with open('training.log', 'w') as f:
    f.write(f"Device: {device}\n")
    f.write(f"Training time: {training_time:.2f} seconds\n")
    f.write(f"Final loss: {losses[-1]:.4f}\n")
    if torch.cuda.is_available():
        f.write(f"GPU: {torch.cuda.get_device_name(0)}\n")
        f.write(f"Max memory allocated: {torch.cuda.max_memory_allocated() / 1e9:.2f} GB\n")

print("Training complete! Check artifacts for results.")
