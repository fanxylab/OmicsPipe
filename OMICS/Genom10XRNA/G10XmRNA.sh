. $1
. $WORKFLOW_DIR/env.Configure
. $WORKFLOW_DIR/env.Variable

echo "`date +%Y%m%d-%H:%M:%S`: 10XRNA"
mkdir -p $G10Xout

USID=$(IFS=, ; echo "${UIDs[*]}")
cd $G10Xout
$CELLRANGER count --id=$SID \
                   --transcriptome=$GENOME_10XRNA \
                   --fastqs=$RawFQout \
                   --sample=$USID \
