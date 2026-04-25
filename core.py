import os
import glob
from tqdm import tqdm
def extract_species_fast(maf_dir):
    maf_files = sorted(glob.glob(os.path.join(maf_dir, "*.maf")))
    if not maf_files:
        print(f"错误：在 {maf_dir} 中没找到 MAF 文件。")
        return

   
    all_species = set() 
    
    BUFFER_SIZE = 64 * 1024 * 1024 

    print(f"正在以二进制流模式扫描 {len(maf_files)} 个 MAF 文件...")

    for maf_file in tqdm(maf_files):
        with open(maf_file, 'rb') as f: 
            while True:
                chunk = f.read(BUFFER_SIZE)
                if not chunk:
                    break
                
                # 寻找 's ' 标志行（物种起始行）
                # 注意：由于是二进制读取，需要匹配 b'\ns '
                lines = chunk.split(b'\ns ')
                for i in range(1, len(lines)):
                    # 提取物种 ID 字段
                    line_part = lines[i].split(None, 1)[0]
                    full_id = line_part.decode('ascii', errors='ignore')
                    species = full_id.split('.')[0]
                    
                    # 修改处：set 使用 add() 而非 append()
                    all_species.add(species) 

    # 排序并输出结果
    sorted_species = sorted(list(all_species))
    
    print("\n" + "="*30)
    print(f"扫描完成！共发现 {len(sorted_species)} 个物种。")
    print("="*30)
    
    species_string = ",".join(sorted_species)
    print(f"物种列表 (可直接用于 Zarr 转换脚本):\n{species_string}")
    
    # 同时保存到本地文件，方便后续查看
    with open("species_list.txt", "w") as f_out:
        f_out.write(species_string)