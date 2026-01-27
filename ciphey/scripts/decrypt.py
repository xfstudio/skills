#!/usr/bin/env python3
"""
Ciphey wrapper script for automatic decryption/decoding.
Supports 50+ encryption/encoding types including Base64, Caesar, Vigenere, XOR, etc.

Installation methods (in order of preference):
1. Docker: docker run -it --rm remnux/ciphey
2. Homebrew: brew install ciphey
3. pipx: pipx install ciphey
"""

import subprocess
import sys
import shutil


def check_docker():
    """Check if Docker is available."""
    return shutil.which("docker") is not None


def check_ciphey_installed():
    """Check if ciphey is installed via any method."""
    # Check direct ciphey command
    if shutil.which("ciphey") is not None:
        return "direct"
    # Check Docker
    if check_docker():
        return "docker"
    return None


def install_ciphey():
    """Try to install ciphey using available methods."""
    # Try Homebrew first (macOS/Linux)
    if shutil.which("brew") is not None:
        print("Installing ciphey via Homebrew...")
        result = subprocess.run(
            ["brew", "install", "ciphey"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True

    # Try pipx
    if shutil.which("pipx") is not None:
        print("Installing ciphey via pipx...")
        result = subprocess.run(
            ["pipx", "install", "ciphey"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True

    return False


def decrypt(ciphertext: str, quiet: bool = False) -> str:
    """
    Decrypt/decode the given ciphertext using Ciphey.

    Args:
        ciphertext: The encrypted/encoded text to decrypt
        quiet: If True, suppress progress output

    Returns:
        The decrypted plaintext
    """
    method = check_ciphey_installed()

    if method is None:
        if not install_ciphey():
            # Fall back to Docker if available
            if check_docker():
                method = "docker"
            else:
                return "Error: Could not install ciphey. Please install manually:\n" \
                       "  - macOS/Linux: brew install ciphey\n" \
                       "  - Docker: docker pull remnux/ciphey\n" \
                       "  - pipx: pipx install ciphey"
        else:
            method = "direct"

    if method == "docker":
        cmd = ["docker", "run", "--rm", "remnux/ciphey", "-t", ciphertext]
        if quiet:
            cmd.append("-q")
    else:
        cmd = ["ciphey", "-t", ciphertext]
        if quiet:
            cmd.append("-q")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        output = result.stdout.strip()
        return output if output else "No decryption found"
    else:
        stderr = result.stderr.strip()
        if "No decryption found" in stderr or not stderr:
            return "No decryption found - text may not be encrypted or encoding not supported"
        return f"Error: {stderr}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python decrypt.py <ciphertext> [-q]")
        print("  ciphertext: The encrypted/encoded text to decrypt")
        print("  -q: Quiet mode (suppress progress output)")
        print("\nSupported methods:")
        print("  - Direct: ciphey command")
        print("  - Docker: remnux/ciphey image")
        print("  - Homebrew: brew install ciphey")
        sys.exit(1)

    ciphertext = sys.argv[1]
    quiet = "-q" in sys.argv

    result = decrypt(ciphertext, quiet)
    print(result)


if __name__ == "__main__":
    main()
