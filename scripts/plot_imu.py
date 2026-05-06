"""Plot raw vs EMA acceleration from IMU pipeline CSV output."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd


def parse_args() -> argparse.Namespace:
    """Parse plotting options."""
    parser = argparse.ArgumentParser(description="Plot IMU raw vs EMA acceleration.")
    parser.add_argument("--input", default="data/imu_pipeline_log.csv")
    return parser.parse_args()


def plot_file(csv_path: str) -> None:
    """Load CSV and render acceleration comparison plots."""
    df = pd.read_csv(csv_path)

    fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    channels = ("x", "y", "z")

    for i, axis in enumerate(channels):
        axes[i].plot(df["time_s"], df[f"raw_accel_{axis}"], label=f"raw {axis}", alpha=0.65)
        axes[i].plot(df["time_s"], df[f"ema_accel_{axis}"], label=f"ema {axis}", linewidth=1.8)
        axes[i].set_ylabel(f"Accel {axis} (m/s^2)")
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)

    axes[-1].set_xlabel("Time (s)")
    fig.suptitle("IMU Acceleration: Raw vs EMA")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    args = parse_args()
    plot_file(args.input)
