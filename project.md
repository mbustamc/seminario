# Instrucciones proyecto


export PROJECT_ID=PROJECT_ID

gcloud config set project $PROJECT_ID

gcloud auth login --update-adc



sudo apt-get update
sudo apt-get install python3-venv -y
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt



--- 
NO VA LO SIGUIENTE

gsutil cp gs://$PROJECT_ID-src/tabs-spaces-voting.zip $HOME

unzip -d tabs-spaces-voting $HOME/tabs-spaces-voting.zip

mkdir -p $HOME/tabs-spaces-voting/.vscode
cat <<EOF > $HOME/tabs-spaces-voting/.vscode/settings.json
{
    "cloudcode.duetAI.project": "$PROJECT_ID",
    "cloudcode.project": "$PROJECT_ID",
    "terminal.integrated.env.linux": {
        "PROJECT_ID": "$PROJECT_ID"
    },
    "workbench.colorTheme": "Default Dark+",
}
EOF

---
