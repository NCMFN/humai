import nbformat as nbf

def add_markdown(nb, text):
    nb.cells.append(nbf.v4.new_markdown_cell(text))

def add_code(nb, code):
    nb.cells.append(nbf.v4.new_code_cell(code))

nb = nbf.v4.new_notebook()

add_markdown(nb, "# Automated Classification of Infant Dermatitis vs. Healthy Skin\n\nThis notebook develops a lightweight deep learning image classifier that distinguishes between:\n- Dermatitis (infant-related skin conditions like Atopic Dermatitis, Eczema)\n- Healthy skin\n\nOptimized for low computational cost and suitable for deployment in real-world, resource-constrained environments (e.g., mobile health tools).")

add_markdown(nb, "## 1. Setup and Imports\n\nFirst, we'll install/import the required libraries and mount Google Drive if necessary, or just set up our environment.")

setup_code = """!pip install pydot graphviz
import os
import zipfile
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2

# For plotting models
import pydot
import graphviz

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping

print("TensorFlow Version:", tf.__version__)"""
add_code(nb, setup_code)

add_markdown(nb, "## 2. Data Preparation\n\nExtracting the uploaded ZIP file and organizing the dataset into the required structure:\n```\ndata/\n  train/\n    healthy/\n    dermatitis/\n  validation/\n    healthy/\n    dermatitis/\n```\nWe merge 'Atopic Dermatitis' and 'Eczema' into the single class 'Dermatitis'.")

data_prep_code = """# Define paths
ZIP_PATH = "dataset.zip" # Replace with actual path if needed when running in Colab
BASE_DIR = "extracted_data"
DATA_DIR = "data"

# Extract zip file
if os.path.exists(ZIP_PATH):
    print(f"Extracting {ZIP_PATH}...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(BASE_DIR)
else:
    print(f"Please upload your dataset zip file as '{ZIP_PATH}'")

# Create new directory structure
for split in ['train', 'validation']:
    for cls in ['healthy', 'dermatitis']:
        os.makedirs(os.path.join(DATA_DIR, split, cls), exist_ok=True)

# Helper function to move files and merge classes
def process_data(source_dir, is_train=True):
    split_name = 'train' if is_train else 'validation'
    if not os.path.exists(source_dir):
        return

    # Map raw class folders to target class folders
    class_mapping = {
        'Atopic Dermatitis': 'dermatitis',
        'Eczema': 'dermatitis',
        'Healthy': 'healthy',
        'healthy': 'healthy',
        'dermatitis': 'dermatitis'
    }

    for folder in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder)
        if not os.path.isdir(folder_path):
            continue

        target_class = None
        for key, val in class_mapping.items():
            if key.lower() in folder.lower():
                target_class = val
                break

        if target_class:
            target_dir = os.path.join(DATA_DIR, split_name, target_class)
            for img in os.listdir(folder_path):
                if img.lower().endswith(('.png', '.jpg', '.jpeg')):
                    src_img = os.path.join(folder_path, img)
                    dst_img = os.path.join(target_dir, f"{folder}_{img}")
                    shutil.copy(src_img, dst_img)

print("Organizing dataset...")
# Recursively find train and validation directories
train_dirs = []
val_dirs = []
for root, dirs, files in os.walk(BASE_DIR):
    for d in dirs:
        lower_d = d.lower()
        if lower_d in ['train', 'training']:
            train_dirs.append(os.path.join(root, d))
        elif lower_d in ['val', 'validation', 'test']:
            val_dirs.append(os.path.join(root, d))

for d in train_dirs:
    process_data(d, is_train=True)
for d in val_dirs:
    process_data(d, is_train=False)

# Check counts
for split in ['train', 'validation']:
    print(f"\\n{split.upper()} set:")
    for cls in ['healthy', 'dermatitis']:
        dir_path = os.path.join(DATA_DIR, split, cls)
        count = len(os.listdir(dir_path)) if os.path.exists(dir_path) else 0
        print(f"  {cls}: {count} images")"""
add_code(nb, data_prep_code)

add_markdown(nb, "## 3. Data Augmentation\n\nWe use `ImageDataGenerator` to apply transformations (Rotation, Horizontal flip, Zoom, Brightness) to the training data. The validation data will only be rescaled.")

