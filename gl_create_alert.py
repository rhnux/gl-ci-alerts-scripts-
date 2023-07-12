## Importación de librerías y módulos necesarios
import gitlab
import os
import requests
import markdown
import pymsteams
import re
import sys

## variables de entorno
key_webhook_alert = os.environ["KEY_WEBHOOK_ALERT"]
url_webhook_alert = os.environ["URL_WEBHOOK_ALERT"]
gitlabToken = os.environ["PRIVATE_TOKEN"]
project_id = os.environ["CI_PROJECT_ID"]
project_name = os.environ["CI_PROJECT_NAME"]
project_owner_id = os.environ["CI_PROJECT_OWNER_ID"]
ci_pipa_url = os.environ["CI_PIPELINE_URL"]
pipeline = f"[pipeline]({ci_pipa_url})"
pipeline_id = os.environ["CI_PIPELINE_ID"]
severity_level = os.environ["SEVERITY"]
desc = os.environ["DESC"]
title = os.environ["TITLE"]
tool = os.environ["TOOL"]
report_name = os.environ["REPORT_NAME"]
label = list([os.environ["LABEL"]])
commit_author = os.environ["CI_COMMIT_AUTHOR"]
gitlab_user_id = os.environ["GITLAB_USER_ID"]
commit_m = os.environ["CI_COMMIT_MESSAGE"]
commit_branch = os.environ["CI_COMMIT_BRANCH"]
help_url = os.environ["HELP_URL"]
asvs_level = os.environ["ASVS_LEVEL"]

gl = gitlab.Gitlab(private_token=gitlabToken)
pr = gl.projects.get(id=project_id)
pipa = pr.pipelines.get(id=pipeline_id)
owner_name = gl.users.get(id=project_owner_id).name

print(type(gitlab_user_id))

print(tool)


def get_jobs(tool):
    for job in pipa.jobs.list():
        if tool.lower() in job.name.lower():
            return job
    return None

cjob = get_jobs(tool)
job_link = f"[job]({cjob.web_url})"
report_link = f"[report]({cjob.web_url}/artifacts/browse)"


## Solo para le periodo de uso ==> allow_failure: true
print(cjob.status)
##

if cjob.status == 'success':
    print(f"{tool} JOB STATUS SUCCESS")
    sys.exit(0)

##

url = url_webhook_alert

print(f"Incident Severity: {severity_level}")

payload = {
    "title": f"Security Incident - {title}",
    "service": project_name,
    "severity": severity_level,
    "start_time": "",
    "description": desc,
    "hosts": [project_name],
    "monitoring_tool": tool,
    "stage": "SAST"
    }

headers = {
    "cookie": "galletaXXXX",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key_webhook_alert}"
}

response = requests.request("POST", url, json=payload, headers=headers)

## set issue labels, user ID
print(response.text)
pattern = '\d+'
alert_iid = re.findall(pattern, response.text)
print(alert_iid) 
iid = str(alert_iid[0])

#gl = gitlab.Gitlab(private_token=gitlabToken)
#pr = gl.projects.get(id=project_id)
## labels ASVS Level
if asvs_level == "ASVS LEVEL 3":
    label.append("ASVS::L3")
elif asvs_level == "ASVS LEVEL 2":
    label.append("ASVS::L2")
else:
    asvs_level = "ASVS LEVEL 1"
    label.append("ASVS::L1")
## end labels ASVS Level

print(f"Labels: {label}")

open_issues = pr.issues.list(state='opened', issue_type='incident', labels=label, get_all=False)

print(f"Open Issues: {open_issues}")

body_description = f"""Job Name: {cjob.name} \n
Pipeline: {ci_pipa_url} \n
Job web: {cjob.web_url} \n
Report: {cjob.web_url}/artifacts/browse \n
Commit Message: {commit_m} \n
Commit Branch: {commit_branch} \n
⛑ Support: {help_url} \n
💀 💀 💀 """

md = markdown.Markdown()
body = md.convert(body_description)

if not open_issues:
    print("List is empty")
    issue_incident = pr.issues.list(get_all=False)[0]
    label.append("::DevSecOps")
    issue_incident.notes.create({'body': body})
    issue_incident.labels = label
    issue_incident.assignee_ids = [project_owner_id, gitlab_user_id]
    issue_incident.save()
    issue_incident.pprint()
    ### Teams
    url_teams = "http://url-teams"
    # You must create the connectorca*rd object with the Microsoft Webhook URL
    myTeamsMessage = pymsteams.connectorcard(url_teams)

    # create the section
    myMessageSection = pymsteams.cardsection()

    # Section Title
    myMessageSection.title(f'💀 Security Incident - {title} | {project_name} | Onwer: {owner_name} | {asvs_level}')

    # Section Text
    myMessageSection.text(f"{cjob.name} | Commit Message: {commit_m} | Commit Branch: {commit_branch} | Author: {commit_author} | ⛑ Support: {help_url}")

    # Section Link Button
    myMessageSection.linkButton(buttontext='Report', buttonurl=f'{cjob.web_url}/artifacts/browse')
    myMessageSection.activityText(sactivityText=f'Job: {cjob.web_url}')
    # Add your section to the connector card object before sending
    myTeamsMessage.addSection(myMessageSection)

    myTeamsMessage.color("6c63ff")
    myTeamsMessage.summary(msummary='DevSecOps')
    myTeamsMessage.send()

    last_status_code = myTeamsMessage.last_http_response.status_code

    print(last_status_code)

else:
    print("List issues")
    print(open_issues)
