.PHONY: setup-pulumi

setup-pulumi:
	npm i
	pulumi config set cloud:provider aws
	pulumi config set cloud-aws:useFargate true
	pulumi config set --plaintext aws:region us-west-2