data_aug_code = """# Define parameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Training Data Generator with Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    horizontal_flip=True,
    zoom_range=0.2,
    brightness_range=[0.8, 1.2]
)

# Validation Data Generator (only rescaling)
val_datagen = ImageDataGenerator(rescale=1./255)

# Load data from directories
train_dir = os.path.join(DATA_DIR, 'train')
val_dir = os.path.join(DATA_DIR, 'validation')

print("Loading training data:")
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    classes=['healthy', 'dermatitis']  # 0: healthy, 1: dermatitis
)

print("\nLoading validation data:")
val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    classes=['healthy', 'dermatitis'],
    shuffle=False
)

# Class indices
class_indices = train_generator.class_indices
print("\nClass mapping:", class_indices)
"""
add_code(nb, data_aug_code)

add_markdown(nb, "## 4. Model Development (Transfer Learning)\n\nWe use a pretrained `MobileNetV2` model as our base (freezing its layers), and add a custom classification head (GlobalAveragePooling2D -> Dense -> Dropout -> Sigmoid).")

model_dev_code = """# Load pretrained MobileNetV2
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

# Freeze the base model
base_model.trainable = False

# Add custom classification head
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(1, activation='sigmoid')(x)

# Construct the final model
model = Model(inputs=base_model.input, outputs=predictions)

model.summary()

# Plot the system architecture
print("\\nGenerating System Architecture Diagram...")
try:
    tf.keras.utils.plot_model(model, to_file='system_architecture.png', show_shapes=True, show_layer_names=True)
    img = cv2.imread('system_architecture.png')
    if img is not None:
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title('System Architecture')
        plt.show()
except Exception as e:
    print(f"Could not plot model architecture. Ensure pydot and graphviz are installed. Error: {e}")
"""
add_code(nb, model_dev_code)

add_markdown(nb, "## 5. Model Compilation & Training\n\nWe compile the model with `Adam` optimizer and `Binary Crossentropy` loss. Then we train it with an `Early Stopping` callback.")

training_code = """# Compile the model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy',
             tf.keras.metrics.Precision(name='precision'),
             tf.keras.metrics.Recall(name='recall')]
)

# Early stopping callback
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True,
    verbose=1
)

# Train the model
EPOCHS = 15

print("Starting training...")
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator,
    callbacks=[early_stopping],
    verbose=1
)
"""
add_code(nb, training_code)

add_markdown(nb, "## 6. Model Evaluation\n\nWe evaluate the model using Accuracy, Precision, Recall, F1-score, and visually inspect a Confusion Matrix and training curves.")

eval_code = """from sklearn.metrics import classification_report, confusion_matrix

# Plot training history
def plot_history(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Loss plot
    ax1.plot(history.history['loss'], label='Train Loss')
    ax1.plot(history.history['val_loss'], label='Val Loss')
    ax1.set_title('Model Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()

    # Accuracy plot
    ax2.plot(history.history['accuracy'], label='Train Accuracy')
    ax2.plot(history.history['val_accuracy'], label='Val Accuracy')
    ax2.set_title('Model Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.legend()

    plt.tight_layout()
    plt.savefig('training_curves.png', dpi=300)
    print("Saved training curves to 'training_curves.png'")
    plt.show()

if 'history' in locals():
    plot_history(history)

# Evaluate on validation set
print("\nEvaluating on validation set:")
eval_results = model.evaluate(val_generator)
print(f"Validation Loss: {eval_results[0]:.4f}")
print(f"Validation Accuracy: {eval_results[1]:.4f}")
print(f"Validation Precision: {eval_results[2]:.4f}")
print(f"Validation Recall: {eval_results[3]:.4f}")

# Get predictions for confusion matrix
val_generator.reset()
Y_pred = model.predict(val_generator)
y_pred_classes = (Y_pred > 0.5).astype(int).reshape(-1)
y_true = val_generator.classes

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Healthy', 'Dermatitis'],
            yticklabels=['Healthy', 'Dermatitis'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300)
print("Saved confusion matrix to 'confusion_matrix.png'")
plt.show()

# Classification Report Table
print("\\nClassification Report Table:")
report_dict = classification_report(y_true, y_pred_classes, target_names=['Healthy', 'Dermatitis'], output_dict=True)
report_df = pd.DataFrame(report_dict).transpose()
report_df.to_csv('classification_results_table.csv')
print("Saved classification results table to 'classification_results_table.csv'")
display(report_df.round(4))

# Display Correctly vs Incorrectly Classified Images
def show_classified_samples(val_gen, y_true, y_pred, is_correct, num_samples=5):
    filepaths = val_gen.filepaths
    indices = [i for i, (t, p) in enumerate(zip(y_true, y_pred)) if (t == p) == is_correct]

    samples = indices[:num_samples]
    if not samples:
        print(f"No {'correctly' if is_correct else 'incorrectly'} classified samples found.")
        return

    plt.figure(figsize=(15, 3))
    for i, idx in enumerate(samples):
        img_path = filepaths[idx]
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        plt.subplot(1, num_samples, i + 1)
        plt.imshow(img)
        true_label = "Dermatitis" if y_true[idx] == 1 else "Healthy"
        pred_label = "Dermatitis" if y_pred[idx] == 1 else "Healthy"
        plt.title(f"True: {true_label}\\nPred: {pred_label}")
        plt.axis('off')
    status = "Correctly" if is_correct else "Incorrectly"
    plt.suptitle(f"{status} Classified Images", y=1.1)
    plt.tight_layout()
    plt.savefig(f'{status.lower()}_classified_images.png', dpi=300)
    print(f"Saved {status.lower()} classified images to '{status.lower()}_classified_images.png'")
    plt.show()

print("\\nCorrectly Classified Images:")
show_classified_samples(val_generator, y_true, y_pred_classes, is_correct=True)

print("\\nIncorrectly Classified Images:")
show_classified_samples(val_generator, y_true, y_pred_classes, is_correct=False)
"""
add_code(nb, eval_code)

