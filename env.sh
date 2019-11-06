source ~/OPAL/env.sh
scripts=`pwd`/scripts
echo "Adding ${scripts} to python path"
export PYTHONPATH=$PYTHONPATH:${scripts}
