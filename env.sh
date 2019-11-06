#!/bin/bash
scripts=`pwd`/scripts
echo "Adding ${scripts} to python path"
export PYTHONPATH=$PYTHONPATH:${scripts}

######### Check environment is okay #############
fail=0

python3 --version >& /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to find python3"
    fail=1
fi


module_list=(numpy scipy matplotlib xboa)
for module in ${module_list[*]}
do
    python3 -c "import ${module}" >& /dev/null
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to import ${module}"
        fail=1
    fi
done

python3 -c "import config.config_base"
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to setup FFA school files. \${PYTHONPATH} is"
    echo "  ${PYTHONPATH}"
    fail=1
fi

echo "" | ${OPAL_EXE_PATH}/opal >& /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to run opal executable, which was expected at \${OPAL_EXE_PATH}/opal"
    fail=1
fi

if [ $fail -eq 0 ]; then
    echo "Setup looks okay!"
else
    echo "ERROR: Setup failed"
fi
