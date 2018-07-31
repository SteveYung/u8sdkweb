
strA=`ps aux | grep python`
strB="packTask.py"
if [[ $strA =~ $strB ]]
then
  echo `date +%Y-%m-%d,%H:%M:%S`' : yes'
else
  echo `date +%Y-%m-%d,%H:%M:%S`' : no'
  python /mnt/hgfs/U8/U8SDKTool-Win-lanmao/webscripts/packTask.py >>/mnt/hgfs/U8/U8SDKTool-Win-lanmao/webscripts/static/u8sdklog/api.log
fi