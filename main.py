import os
import shutil
import sys

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(base_dir, "entry.png")
    
    if not os.path.exists(src_path):
        print(f"Error: Source entry.png not found at {src_path}.", file=sys.stderr)
        sys.exit(1)
        
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception as e:
        print(f"Error: Failed to create output directory {out_dir}: {e}", file=sys.stderr)
        sys.exit(1)
    
    dst_path = os.path.join(out_dir, "entry.png")
    try:
        shutil.copy2(src_path, dst_path)
        print(f"Successfully copied entry.png to {dst_path}")
    except Exception as e:
        print(f"Error: Failed to copy entry.png to {dst_path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
