from collections import Counter
import gzip
import os

data_dir = "/data/pam/team230/sm71/scratch/learning/fastqs"

# dataset: FASTQ filenames
fastq_files = [
    os.path.join(data_dir, f)
    for f in os.listdir(data_dir)
    if f.endswith(".fastq") or f.endswith(".fastq.gz")
]

# frequency tally: files per sample
samples = [f.split("_")[0] for f in fastq_files]
sample_file_counts = Counter(samples)

# frequency tally: file types
read_types = ["R1" if "_1" in f else "R2" for f in fastq_files]
read_type_counts = Counter(read_types)

# function to count reads inside FASTQ
def count_reads_in_fastq(filename):
    open_func = gzip.open if filename.endswith(".gz") else open
    with open_func(filename, "rt") as f:
        return sum(1 for _ in f) // 4

read_counts_per_file = {
    f: count_reads_in_fastq(f)
    for f in fastq_files
}

# write results to text file
with open("fastq_summary.txt", "w") as out:
    out.write("FASTQ files per sample:\n")
    for sample, count in sample_file_counts.items():
        out.write(f"{sample}: {count}\n")

    out.write("\nRead type counts (R1 vs R2):\n")
    for read_type, count in read_type_counts.items():
        out.write(f"{read_type}: {count}\n")

    out.write("\nSequencing read counts per FASTQ file:\n")
    for filename, count in read_counts_per_file.items():
        out.write(f"{filename}: {count}\n")