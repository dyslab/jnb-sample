##
#
# Decode a base64-encoded text file and then save as another text file. 
# 
# PowerShell version: 5+
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File b64decoder.ps1 -InputFile example.txt
#
##
param(
    [string]$InputFile = "example.txt"
)

# Check PowerShell version
if ($PSVersionTable.PSVersion.Major -lt 5)
{
	Write-Warning -Message "This script requires PowerShell 5+ to run, but you're currently running PowerShell $(if (Test-Path Variable:\PSVersionTable) {$PSVersionTable.PSVersion} else {"1.0"})!"
	Exit 1
}

# Check if the input file exists
if (-not (Test-Path -Path $InputFile -PathType Leaf)) {
    Write-Host $InputFile -ForegroundColor Red -NoNewline
    Write-Host " does not exist."
    Exit 1
}

# Generate output file name
$OutputFile = $InputFile -replace '^(?<path>.*[\/\\]+)?(?<name>.*)\.(?<ext>.\w+)$', '${path}${name}_decoded.${ext}' # output: "./example_decoded.txt"
<#
# For debugging (regular expression)
$input_file -match "^(?<path>.*[\/\\]+)?(?<name>.*)\.(?<ext>.\w+)$"
Write-Host $output_file -ForegroundColor Red
Write-Output $Matches
Exit 1
#>

# Decode and save
$InputFileContent = Get-Content $InputFile
$OutputFileContentBytes = [convert]::FromBase64String($InputFileContent)
$OutputFileContent =[System.Text.Encoding]::UTF8.GetString($OutputFileContentBytes)
Out-File -FilePath $OutputFile -InputObject $OutputFileContent

Write-Host $InputFile -NoNewline -ForegroundColor Green
Write-Host " decoded to " -NoNewline
Write-Host $OutputFile -ForegroundColor Blue
