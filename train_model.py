import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
import numpy as np
from pathlib import Path

print("=" * 60)
print("🤖 Fake Message Detection Model Training")
print("=" * 60)

# Check if dataset exists
if not Path("combined_data.csv").exists():
    print("\n⚠️ ERROR: combined_data.csv not found!")
    print("Please ensure your training dataset is in the project root directory.")
    print("Expected format: CSV with 'label' and 'text' columns")
    print("Labels: 'ham' (real) or 'spam' (fake)")
    exit(1)

print("\n📂 Loading dataset...")
try:
    # Load dataset with different encodings to handle various formats
    try:
        df = pd.read_csv("combined_data.csv", encoding='utf-8')
    except:
        df = pd.read_csv("combined_data.csv", encoding='latin-1')
    
    print(f"✓ Dataset loaded: {len(df)} messages")
except Exception as e:
    print(f"✗ Error loading dataset: {e}")
    exit(1)

print("\n🔍 Data Preprocessing...")

# Keep only necessary columns
available_cols = df.columns.tolist()
print(f"Available columns: {available_cols}")

# Find label and text columns (case-insensitive)
label_col = None
text_col = None

for col in available_cols:
    col_lower = col.lower()
    if 'label' in col_lower:
        label_col = col
    if any(x in col_lower for x in ['text', 'message', 'content', 'email', 'body']):
        text_col = col

if label_col is None or text_col is None:
    print(f"✗ Could not find required columns")
    print(f"Need: label column and text/message column")
    exit(1)

print(f"✓ Using columns: label='{label_col}', text='{text_col}'")

# Keep only relevant columns
df = df[[label_col, text_col]]
df.columns = ['label', 'message']

print(f"Original dataset size: {len(df)}")

# Remove duplicates
df = df.drop_duplicates()
print(f"After removing duplicates: {len(df)}")

# Remove empty rows
df = df.dropna()
print(f"After removing null values: {len(df)}")

# Convert message column to string
df['message'] = df['message'].astype(str)

# Remove very short messages
df = df[df['message'].str.len() > 2]
print(f"After removing very short messages: {len(df)}")

# Standardize labels
print("\n🏷️ Processing labels...")
unique_labels = df['label'].unique()
print(f"Found labels: {unique_labels}")

# Map labels to binary (0: real/ham, 1: fake/spam)
label_mapping = {}
for label in unique_labels:
    label_lower = str(label).lower().strip()
    if label_lower in ['ham', 'real', '0', 'legitimate']:
        label_mapping[label] = 0
    else:
        label_mapping[label] = 1

print(f"Label mapping: {label_mapping}")
df['label'] = df['label'].map(label_mapping)

# Remove unmapped labels
df = df.dropna()

# Check class distribution
print(f"\n📊 Class Distribution:")
print(f"Real messages (0): {(df['label'] == 0).sum()}")
print(f"Fake messages (1): {(df['label'] == 1).sum()}")

if len(df) < 10:
    print("✗ Not enough data to train model (minimum 10 samples)")
    exit(1)

# Prepare data
print("\n🔧 Preparing data for training...")
X = df['message'].values
y = df['label'].values

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

# Vectorize text
print("\n📝 Vectorizing text with TF-IDF...")
try:
    vectorizer = TfidfVectorizer(
        max_features=5000,
        min_df=1,
        max_df=0.95,
        ngram_range=(1, 2),
        lowercase=True,
        stop_words='english',
        token_pattern=r'\b\w{2,}\b'  # Only words with 2+ characters
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"✓ Vectorization complete")
    print(f"  Features created: {X_train_vec.shape[1]}")
    print(f"  Training samples: {X_train_vec.shape[0]}")
    
except Exception as e:
    print(f"✗ Vectorization failed: {e}")
    exit(1)

# Train model
print("\n🚀 Training Logistic Regression model...")
try:
    model = LogisticRegression(
        max_iter=1000,
        solver='lbfgs',
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    
    model.fit(X_train_vec, y_train)
    print("✓ Model training complete")
    
except Exception as e:
    print(f"✗ Training failed: {e}")
    exit(1)

# Evaluate model
print("\n📈 Model Evaluation:")
try:
    # Training accuracy
    train_pred = model.predict(X_train_vec)
    train_acc = accuracy_score(y_train, train_pred)
    print(f"Training Accuracy: {train_acc:.4f} ({train_acc*100:.2f}%)")
    
    # Test accuracy
    test_pred = model.predict(X_test_vec)
    test_acc = accuracy_score(y_test, test_pred)
    print(f"Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    
    # Detailed classification report
    print("\n" + "="*60)
    print("Detailed Classification Report (Test Set):")
    print("="*60)
    print(classification_report(
        y_test, test_pred,
        target_names=['Real Messages', 'Fake Messages'],
        digits=4
    ))
    
    # Confusion matrix
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, test_pred)
    print(f"True Negatives: {cm[0][0]}")
    print(f"False Positives: {cm[0][1]}")
    print(f"False Negatives: {cm[1][0]}")
    print(f"True Positives: {cm[1][1]}")
    
except Exception as e:
    print(f"⚠️ Error during evaluation: {e}")

# Save model and vectorizer
print("\n💾 Saving model and vectorizer...")
try:
    pickle.dump(model, open("model.pkl", "wb"))
    print("✓ Model saved: model.pkl")
    
    pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
    print("✓ Vectorizer saved: vectorizer.pkl")
    
    # Save model info
    model_info = {
        'accuracy': float(test_acc),
        'features': X_train_vec.shape[1],
        'training_samples': len(X_train),
        'test_samples': len(X_test),
        'parameters': {
            'max_iter': 1000,
            'solver': 'lbfgs',
            'vectorizer_max_features': 5000
        }
    }
    
    pickle.dump(model_info, open("model_info.pkl", "wb"))
    print("✓ Model info saved: model_info.pkl")
    
except Exception as e:
    print(f"✗ Save failed: {e}")
    exit(1)

print("\n" + "="*60)
print("✅ Training Complete!")
print("="*60)
print("\nYour model is ready to use!")
print("Run: python app.py")
print("Then open: http://127.0.0.1:5500")
