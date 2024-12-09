#!/bin/bash

NEW_URL=$(curl --silent http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url' | sed 's|https://||g')

if [ -z "$NEW_URL" ]; then
    echo "Ngrok URL not found. Is Ngrok running?"
    exit 1
fi

echo "Updating Drone with new Ngrok URL: $NEW_URL"

docker stop drone drone-runner
docker rm drone drone-runner

docker run \
  --volume=/var/lib/drone:/data \
  --env=DRONE_GITHUB_CLIENT_ID=Ov23liTlJpNnTrPHRbmW \
  --env=DRONE_GITHUB_CLIENT_SECRET=54b58f8f9d68e1de38afd865c3a8bc2e5ba637a1 \
  --env=DRONE_RPC_SECRET=2e264099bfd0f48f6feb1ce71fb42f08 \
  --env=DRONE_SERVER_HOST="$NEW_URL" \
  --env=DRONE_SERVER_PROTO=https \
  --env=DRONE_USER_CREATE=username:routemypacket,admin:true \
  --publish=80:80 \
  --publish=443:443 \
  --restart=always \
  --detach=true \
  --name=drone \
  drone/drone:2

docker run \
  --volume=/var/run/docker.sock:/var/run/docker.sock \
  --env=DRONE_RPC_PROTO=https \
  --env=DRONE_RPC_HOST="$NEW_URL" \
  --env=DRONE_RPC_SECRET=2e264099bfd0f48f6feb1ce71fb42f08 \
  --env=DRONE_RUNNER_CAPACITY=2 \
  --env=DRONE_RUNNER_NAME=runner \
  --restart=always \
  --detach=true \
  --name=drone-runner \
  drone/drone-runner-docker:1


curl -X PATCH \
  -H "Authorization: token <your-github-token>" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/routemypacket/network-ci_cd/settings/hooks/516620297 \
  -d '{"config": {"url": "https://$NEW_URL/hook"}}'