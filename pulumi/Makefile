.PHONY: update setup-pulumi

update:
	pulumi update --yes --non-interactive

setup-pulumi:
	pip install -r requirements.txt
	pulumi config set cloud:provider aws
	pulumi config set cloud-aws:useFargate true
	pulumi config set --plaintext aws:region us-west-2


