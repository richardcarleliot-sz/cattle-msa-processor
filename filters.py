import os
from tqdm import tqdm
def filter_maf(maf_path, target_species_set):
    temp_path = maf_path + ".tmp"

    with open(maf_path, 'r') as fin, open(temp_path, 'w') as fout:
        buffer = []
        keep_block = False

        for line in fin:
            # 每个 block 开头
            if line.startswith('a '):
                # 写入上一个 block（只有包含目标物种才写）
                if buffer and keep_block:
                    fout.write("".join(buffer) + "\n")

                buffer = [line]
                keep_block = False

            elif line.startswith('s '):
                parts = line.split()
                if len(parts) > 1:
                    full_id = parts[1]
                    sp = full_id.split('.')[0]

                    if sp in target_species_set:
                        buffer.append(line)
                        keep_block = True

            elif line.startswith('#') or line.strip() == "":
                # 注释和空行直接写
                fout.write(line)

        # 最后一个 block
        if buffer and keep_block:
            fout.write("".join(buffer) + "\n")

    os.replace(temp_path, maf_path)  #硬盘不够用replace
    pass