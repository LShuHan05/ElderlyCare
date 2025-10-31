"""
允许通过 `python -m elderlycare` 运行命令行工具
"""
from .cli import cli

if __name__ == "__main__":
    cli()