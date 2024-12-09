#!/bin/bash

# Extract the current ngrok URL
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url' | sed 's|https://||g')
echo "Starting Drone with ngrok URL: $NGROK_URL"

# Stop and remove existing containers
docker stop drone runner >/dev/null 2>&1
docker rm drone runner >/dev/null 2>&1

# Start Drone server
docker run \
  --volume=/var/lib/drone:/data \
  --env=DRONE_GITHUB_CLIENT_ID=Ov23liTlJpNnTrPHRbmW \
  --env=DRONE_GITHUB_CLIENT_SECRET=54b58f8f9d68e1de38afd865c3a8bc2e5ba637a1 \
  --env=DRONE_RPC_SECRET=2e264099bfd0f48f6feb1ce71fb42f08 \
  --env=DRONE_SERVER_HOST=$NGROK_URL \
  --env=DRONE_SERVER_PROTO=https \
  --env=DRONE_USER_CREATE=username:routemypacket,admin:true \
  --publish=80:80 \
  --publish=443:443 \
  --restart=always \
  --detach=true \
  --name=drone \
  drone/drone:2

# Start Drone runner
docker run --detach \
  --volume=/var/run/docker.sock:/var/run/docker.sock \
  --env=DRONE_RPC_PROTO=https \
  --env=DRONE_RPC_HOST=$NGROK_URL \
  --env=DRONE_RPC_SECRET=2e264099bfd0f48f6feb1ce71fb42f08 \
  --env=DRONE_RUNNER_CAPACITY=2 \
  --env=DRONE_RUNNER_NAME=runner \
  --publish=3000:3000 \
  --restart=always \
  --name=runner \
  drone/drone-runner-docker:1

echo "Drone server and runner started successfully!"