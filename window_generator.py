import zarr
import pandas as pd
import numpy as np
from tqdm import tqdm
def generate_windows(zarr_path, output_parquet, window_size, step_size, val_chroms, test_chroms, min_valid_ratio=0.7):
    print(f"正在读取 Zarr 库: {zarr_path}")
    z_root = zarr.open_group(zarr_path, mode='r')

    records = []
    total_raw_windows = 0
    
    for chrom, dataset in z_root.items():
        chrom_len = dataset.shape[0]
        
        if chrom in val_chroms:
            split_name = "validation"
        elif chrom in test_chroms:
            split_name = "test"
        else:
            split_name = "train"
            
        print(f"正在切分染色体 {chrom} ({chrom_len} bp) -> {split_name} 集...")
        
       
        # 1.5 亿个 int8 仅占 150MB 内存，非常安全
        ref_ids = dataset[:, 0]
        
        for start in range(0, chrom_len - window_size + 1, step_size):
            total_raw_windows += 1
            end = start + window_size
            
            # 质量控制：统计有效碱基 (A,C,G,T 对应 0,1,2,3；N 对应 4)
            window_ref = ref_ids[start:end]
            valid_bases = np.sum(window_ref < 4) 
            
            # 如果有效碱基比例大于设定阈值 (默认 70%)，才保留此窗口
            if (valid_bases / window_size) >= min_valid_ratio:
                records.append({
                    "chrom": chrom,
                    "start": start,
                    "end": end,
                    "strand": "+", 
                    "split": split_name
                })

    df = pd.DataFrame(records)
    
    print("\n============== 数据集过滤统计 ==============")
    print(f"切分参数: 窗口 {window_size}bp | 步长 {step_size}bp")
    print(f"最低有效碱基要求: {min_valid_ratio * 100}%")
    print(f"原始产生窗口数: {total_raw_windows}")
    print(f"过滤后有效窗口: {len(df)} (保留率: {len(df)/total_raw_windows*100:.1f}%)")
    print("\n最终划分情况：")
    print(df["split"].value_counts().to_string())
    print("============================================")

    df.to_parquet(output_parquet, engine='pyarrow', index=False)
    print(f"\n高净度坐标 Parquet 已成功保存至: {output_parquet}")
    pass