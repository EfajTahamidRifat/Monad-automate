#!/usr/bin/env bash
# Minimal setup script.
# Prompts for a private key and writes a config.json file.
set -e
echo "This script will create config.json in the current directory."
read -p "Enter config name (default: default): " CONFNAME
CONFNAME=${CONFNAME:-default}
# prompt securely
stty -echo
printf "Enter private key: "
read PRIVATE_KEY
stty echo
printf "\n"
if [ -z "$PRIVATE_KEY" ]; then
  echo "No private key provided. Exiting."
  exit 1
fi
cat > config.json <<EOF
{
  "name": "$CONFNAME",
  "private_key": "$PRIVATE_KEY"
}
EOF
chmod 600 config.json
echo "config.json created, permissions set to 600."
