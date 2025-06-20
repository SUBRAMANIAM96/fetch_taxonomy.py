from Bio import Entrez
import time
import re
from datetime import datetime
import os

# Set your email for NCBI Entrez API (mandatory)
Entrez.email = "subramanyamvkumar@gmail.com"

# List of input BLAST output files to process
input_files = [
    "/mnt/c/Users/User/downloads/Master_thesis/DADA2_Files/cleaned_OTU/cleaned_otu_sample06b_results.out"
]

def extract_accession(acc_string):
    """
    Extract GenBank accession number from a gi|XXX|db|ACCESSION| formatted string.
    
    Args:
        acc_string (str): The full accession string.
        
    Returns:
        str or None: Extracted accession number or None if not found.
    """
    match = re.search(r"gi\|\d+\|[A-Za-z]+(?:\|([A-Za-z0-9_.]+))", acc_string)
    return match.group(1) if match else None

def fetch_taxonomy(acc_number):
    """
    Fetch taxonomy information from NCBI for a given accession number.
    
    Args:
        acc_number (str): GenBank accession number.
        
    Returns:
        str: Taxonomy name or error message.
    """
    try:
        print(f"Fetching taxonomy for accession: {acc_number}")
        with Entrez.efetch(db="nucleotide", id=acc_number, rettype="gb", retmode="xml") as handle:
            record = Entrez.read(handle)
        
        taxon = record[0].get("GBSeq_organism", "No taxonomy data found")
        return taxon
    
    except Exception as e:
        return f"Error: {e}"

def process_blast_output(input_file_path):
    """
    Process a single BLAST output file to replace accession numbers with taxonomy names.
    
    Args:
        input_file_path (str): Path to the BLAST output file.
    """
    processed_lines = set()

    # Prepare output file path with timestamp to avoid overwriting
    base_name = os.path.basename(input_file_path).replace("cleaned_results.out", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "/mnt/c/Users/User/downloads/FinalOTUs/Pool1OTUs/blast_results/final_files"
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
    output_file_path = os.path.join(output_dir, f"{base_name}taxonomy_results_{timestamp}.txt")

    with open(input_file_path, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    with open(output_file_path, "w", encoding="utf-8") as outfile:
        for line in lines:
            columns = line.strip().split("\t")

            if len(columns) >= 3:  # Check for minimum columns (OTU ID, Accession, Identity %)
                otu_id = columns[0].strip()
                acc_string = columns[1].strip()
                identity = columns[2].strip()

                acc_number = extract_accession(acc_string)
                if acc_number:
                    print(f"Processing accession: {acc_number}")
                    taxonomy = fetch_taxonomy(acc_number)
                    columns[1] = taxonomy  # Replace accession with taxonomy

                    new_line = "\t".join(columns)
                    if new_line not in processed_lines:
                        outfile.write(new_line + "\n")
                        processed_lines.add(new_line)

                    time.sleep(5)  # Delay to respect NCBI API usage policy

    print(f"Processing complete. Results saved to: {output_file_path}")

if __name__ == "__main__":
    for input_path in input_files:
        process_blast_output(input_path)
