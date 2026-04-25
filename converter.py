import os
import zarr
import numpy as np
from Bio import AlignIO
from tqdm import tqdm
import glob
from .utils import encode_to_ids  
def maf_to_zarr_optimized(maf_dir, output_zarr, ref_species, species_list, chunk_size=100000):
    os.makedirs(os.path.dirname(output_zarr) if os.path.dirname(output_zarr) else '.', exist_ok=True)
    maf_files = sorted(glob.glob(os.path.join(maf_dir, "*.maf")))
    
    species_to_idx = {sp: i for i, sp in enumerate(species_list)}
    num_species = len(species_list)
    z_root = zarr.open_group(output_zarr, mode='a') 

    print("=== 第一阶段：扫描 MAF 获取序列长度并初始化 Zarr ===")
    chrom_info = {}
    for maf_file in tqdm(maf_files, desc="扫描进度"):
        for multiple_alignment in AlignIO.parse(maf_file, "maf"):
            for rec in multiple_alignment:
                parts = rec.id.split('.')
                sp_name = parts[0]
                if sp_name == ref_species:
                    chrom_id = parts[1] if len(parts) > 1 else "unknown"
                    if chrom_id not in chrom_info:
                        chrom_info[chrom_id] = rec.annotations['srcSize']
                    break

    print(f"共发现 {len(chrom_info)} 条序列。正在分配硬盘空间...")
    for chrom_id, length in chrom_info.items():
        if chrom_id not in z_root:
            # 采用 i1 (int8) 存储 Token ID，极大节省磁盘和显存
            # fill_value=4 代表默认全是 N
            z_root.create_dataset(
                chrom_id, 
                shape=(length, num_species), 
                chunks=(chunk_size, num_species), 
                dtype='i1', 
                fill_value=4
            )

    print("=== 第二阶段：将多物种对齐序列转换为 Token IDs 并落盘 ===")
    for maf_file in maf_files:
        chrom_name = os.path.basename(maf_file).replace(".maf", "")
        print(f"正在转换: {chrom_name}")
        
        for multiple_alignment in tqdm(AlignIO.parse(maf_file, "maf"), leave=False):
            ref_rec = next((r for r in multiple_alignment if r.id.split('.')[0] == ref_species), None)
            if not ref_rec: continue
            
            chrom_id = ref_rec.id.split('.')[1] if len(ref_rec.id.split('.')) > 1 else "unknown"
            start = ref_rec.annotations['start']
            
            if ref_rec.annotations['strand'] == -1:
                start = ref_rec.annotations['srcSize'] - start - ref_rec.annotations['size']
            
            # 使用 numpy 极速寻找参考序列中非 Gap 的位置
            ref_bytes = np.frombuffer(str(ref_rec.seq).encode('ascii'), dtype=np.uint8)
            non_gap_mask = (ref_bytes != 45) # 45 是 '-' 的 ASCII 码
            ref_len = np.sum(non_gap_mask)
            
            # 将该 Block 中所有物种投影至矩阵
            for rec in multiple_alignment:
                sp = rec.id.split('.')[0]
                if sp in species_to_idx:
                    idx = species_to_idx[sp]
                    # 极速转换为 ID 数组，并用 mask 剔除 Insertions
                    seq_ids = encode_to_ids(str(rec.seq))
                    z_root[chrom_id][start:start+ref_len, idx] = seq_ids[non_gap_mask]

    print(f"\n全部转换完成！高密度张量已存入: {output_zarr}")
    pass