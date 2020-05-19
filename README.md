# SMNCopyNumberCaller

SMNCopyNumberCaller is a tool to call the copy number of full-length SMN1, full-length SMN2, as well as SMN2Δ7–8 (SMN2 with a deletion of Exon7-8) from a whole-genome sequencing (WGS) BAM file. This caller works with standard WGS sequencing depth (>=30X), and is insensitive to various aligners (BWA and Isaac have been tested and no difference was observed). Please refer to our [paper](https://www.nature.com/articles/s41436-020-0754-0) for details about the method.   

Chen X, Sanchis-Juan A, French CE, et al. Spinal muscular atrophy diagnosis and carrier screening from genome sequencing data. Genet Med. February 2020:1-9. doi:10.1038/s41436-020-0754-0

SMNCopyNumberCaller is provided under the terms and conditions of the [Apache License Version 2.0](https://github.com/Illumina/SMNCopyNumberCaller/blob/master/LICENSE.txt). It requires several third party packages (numpy, scipy, statsmodels and pysam) provided under other open source licenses, which are listed in [COPYRIGHT.txt](https://github.com/Illumina/SMNCopyNumberCaller/blob/master/COPYRIGHT.txt).  

## Running the program
This Python3 program can be run as follows:
```bash
smn_caller.py --manifest MANIFEST_FILE \
              --genome [19/37/38] \
              --prefix OUTPUT_FILE_PREFIX \
              --outDir OUTPUT_DIRECTORY \
              --threads NUMBER_THREADS
```
Each line in the manifest file should list the absolute path to an input BAM/CRAM file.
For CRAM input, it’s suggested to provide the path to the reference fasta file with --reference in the command. 

## Interpreting the output
The program produces a .tsv file in the directory specified by --outDir.   
The fields are explained below: 

| Fields in tsv     | Explanation                                                    | 
|:------------------|:---------------------------------------------------------------|
| Sample            | Sample name                                                    |
| isSMA             | Whether sample is called as SMA (zero copy of SMN1)            |
| isCarrier         | Whether sample is called as SMA carrier (one copy of SMN1)     |
| SMN1_CN           | Copy number of SMN1 (None means no-call)                       |
| SMN2_CN           | Copy number of SMN2                                            |
| SMN2delta7-8_CN   | Copy number of SMN2Δ7–8 (deletion of Exon7-8)                  |
| Total_CN_raw      | Raw normalized depth of total SMN                              |
| Full_length_CN_raw| Raw normalized depth of full-length SMN                        |
| g.27134T>G_CN     | CN of g.27134T>G, SNP associated with 2+0 silent carrier       |
| SMN1_CN_raw       | Raw SMN1 CN values at SNP sites that differ btn SMN1/SMN2      |

A .json file is also produced that contains more information for debugging purpose.   

| Fields in json    | Explanation                                                    | 
|:------------------|:---------------------------------------------------------------|
| Coverage_MAD      | Median absolute deviation of depth, measure of sample quality  |
| Median_depth      | Sample median depth                                            |
| SMN1_read_support | Number of reads carrying SMN1 allele                           |
| SMN2_read_support | Number of reads carrying SMN2 allele                           |
| SMN1_fraction     | Fraction of reads carrying SMN1 allele                         |
| g27134TG_REF_count| Number of reads carrying g.27134T                              |
| g27134TG_ALT_count| Number of reads carrying g.27134G                              |
| g27134TG_raw      | Raw CN value of g.27134T>G                                     |
| Info              | Filter value for SMN1 CN call                                  |
| Confidence        | Confidence of SMN1 CN calls at SNP sites                       |
  
## Visualizing the results
A visualization tool for the SMNCopyNumberCaller result takes the .json file produced by SMNCopyNumberCaller and can be run as follows:
```bash
smn_charts.py -s SMN_JSON_FILE \
              -o OUTPUT_DIRECTORY
```
A .pdf file is produced for each sample in OUTPUT_DIRECTORY, containing four plots. The first two plots show where the raw depth values (vertical lines) stand against the population samples for the total SMN CN and the full length SMN CN. The third plot shows the raw CN values for SMN1 and SMN2 at 8 sites that we use to determine the consensus. #13 is the splice variant site. The last plot shows the raw read counts for SMN1 and SMN2 on the right y axis and the left y axis is a rough calculation of CN: #reads divided by the median haploid depth. An example can be found [here](https://github.com/Illumina/SMNCopyNumberCaller/blob/master/charts/data/smn_HG03458.pdf).    

