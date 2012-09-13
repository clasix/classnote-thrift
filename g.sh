files=$(ls ./thrift | grep '.thrift$')
for file in $files
do
    thrift --gen py  -out gen-py/. thrift/$file
    thrift --gen cocoa -out gen-cocoa/. thrift/$file
    echo "$file"
done
