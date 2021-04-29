# OmicsPipe
## Overview

The [OmicsPipe](https://github.com/fanxylab/OmicsPipe.git) pipeline for processing RNA, ATAC and CHIP data.
The pipeline is built on [Makeflow](https://cctools.readthedocs.io/en/latest/makeflow/) workflow system. It will be your good choice with the strong readability,  flexible extensibility and large scale distributed computing. 

## Installation

1. Git clone this pipeline.
    ```bash
    $ git clone https://github.com/fanxylab/OmicsPipe.git
    ```
2. Install [makeflow](http://ccl.cse.nd.edu/software/downloadfiles.php), requires `java` >= 1.8 and `python` >= 3.6.

## Usage
```bash
$ python GetPipeconf.py 
	-i sample.infor.txt 
	-o outdir 
	-q #submit the batch parallel tasks on you cluster
```
The input file format. You can refer to [test](test/sample.infor.txt) file
| Sampleid|Uniqueid|Lane|Rep|Group|Control|Module|Species|Outdir|Fastq|Havadone|
|:-----|:-----|:-----|:-----|:-----|:-----|:-----|:-----|:-----|:-----|:-----|
|TS-Bu-1-H3K27ac|TS-Bu-1-H3K27ac|L4|D1||TS-Bu-1-input|CHIP|mm10|/outpath/|TS-Bu-1-H3K27ac_L4_1.fq.gz,TS-Bu-1-H3K27ac_L4_2.fq.gz||
|TS-Bu-1-H3K9ac|TS-Bu-1-H3K9ac|L1|D1||TS-Bu-1-input|CHIP|mm10|/outpath/|TS-Bu-1-H3K9ac_L1_1.fq.gz,TS-Bu-1-H3K9ac_L1_2.fq.gz||
|TS-Bu-1-input|TS-Bu-1-input|L1|D1|||CHIP|mm10|/outpath/|TS-Bu-1-input_L1_1.fq.gz,TS-Bu-1-input_L1_2.fq.gz||
|ND1-1W-oligo_S3|ND1-1W-oligo_S3|L2|D1|1||ATAC|mm10|/outpath/|ND1-1W-oligo_S3_L002_R1_001.fastq.gz,ND1-1W-oligo_S3_L002_R2_001.fastq.gz||
|U2OS_b3_R1|U2OS-b3-R1_L1_Q801605|L1|D1|1||SS2|hg38|/outpath/|U2OS-b3-R1_L1_Q801605.R1.fastq.gz,U2OS-b3-R1_L1_Q801605.R2.fastq.gz||
|U2OS_b3_R1|U2OS_b3_R1_S4|L2|D1|1||SS2|hg38|/outpath/|U2OS_b3_R1_S4_L002_R1_001.fastq.gz,U2OS_b3_R1_S4_L002_R2_001.fastq.gz||
|mE16-5-10x-GE|mE16-5-10x-GE-1|L002|S13|1||10XRNA|mm10|/outpath/|mE16-5-10x-GE-1_S13_L002_R1_001.fastq.gz,mE16-5-10x-GE-1_S13_L002_R2_001.fastq.gz||
|mE16-5-10x-GE|mE16-5-10x-GE-2|L002|S14|1||10XRNA|mm10|/outpath/|mE16-5-10x-GE-2_S14_L002_R1_001.fastq.gz,mE16-5-10x-GE-2_S14_L002_R2_001.fastq.gz||
```
Sampleid: the sample id. the same id get one output directory.
#Uniqueid: the unique id.
#Lane    : the library lane id. You need to set lane format like L001 and L021 if running 10xgenomics piepline. 
#Rep     : the biological duplication in some modules, such as CHIP and ATAC
#Group   : the sample group.
#Control : The control sample used for  masking background single.
#Module  : the pipeline modules. One sample can analyze multiple modules.
#Species : the reference genome name, including hg38, hg19, mm10 and mm9. You also can assign youself reference by modifying env.Configure file
#Outdir  : the output directory. You can set different path.
#Fastq   : the r1 and r2 fastq file split by comma or semicolon. If you have multiple paired fastq files, you can set multiple lines with different LaneID (column 3).
```