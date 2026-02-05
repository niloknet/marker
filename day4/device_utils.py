"""
Device selection utility (CUDA -> Apple Silicon (MPS) -> CPU)

Auto-select device for Stable Baselines3 / PyTorch.
"""


def get_device():
    """
    Priority: CUDA > Apple Silicon (MPS) > CPU

    Returns:
        "cuda", "mps", or "cpu"
    """
    import torch

    if torch.cuda.is_available():
        return "cuda"

    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"

    return "cpu"


def get_device_name(device) -> str:
    """Return human-readable device name."""
    if device is None:
        return "auto"
    s = str(device)
    if "cuda" in s.lower():
        return "CUDA"
    if "mps" in s.lower():
        return "Apple Silicon (MPS)"
    return "CPU"
