import argparse

def main():
    parser = argparse.ArgumentParser(prog="cattle-msa-processor", description="MSA Data Processing Toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 子命令：list-species (对应 get_species_list.py)
    parser_list = subparsers.add_parser("list-species", help="Extract species list from MAF files")
    parser_list.add_argument("--maf_dir", required=True, help="Directory containing MAF files")
    parser_list.set_defaults(func=run_list_species)

    # 子命令：filter-maf (对应 filter_maf_species.py)
    parser_filter = subparsers.add_parser("filter-maf", help="Filter MAF files by species")
    parser_filter.add_argument("--maf_dir", required=True)
    parser_filter.add_argument("--species", required=True)
    parser_filter.set_defaults(func=run_filter_maf)

    # 子命令：maf-to-zarr (对应 maf_to_msa_zarr.py)
    parser_convert = subparsers.add_parser("maf-to-zarr", help="Convert MAF to Zarr tensor")
    parser_convert.add_argument("--maf_dir", required=True)
    parser_convert.add_argument("--output_zarr", required=True)
    parser_convert.add_argument("--ref_species", default="bosTau9")
    parser_convert.add_argument("--species_list", required=True)
    parser_convert.add_argument("--chunk_size", type=int, default=100000)
    parser_convert.set_defaults(func=run_maf_to_zarr)

    # 子命令：generate-windows (对应 generate_windows_parquet.py)
    parser_windows = subparsers.add_parser("generate-windows", help="Generate training windows from Zarr")
    parser_windows.add_argument("--zarr_path", required=True)
    parser_windows.add_argument("--output", required=True)
    parser_windows.add_argument("--window", type=int, default=512)
    parser_windows.add_argument("--step", type=int, default=512)
    parser_windows.add_argument("--val_chroms", default="")
    parser_windows.add_argument("--test_chroms", default="")
    parser_windows.add_argument("--min_valid_ratio", type=float, default=0.7)
    parser_windows.set_defaults(func=run_generate_windows)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
    else:
        args.func(args)  # 调用对应的函数

# 定义各个子命令对应的函数，这些函数内部调用您原先脚本中的核心函数
def handle_list_species(args):
    extract_species_fast(args.maf_dir)

def handle_filter(args):
    target_species = set(sp.strip() for sp in args.species.split(",") if sp.strip())
    maf_files = sorted(glob.glob(os.path.join(args.maf_dir, "*.maf")))
    for maf_file in maf_files:
        filter_maf(maf_file, target_species)

def handle_convert(args):
    species_list = [s.strip() for s in args.species_list.split(',')]
    maf_to_zarr_optimized(args.maf_dir, args.output_zarr, args.ref_species, species_list, args.chunk_size)

def handle_make_windows(args):
    val_list = [c.strip() for c in args.val_chroms.split(',')] if args.val_chroms else []
    test_list = [c.strip() for c in args.test_chroms.split(',')] if args.test_chroms else []
    generate_windows(args.zarr_path, args.output, args.window, args.step, val_list, test_list, args.min_valid_ratio)


if __name__ == "__main__":
    main()