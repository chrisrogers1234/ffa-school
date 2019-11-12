#!/bin/bash

fail=0 # flag whether the setup was okay

######### Source OPAL environment ##########################

if [[ -z ${OPAL_BUILD_PATH} ]]; then
    echo "ERROR: Failed to find \${OPAL_BUILD_PATH}"
    fail=1
fi

source ${OPAL_BUILD_PATH}/etc/profile.d/opal.sh
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to source opal.sh"
    fail=1
fi

export OPAL_EXE_PATH=${OPAL_BUILD_PATH}/bin/

######### Add scripts directory to python path #############

scripts=`pwd`/scripts
echo "Adding ${scripts} to python path"
if [[ -d ${scripts} ]]; then
    export PYTHONPATH=$PYTHONPATH:${scripts}
else
    echo "ERROR: Could not find ${scripts} directory for \$PYTHONPATH"
    echo "ERROR: 'env.sh' should be sourced from ffa-school root directory"
    fail=1
fi

######### Check environment is okay #############

echo "Checking environment"

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

python3 -c "import config.config_base" >& /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to setup FFA school files. \${PYTHONPATH} is"
    echo "  ${PYTHONPATH}"
    fail=1
fi

echo "" | ${OPAL_EXE_PATH}/opal >& /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to run opal executable, which was expected at"
    echo "       \${OPAL_EXE_PATH}/opal which evaluates as '${OPAL_EXE_PATH}/opal'"
    fail=1
fi

if [ $fail -eq 0 ]; then
    echo "Setup looks okay!"
else
    echo "ERROR: Setup failed"
fi
