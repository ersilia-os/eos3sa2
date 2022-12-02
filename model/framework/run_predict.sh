ABSOLUTE_PATH=$(pwd)
cd $1/code; python main.py $ABSOLUTE_PATH/$2 $ABSOLUTE_PATH/$3; cd ..
