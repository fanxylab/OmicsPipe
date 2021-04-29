. $1
. $WORKFLOW_DIR/env.Configure
. $WORKFLOW_DIR/env.Variable

echo "`date +%Y%m%d-%H:%M:%S`: Fastq link"
mkdir -p $RawFQout

for((j=0; j<${#UIDs[@]}; j++))
do
    ln -sf ${R1s[j]} $RawFQout/${HIDs[j]}_R1_001.fastq.gz
    ln -sf ${R2s[j]} $RawFQout/${HIDs[j]}_R2_001.fastq.gz
done
