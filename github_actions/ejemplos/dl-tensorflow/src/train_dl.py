import tensorflow as tf
import numpy as np

def build_and_train():
    # Datos dummy
    X = np.random.random((100, 10))
    y = np.random.randint(0, 2, (100, 1))

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    print("Training Deep Learning model...")
    model.fit(X, y, epochs=5, verbose=0)
    
    loss, acc = model.evaluate(X, y, verbose=0)
    print(f"Accuracy: {acc:.4f}")

    model.save("models/dl_model.h5")
    print("TF Model saved to models/dl_model.h5")

if __name__ == "__main__":
    build_and_train()
