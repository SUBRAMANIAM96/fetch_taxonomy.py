# Fetch Taxonomy from NCBI for BLAST Output

This Python script fetches taxonomy information from the NCBI database for accession numbers extracted from BLAST output files.

---

## Overview

- Parses BLAST output files to extract GenBank accession numbers.  
- Queries NCBI Entrez database to retrieve taxonomy (organism name) for each accession.  
- Replaces accession numbers in the output with the corresponding taxonomy names.  
- Saves results with timestamped filenames to avoid overwriting.  
- Includes rate limiting (5 seconds delay) to comply with NCBI API usage policies.

---

## Requirements

- Python 3.x  
- [Biopython](https://biopython.org/) package installed:  
  ```bash
  pip install biopython

Usage Instructions

    Edit the script

        Set your email in the script at the line:

    Entrez.email = "subramanyamvkumar@gmail.com"

    Update the input_files list with paths to your BLAST output files.

Run the script

    python fetch_taxonomy.py

    Output

        Processed files will be saved in:
        /mnt/c/Users/User/downloads/FinalOTUs/Pool1OTUs/blast_results/final_files/

        Output filenames include timestamps to ensure uniqueness.

Important Notes

    Make sure you have internet connectivity as the script queries the NCBI servers.

    The script adds a 5-second pause between queries to avoid hitting NCBI rate limits.

    Input files should be tab-delimited with accession numbers in the second column.
