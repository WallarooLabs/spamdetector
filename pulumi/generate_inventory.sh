#1/bin/sh
STACK=$(pulumi stack output | tail -n+3)
CHAT_SERVER=$(echo "$STACK" | grep chat \
		  | awk '{print $2}' | jq '.[]' \
		  | head -n1 \
		  | xargs -n1 echo)
WALLAROO_SERVERS=$(echo "$STACK" | grep wallaroo \
		       | awk '{print $2}' | jq '.[]' \
		       | xargs -n1 echo)

echo "[chat_server]"
for s in "$CHAT_SERVER"; do echo "$s ansible_user=ubuntu"; done


echo "[wallaroo_workers]"
for s in "$WALLAROO_SERVERS"; do echo "$s ansible_user=ubuntu"; done
