"""
Train a lightweight TensorFlow Keras ranker over engineered features.
"""
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split


def build_model(input_dim: int) -> tf.keras.Model:
    inp = tf.keras.Input(shape=(input_dim,))
    x = tf.keras.layers.Dense(64, activation="relu")(inp)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(32, activation="relu")(x)
    out = tf.keras.layers.Dense(1, activation="sigmoid")(x)
    model = tf.keras.Model(inp, out)
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["AUC"])
    return model


def main():
    features_path = "ml_pipeline/results/features.csv"
    if not os.path.exists(features_path):
        raise SystemExit("Run ml_pipeline/feature_engineering.py first.")
    df = pd.read_csv(features_path).drop(columns=["id"])
    y = (df["emb_mean"] > df["emb_mean"].median()).astype(int).values
    X = df.values.astype("float32")
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    model = build_model(X.shape[1])
    model.fit(Xtr, ytr, epochs=10, batch_size=16, validation_data=(Xte, yte), verbose=2)
    os.makedirs("ml_pipeline/results", exist_ok=True)
    model.save("ml_pipeline/results/ranker.keras")
    print("Saved ranker to ml_pipeline/results/ranker.keras")


if __name__ == "__main__":
    main()
