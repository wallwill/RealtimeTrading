import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import torch
import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Download historical stock prices
ticker = "EURUSD=X"
start_date = "2024-04-01"
end_date = "2024-06-10"
data = yf.download(ticker, start=start_date, end=end_date)

# Extract closing prices
prices = data["Close"].tolist()

# Initialize tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Encode prices
encoded_prices = tokenizer.encode(" ".join([str(price) for price in prices]), return_tensors="pt")
attention_mask = torch.ones(encoded_prices.shape, dtype=torch.long)  # Generate attention mask

# Set model to training mode
model.train()

# Initialize optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)

# Resize token embeddings (GPT-2 does not typically require resizing, but kept for consistency)
model.resize_token_embeddings(len(tokenizer))

# Training loop
for _ in range(10):
    model.zero_grad()
    outputs = model(encoded_prices, labels=encoded_prices)
    loss = outputs.loss
    loss.backward()
    optimizer.step()

print("Entering the Generate Predictions Section..")

# Generate predictions
generated = model.generate(encoded_prices, attention_mask=attention_mask, max_length=700, temperature=1.0, num_return_sequences=1)

print("About to start decoding the tokens..")
# Decode generated tokens
generated_text = tokenizer.decode(generated[0], skip_special_tokens=True)
generated_prices = [float(price) for price in generated_text.split() if price.replace('.', '', 1).isdigit()]

# Ensure the length of generated prices matches the required length
predicted_prices = generated_prices[len(prices):len(prices) + len(prices)]

# Plot historical and predicted prices
plt.figure(figsize=(12, 6))
plt.plot(data.index, prices, label="Historical Prices")
future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=len(predicted_prices))
plt.plot(future_dates, predicted_prices, "g^", label="Predicted Prices")
plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.title(f"{ticker} - Historical and Predicted Stock Prices (GPT)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()