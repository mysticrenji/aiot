$AzureDevOpsPAT = ""
$OrganizationName = ""
$Project = "MLOps-ImageClassification"

$AzureDevOpsAuthenicationHeader = @{Authorization = 'Basic ' + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$($AzureDevOpsPAT)")) }

$UriOrga = "https://dev.azure.com/$($OrganizationName)/$($Project)/"
$uriAccount = $UriOrga + "_apis/build/builds?api-version=6.0"


Write-Host "Calling Build Pipeline from Azure Function"
$body = '
{ 
        "definition": {
            "id": 23
        } 
}
'
$bodyJson=$body | ConvertFrom-Json
Write-Output $bodyJson
$bodyString=$bodyJson | ConvertTo-Json -Depth 100
Write-Output $bodyString


Invoke-RestMethod -Uri $uriAccount -Method post -Headers $AzureDevOpsAuthenicationHeader -ContentType application/json -Body $bodyString