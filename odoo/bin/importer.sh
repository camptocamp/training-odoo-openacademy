#!/bin/sh
# This script can be use to import big csv file
# He splits the csv file and run multiple anthem (one by processor)
# WARNING: You can't use it if the imported model as foreign key on itself

# Usage: importer.sh anthem_command csv_file_path
set -e

PROC=`nproc --all`

ANTHEM_ARG=$1
if [ -z $1 ]; then
    echo "Please provide a file path and the anthem arg"
    exit 1;
fi


DATA_PATH=$2
if [ -z $2 ] || [ ! -e $DATA_PATH ]; then
    echo "Unable to find the data file $2";
    exit 1;
fi;

IMPORTER_DIR=/var/tmp/importer
SPLIT_DIR=${IMPORTER_DIR}/`basename $DATA_PATH`_split
mkdir -p $SPLIT_DIR

cd ${IMPORTER_DIR}

# Split the csv file in $PROC files
CSV_HEADER=$(sed 1q "$DATA_PATH")
split -d -n l/$PROC ${DATA_PATH} ${SPLIT_DIR}/
# Add missing CSV header
for file in `find ${SPLIT_DIR} -type f`; do
    # Split in smaller chunks of 500 maximum
    SUB_SPLIT_DIR=${file}_split
    mkdir $SUB_SPLIT_DIR
    split -d -l 500 ${file} ${SUB_SPLIT_DIR}/
    rm $file
    for sub_file in `find ${file}_split -type f`; do
        if [ $CSV_HEADER != "`sed 1q $sub_file`" ]; then
            sed -i "1i\\$CSV_HEADER" $sub_file;
        fi
    done
done

# Import splitted files with parallel
START_TIME=$(date +%s)
ls -1 $SPLIT_DIR | parallel -j $PROC DATA_DIR=${SPLIT_DIR}/{} anthem $ANTHEM_ARG --no-xmlrpc

echo "Parallel total loading data: $(($(date +%s) - $START_TIME))s"


if [ $? -eq 0 ]; then
    rm ${IMPORTER_DIR} -r
fi
