from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="elderlycare",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="老年人关怀模型命令行工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/HealthButler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=[
        "click>=8.0.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "requests>=2.25.0",
        "transformers>=4.40.0",
        "torch>=2.1.0",
        "datasets>=2.18.0",
        "peft>=0.10.0",
        "trl>=0.8.6",
        "accelerate>=0.29.0",
        "bitsandbytes>=0.43.0",
        "swanlab>=0.2.0",
        "pandas>=2.0.0",
        "sentencepiece>=0.2.0",
        "modelscope>=1.16.0",
    ],
    entry_points={
        "console_scripts": [
            "elderlycare-cli=cli.cli:cli",
        ],
    },
)