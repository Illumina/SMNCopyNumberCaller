# SMNCopyNumberCaller

SMNCopyNumberCaller is a tool to call the copy number of full-length SMN1, full-length SMN2, as well as SMN2Δ7–8 (SMN2 with a deletion of Exon7-8) from a whole-genome sequencing (WGS) BAM file. This caller works with standard WGS sequencing depth (>=30X), and is insensitive to various aligners (BWA and Isaac have been tested and no difference was observed). Please refer to our [medRxiv link](https://www.medrxiv.org/content/10.1101/19006635v2) for details about the method.   

SMNCopyNumberCaller is provided under the terms and conditions of the [Apache License Version 2.0](https://github.com/Illumina/SMNCopyNumberCaller/blob/master/LICENSE.txt). It requires several third party packages (numpy, scipy, statsmodels and pysam) provided under other open source licenses, which are listed in [COPYRIGHT.txt](https://github.com/Illumina/SMNCopyNumberCaller/blob/master/COPYRIGHT.txt).  

## Running the program
This Python3 program can be run as follows:
```bash
./smn_caller.py --manifest MANIFEST_FILE \
                --genome [19/37/38] \
                --prefix OUTPUT_FILE_PREFIX \
                --outDir OUTPUT_DIRECTORY \
                --threads NUMBER_THREADS
```
Each line in the manifest file should list the absolute path to an input bam file.    

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
| SMN1_read_support | Number of reads carrying SMN1 allele                           |
| SMN2_read_support | Number of reads carrying SMN2 allele                           |
| SMN1_fraction     | Fraction of reads carrying SMN1 allele                         |
| g27134TG_REF_count| Number of reads carrying g.27134T                              |
| g27134TG_ALT_count| Number of reads carrying g.27134G                              |
| g27134TG_raw      | Raw CN value of g.27134T>G                                     |
| Info              | Filter value for SMN1 CN call                                  |
| Confidence        | Confidence of SMN1 CN calls at SNP sites                       |

