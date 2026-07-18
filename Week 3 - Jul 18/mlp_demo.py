"""Tutorial 2's MLP demonstration, Python file.

It compares a logistic-regression model with a small neural network (MLP) on
data that cannot be separated well with a straight line.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

OUTPUT_FILE = Path(__file__).with_name("mlp_vs_logistic_regression.png")


def plot_decision_boundary(model, features, labels, title, axis) -> None:
    """Draw the areas each model predicts as class 0 or class 1."""
    step_size = 0.02
    x_values, y_values = np.meshgrid(
        np.arange(features[:, 0].min() - 0.5, features[:, 0].max() + 0.5, step_size),
        np.arange(features[:, 1].min() - 0.5, features[:, 1].max() + 0.5, step_size),
    )

    grid = np.c_[x_values.ravel(), y_values.ravel()]
    predictions = model.predict(grid).reshape(x_values.shape)

    axis.contourf(x_values, y_values, predictions, alpha=0.3, cmap="coolwarm")
    axis.scatter(features[:, 0], features[:, 1], c=labels, cmap="coolwarm", edgecolors="k", s=25)
    axis.set_title(title, fontweight="bold")
    axis.set_xlabel("Feature 1")
    axis.set_ylabel("Feature 2")


def main() -> None:
    # The two half-moon shapes represent a pattern that is not a straight line.
    features, labels = make_moons(n_samples=300, noise=0.25, random_state=42)

    # This is the simple model from the previous tutorial.
    linear_model = LogisticRegression().fit(features, labels)

    # Our small MLP: two middle layers, with 16 small pattern-finders in each.
    mlp_model = MLPClassifier(
        hidden_layer_sizes=(16, 16),
        max_iter=3000,
        random_state=42,
    ).fit(features, labels)

    linear_accuracy = linear_model.score(features, labels)
    mlp_accuracy = mlp_model.score(features, labels)
    parameter_count = sum(weights.size for weights in mlp_model.coefs_) + sum(
        bias.size for bias in mlp_model.intercepts_
    )

    print("Two Moons: straight-line model vs small neural network\n")
    print(f"Logistic regression accuracy: {linear_accuracy:.0%}")
    print(f"MLP accuracy:                 {mlp_accuracy:.0%}")
    print(f"MLP trainable parameters:     {parameter_count}")
    print("\nThe MLP can form a curved boundary because its middle layers combine patterns.")

    figure, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    plot_decision_boundary(
        linear_model,
        features,
        labels,
        f"Logistic Regression | Accuracy: {linear_accuracy:.0%}",
        axes[0],
    )
    plot_decision_boundary(
        mlp_model,
        features,
        labels,
        f"Small MLP | Accuracy: {mlp_accuracy:.0%}",
        axes[1],
    )
    figure.tight_layout()
    figure.savefig(OUTPUT_FILE, dpi=160)
    print(f"\nChart saved to: {OUTPUT_FILE.name}")
    plt.show()


if __name__ == "__main__":
    main()