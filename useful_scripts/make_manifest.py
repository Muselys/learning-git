#!/usr/bin/env python3
import os
import re
import sys

def find_pairs(root_dir: str):
    """
    Finds paired FASTQs under accession folders like:
      root/ERR123/anything/*.fastq.gz
    Pairs common patterns:
      sample_1.fastq.gz <-> sample_2.fastq.gz
      sample_R1.fastq.gz <-> sample_R2.fastq.gz
      sample_1.fq.gz <-> sample_2.fq.gz
      sample_R1.fq.gz <-> sample_R2.fq.gz
    """
    r1_patterns = [
        (re.compile(r"^(.*)_1\.(fastq|fq)\.gz$"), "_2"),
        (re.compile(r"^(.*)_R1\.(fastq|fq)\.gz$"), "_R2"),
    ]

    rows = []
    missing_r2 = []

    # iterate accession folders directly under root_dir
    for acc in sorted(os.listdir(root_dir)):
        acc_path = os.path.join(root_dir, acc)
        if not os.path.isdir(acc_path):
            continue

        # find fastqs anywhere under the accession folder
        for dirpath, _, filenames in os.walk(acc_path):
            for fn in filenames:
                if not (fn.endswith(".fastq.gz") or fn.endswith(".fq.gz")):
                    continue

                for pat, r2_tag in r1_patterns:
                    m = pat.match(fn)
                    if not m:
                        continue

                    prefix = m.group(1)
                    ext = m.group(2)  # fastq or fq
                    r1 = os.path.join(dirpath, fn)
                    r2_name = f"{prefix}{r2_tag}.{ext}.gz"
                    r2 = os.path.join(dirpath, r2_name)

                    if os.path.exists(r2):
                        # ID = accession (since your samples are accession-based)
                        rows.append((acc, r1, r2))
                    else:
                        missing_r2.append((acc, r1, r2))

                    break  # stop after first matching pattern

    return rows, missing_r2

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <reads_root_dir>", file=sys.stderr)
        sys.exit(2)

    root_dir = sys.argv[1]
    rows, missing_r2 = find_pairs(root_dir)

    with open("manifest.csv", "w") as f:
        f.write("ID,R1,R2\n")
        for acc, r1, r2 in rows:
            f.write(f"{acc},{r1},{r2}\n")

    print(f"Wrote manifest.csv with {len(rows)} pairs.")
    if missing_r2:
        print(f"WARNING: {len(missing_r2)} R1 files had no matching R2. Showing first 10:")
        for acc, r1, r2 in missing_r2[:10]:
            print(f"  {acc}: missing {r2} (from {r1})")

if __name__ == "__main__":
    main()