add_markdown(nb, "## 7. Model Interpretation (Bonus: Grad-CAM)\n\nWe use Grad-CAM to visualize which regions of an image the model uses to make its predictions.")

grad_cam_code = """import tensorflow as tf
from tensorflow.keras.models import Model

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    # Create a model that maps the input image to the activations of the last conv layer as well as the output predictions
    grad_model = Model(
        inputs=[model.inputs],
        outputs=[model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    # Gradient of the output neuron with respect to the output feature map
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # Vector where each entry is the mean intensity of the gradient over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Multiply each channel in the feature map array by "how important this channel is" with regard to the top predicted class
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # Normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def display_gradcam(img_path, heatmap, alpha=0.4):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    superimposed_img = heatmap * alpha + img
    superimposed_img = np.clip(superimposed_img, 0, 255).astype('uint8')

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title("Original Image")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(superimposed_img)
    plt.title("Grad-CAM")
    plt.axis('off')

    filename = os.path.basename(img_path)
    plt.tight_layout()
    plt.savefig(f'gradcam_{filename}', dpi=300)
    print(f"Saved Grad-CAM visualization to 'gradcam_{filename}'")
    plt.show()

# Get sample images
sample_imgs = []
for cls in ['healthy', 'dermatitis']:
    dir_path = os.path.join(DATA_DIR, 'validation', cls)
    if os.path.exists(dir_path):
        files = os.listdir(dir_path)
        if files:
            sample_imgs.append(os.path.join(dir_path, files[0]))

# Find the last convolutional layer
last_conv_layer = None
for layer in reversed(model.layers):
    if len(layer.output_shape) == 4:
        last_conv_layer = layer.name
        break

print(f"Using layer {last_conv_layer} for Grad-CAM")

for img_path in sample_imgs:
    img_array = cv2.imread(img_path)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    img_array = cv2.resize(img_array, IMG_SIZE)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer)
    display_gradcam(img_path, heatmap)
"""
add_code(nb, grad_cam_code)

add_markdown(nb, "## 8. Inference\n\nA simple function to predict on a new, unseen image.")

inference_code = """def predict_image(img_path, model):
    if not os.path.exists(img_path):
        print(f"Image {img_path} not found.")
        return

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Preprocess
    img_resized = cv2.resize(img, IMG_SIZE)
    img_array = np.expand_dims(img_resized, axis=0) / 255.0

    # Predict
    pred_prob = model.predict(img_array)[0][0]

    # Label
    label = "Dermatitis" if pred_prob > 0.5 else "Healthy"
    confidence = pred_prob if pred_prob > 0.5 else 1 - pred_prob

    # Display
    plt.figure(figsize=(4, 4))
    plt.imshow(img)
    plt.title(f"{label} ({confidence:.2%} confidence)")
    plt.axis('off')
    plt.show()

    return label, confidence

# Example prediction on a validation image
if sample_imgs:
    predict_image(sample_imgs[0], model)
"""
add_code(nb, inference_code)

add_markdown(nb, "## 9. Bonus: Convert Model to TensorFlow Lite (TFLite)\n\nWe convert the model to TFLite format to make it lightweight and suitable for mobile deployment.")

tflite_code = """# Save standard model
model.save("infant_dermatitis_model.h5")

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model
with open('infant_dermatitis_model.tflite', 'wb') as f:
    f.write(tflite_model)

print("TFLite model saved successfully. Size:", len(tflite_model) / (1024 * 1024), "MB")
"""
add_code(nb, tflite_code)

with open("infant_dermatitis_classification.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)
