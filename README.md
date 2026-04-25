# Cattle MSA Processor 

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**一个高性能、模块化的工具包，用于将多物种全基因组比对 (MAF) 数据转换为适用于深度学习模型训练的格式。**

---

## 功能概述 

本工具包提供了一个完整的流水线，用于处理大规模的多物种比对数据：
1.  **物种列表提取**：快速扫描 MAF 目录，提取所有物种名称。
2.  **数据过滤（可选）**：根据目标物种列表，缩减 MAF 文件体积。
3.  **高效格式转换**：将 MAF 文件转换为内存/磁盘友好的 **Zarr 张量格式** (形状: `[基因组位置, 物种数]`)。支持并行化和极速编码。
4.  **训练样本生成**：从 Zarr 数据中滑动生成高质量的训练/验证/测试窗口坐标 (Parquet 格式)，并进行严格的质量控制。

## 主要特性 
*   **极速处理**：利用 NumPy 向量化操作和内存映射，高效处理海量基因组数据。
*   **节省存储**：使用 `int8` 存储编码后的序列，并使用高压缩率的 Zarr 格式，大幅节省磁盘空间。
*   **即用型输出**：生成的 Zarr 和 Parquet 文件可直接与 PyTorch/TensorFlow 等主流框架集成，方便流式数据加载。
*   **用户友好**：提供统一的命令行接口，支持模块化分步执行。

## 安装 

### 从源码安装（推荐用于开发）
bash

git clone <您的仓库地址>

cd cattle-msa-processor
### 从 PyPI 安装
pip install -e .

bash

pip install cattle-msa-processor
## 快速开始 🚀

假设您有一组 `.maf` 文件存储在 `/path/to/maf_files` 目录中。

**第一步：获取物种列表**
bash

cattle-msa-processor list-species --maf_dir /path/to/maf_files

此命令会扫描目录并输出所有物种名称的列表。

**第二步（可选）：过滤物种**
假设您只想保留 `bosTau9` (牛), `hg38` (人), `mm10` (鼠) 的数据。
bash

cattle-msa-processor filter \

--maf_dir /path/to/maf_files \

--species bosTau9,hg38,mm10
*注意：此操作会**覆盖**原MAF文件，建议先备份。*

**第三步：转换为 Zarr 格式**
bash

cattle-msa-processor convert \

--maf_dir /path/to/maf_files \

--output_zarr ./output/msa_data.zarr \

--ref_species bosTau9 \

--species_list bosTau9,hg38,mm10 \

--chunk_size 100000
**第四步：生成训练窗口**
您问的是 README.md应该写什么。对于一个像“牛多物种比对数据处理工具”这样的专业软件包，一个优秀的 README.md是项目成功的关键。它需要清晰、全面地引导用户。

以下是针对您的 cattle-msa-processor​ 项目的 README.md​ 应包含的核心内容与结构建议。您可以以此为基础，填充具体信息。

README.md内容模板
markdown
复制
# Cattle MSA Processor 🐂

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**一个高性能、模块化的工具包，用于将多物种全基因组比对 (MAF) 数据转换为适用于深度学习模型训练的格式。**

---

## 功能概述 ✨

本工具包提供了一个完整的流水线，用于处理大规模的多物种比对数据：
1.  **物种列表提取**：快速扫描 MAF 目录，提取所有物种名称。
2.  **数据过滤（可选）**：根据目标物种列表，缩减 MAF 文件体积。
3.  **高效格式转换**：将 MAF 文件转换为内存/磁盘友好的 **Zarr 张量格式** (形状: `[基因组位置, 物种数]`)。支持并行化和极速编码。
4.  **训练样本生成**：从 Zarr 数据中滑动生成高质量的训练/验证/测试窗口坐标 (Parquet 格式)，并进行严格的质量控制。

## 主要特性 ⚡
*   **极速处理**：利用 NumPy 向量化操作和内存映射，高效处理海量基因组数据。
*   **节省存储**：使用 `int8` 存储编码后的序列，并使用高压缩率的 Zarr 格式，大幅节省磁盘空间。
*   **即用型输出**：生成的 Zarr 和 Parquet 文件可直接与 PyTorch/TensorFlow 等主流框架集成，方便流式数据加载。
*   **用户友好**：提供统一的命令行接口，支持模块化分步执行。

## 安装 📦

### 从源码安装（推荐用于开发）

bash

git clone <您的仓库地址>

cd cattle-msa-processor

pip install -e .

复制
### 从 PyPI 安装（发布后）

bash

pip install cattle-msa-processor

复制
## 快速开始 🚀

假设您有一组 `.maf` 文件存储在 `/path/to/maf_files` 目录中。

**第一步：获取物种列表**

bash

cattle-msa-processor list-species --maf_dir /path/to/maf_files

复制
此命令会扫描目录并输出所有物种名称的列表。

**第二步（可选）：过滤物种**
假设您只想保留 `bosTau9` (牛), `hg38` (人), `mm10` (鼠) 的数据。

