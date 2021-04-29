INpath=$1
SID=$2
Module=$3

Lanemkflow()
{
    INp=$1
    OUp=$2
    cat $INp >> $OUp
    cat>>$OUp<<EOF


CATEGORY="fastqclink.${SID}"
CORES=7
MEMORY=30000
DISK=10
${TransR1s[@]} ${TransR2s[@]} : ${R1s[@]} ${R2s[@]}
    sh $WORKFLOW_DIR/FastqLink.sh $INp

CATEGORY="10xrna.${SID}"
CORES=20
MEMORY=40000
DISK=10
$G10Xpre/outs/web_summary.html : ${TransR1s[@]} ${TransR2s[@]} 
    sh $WORKFLOW_DIR/G10XmRNA.sh $INp

EOF
}

INSf=( $INpath/${SID}_*${Module}.input )
. ${INSf[0]}
WorkSH=$AUT/WorkShell
SampMK=$WorkSH/${SID}_${Module}.mf

if [ -f $SampMK ];then
    rm $SampMK
fi
mkdir -p $WorkSH

#########each lane
for i in ${INSf[@]};do
    . $i
    . $WORKFLOW_DIR/env.Variable
    cp  $i $WorkSH/${SID}_${Module}.input
    Lanemkflow $WorkSH/${SID}_${Module}.input $SampMK
done