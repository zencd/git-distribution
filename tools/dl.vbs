'// Download a file from URL

Set args = WScript.Arguments
 
Url = args.Item(0)
targetFile = args.Item(1)
dim xHttp: Set xHttp = createobject("Microsoft.XMLHTTP")
dim bStrm: Set bStrm = createobject("Adodb.Stream")
xHttp.Open "GET", Url, False
xHttp.Send
 
with bStrm
    .type = 1 '//binary
    .open
    .write xHttp.responseBody
    .savetofile targetFile, 2 '//overwrite
end with