bash

cattle-msa-processor filter \

--maf_dir /path/to/maf_files \

--species bosTau9,hg38,mm10

复制
*注意：此操作会**覆盖**原MAF文件，建议先备份。*

**第三步：转换为 Zarr 格式**

bash

cattle-msa-processor convert \

--maf_dir /path/to/maf_files \

--output_zarr ./output/msa_data.zarr \

--ref_species bosTau9 \

--species_list bosTau9,hg38,mm10 \

--chunk_size 100000

复制
**第四步：生成训练窗口**

bash

cattle-msa-processor make-windows \

--zarr_path ./output/msa_data.zarr \

--output ./output/train_windows.parquet \

--window 512 \

--step 512 \

--val_chroms 28,29 \

--test_chroms X \

--min_valid_ratio 0.7
## 详细使用说明 📖

### 1. 物种列表提取 (`list-species`)
*   用途：快速预览 MAF 目录中包含的所有物种。
*   输出：在终端打印逗号分隔的列表，并保存到当前目录的 `species_list.txt` 文件。

### 2. MAF 文件过滤 (`filter`)
*   用途：在后续分析前，剔除不感兴趣的物种，大幅减少数据量。
*   **重要**：此操作是**原地修改**，请确保已备份原始数据。

### 3. MAF 到 Zarr 转换 (`convert`)
这是核心步骤，参数说明：
*   `--ref_species`：指定参考基因组物种 (如 `bosTau9`)。其他物种的序列将根据此物种的坐标进行投影。
*   `--species_list`：逗号分隔的物种列表，定义输出 Zarr 数组中物种维度的顺序。
*   `--chunk_size`：Zarr 数组在基因组位置维度上的分块大小。影响后续读取性能，通常设为 10000 的倍数。

**输出结构**：
生成的 `.zarr` 目录是一个组 (Group)，每个染色体 (如 `1`, `2`, `X`) 是一个独立的 Zarr 数组 (Dataset)。
*   **形状**: `(染色体长度, 物种数量)`
*   **数据类型**: `int8`
*   **编码**:
    *   `0`: `A`
    *   `1`: `C`
    *   `2`: `G`
    *   `3`: `T`
    *   `4`: `N` 或间隙 (`-`)

### 4. 生成训练窗口 (`make-windows`)
从 Zarr 数据中创建用于模型训练的数据集。
*   `--window`: 窗口大小 (单位: bp)。
*   `--step`: 滑动步长。当 `step` < `window` 时，窗口会重叠。
*   `--val_chroms` / `--test_chroms`: 指定用于验证集和测试集的染色体。**未在此指定的染色体将全部用于训练集**。
*   `--min_valid_ratio`: 窗口内有效碱基 (`A`/`C`/`G`/`T`) 的最低比例，用于过滤低质量区域。

**输出文件 (`train_windows.parquet`)**：
一个包含以下列的表格：
| chrom | start | end | strand | split |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 0 | 512 | + | train |
| 1 | 512 | 1024 | + | train |
| ... | ... | ... | ... | ... |
| 28 | 10000 | 10512 | + | validation |

## 高级用法与集成 🔧

### 作为 Python 库使用
您也可以将本工具包作为库导入到自己的 Python 脚本中：
python

from cattle_msa_processor import maf_to_zarr_optimized, generate_windows

### 创建 PyTorch DataLoader
python

import zarr

import pandas as pd

import torch

from torch.utils.data import Dataset, DataLoader

class MSAWindowDataset(Dataset):

def init(self, zarr_path, parquet_path):

self.zarr_root = zarr.open_group(zarr_path, mode='r')

self.windows_df = pd.read_parquet(parquet_path)

# ... 实现 len和 getitem...

dataset = MSAWindowDataset('./output/msa_data.zarr', './output/train_windows.parquet')

dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

## 项目结构 📁
cattle-msa-processor/

├── cattle_msa_processor/     # 核心 Python 包

│   ├── init.py

│   ├── cli.py               # 统一命令行接口

│   ├── core.py              # 物种列表提取

│   ├── filters.py           # MAF 过滤

│   ├── converter.py         # MAF 到 Zarr 转换

│   ├── window_generator.py  # 窗口生成

│   └── utils.py             # 共享工具函数

├── setup.py

├── setup.cfg

├── requirements.txt

└── README.md                # 本文档
## 贡献 🤝
我们欢迎任何形式的贡献！请查阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。
1.  提交 Issue 报告 bug 或提出新功能建议。
2.  Fork 项目并提交 Pull Request。

## 许可证 📄
本项目基于 MIT 许可证开源。详情见 [LICENSE](LICENSE) 文件。

## 致谢
*   感谢 [Biopython](https://biopython.org/), [Zarr](https://zarr.readthedocs.io/), [pandas](https://pandas.pydata.org/) 等优秀开源项目。
*   本工具的设计灵感来源于大规模基因组学深度学习的前沿研究。