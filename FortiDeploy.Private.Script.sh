# Fortinet Technologies.
# Sample Script on using the REST API of the Private FortiCloud
# pre-set variables
url=https://172.16.94.108/api/v1

# check parameters
if [ ! $# == 2 ]; then
  echo "Usage: $0 [backup|restore] <filename>"
  exit
fi

# logon
echo Logging on
curl $url/auth -H "Content-Type: application/json" -X POST -d '{"username":"admin","password":"fortinet"}' -k -o out1.txt -s
token=`cut -d"," -f3 out1.txt | cut -d":" -f2 | sed 's/"//g'`

if [ "$1" == "backup" ]; then
	# To Download:
	echo Downloading
	curl $url/backup -k -X GET -H "Authorization: Bearer $token" -o out2.txt -s
	content=`cut -d"," -f3 out2.txt | cut -d":" -f2 | sed 's/"//g'`

	echo Processing
	# output file is in rules.config.backup.txt
	echo $content | base64 --decode -i > $2
	
	echo Sample of $2:
	head $2

elif [ "$1" == "restore" ]; then
	# To Upload:
	echo Processing
	strUpload=`base64 $2`
	
	echo Uploading
	curl $url/restore -k -H "Content-Type: application/json" -H "Authorization: Bearer $token" -X POST -d '{"appendMode":1,"content":"$strUpload"}' 

else
	echo "wrong method"
fi

# logout
echo Logging out
curl $url/logout -H "Content-Type: application/json" -X POST -k -o out1.txt -s

echo Done
