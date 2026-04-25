"""
Cattle MSA Processor - 一个用于处理多物种比对数据的高性能工具包。
"""

from .core import extract_species_fast
from .filters import filter_maf
from .converter import maf_to_zarr_optimized
from .window_generator import generate_windows
from .utils import encode_to_ids


__all__ = [
    'extract_species_fast',
    'filter_maf',
    'maf_to_zarr_optimized',
    'generate_windows',
    'encode_to_ids',
]

# 可选：定义包的版本号，便于管理
__version__ = '0.1.0'
__author__ = 'richardcarleliot-sz'