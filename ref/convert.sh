file=${1:-top10000en-1to200}
soffice --headless --convert-to csv $file.xlsx

# Remove the empty lines & starting comma
cat $file.csv | grep -v ',,' | sed 's/^,//' | sed 's/,$//' | awk ' { if (NR > 1) print $0 } ' > $file.clean

cat $file.clean | awk -F , ' { print $1 } ' > $file-en.txt
cat $file.clean | awk -F , ' { print $2 } ' > $file-ek.txt
