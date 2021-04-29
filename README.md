# OmicsPipe
## Overview

The [OmicsPipe](https://github.com/fanxylab/OmicsPipe.git) pipeline for processing RNA, ATAC and CHIP data.
The pipeline is built on [Makeflow](https://cctools.readthedocs.io/en/latest/makeflow/) workflow system. It will be your good choice with the excellent features of strong readability, flexible extensibility and large scale distributed computing. 

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
|CHIPs1case|CHIPs1case|L4|D1||CHIPscontrol|CHIP|mm10|/outpath/|CHIPs1case_L4_1.fq.gz,CHIPs1case_L4_2.fq.gz||
|CHIPs2case|CHIPs2case|L1|D1||CHIPscontrol|CHIP|mm10|/outpath/|CHIPs2case_L1_1.fq.gz,CHIPs2case_L1_2.fq.gz||
|CHIPscontrol|CHIPscontrol|L1|D1|||CHIP|mm10|/outpath/|CHIPscontrol_L1_1.fq.gz,CHIPscontrol_L1_2.fq.gz||
|ATACs1|ATACs1|L2|D1|1||ATAC|mm10|/outpath/|ATACs1_R1.fastq.gz,ATACs1_R2.fastq.gz||
|RNAs1|RNAs11|L1|D1|1||SS2|hg38|/outpath/|RNAs11.R1.fastq.gz,RNAs11.R2.fastq.gz||
|RNAs1|RNAs12|L2|D1|1||SS2|hg38|/outpath/|RNAs12_R1.fastq.gz,RNAs12_R2.fastq.gz||
|G10XRNA1|G10XRNA1-1|L002|S13|1||10XRNA|mm10|/outpath/|G10XRNA1-1_S13_R1.fastq.gz,G10XRNA1-1_S13_R2.fastq.gz||
|G10XRNA1|G10XRNA1-2|L002|S14|1||10XRNA|mm10|/outpath/|G10XRNA1-2_S14_R1.fastq.gz,G10XRNA1-2_S14_R2.fastq.gz||
```
#Sampleid: the sample id. the same id get one output directory.
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
