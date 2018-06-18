import pulumi
from pulumi_aws import ec2

ami = "ami-e308459b"
instance_type = "t2.micro"
wallaroo_instance_count = 1
chat_instance_count = 1

group = ec2.SecurityGroup("spamdetector-secgrp",
    ingress=[{ "protocol": "tcp", "fromPort": 22,
	       "toPort": 22, "cidrBlocks": ["0.0.0.0/0"] },
	     { "protocol": "tcp", "fromPort": 80,
	       "toPort": 80, "cidrBlocks": ["0.0.0.0/0"] },
	     { "protocol": "tcp", "fromPort": 5000,
	       "toPort": 5999, "cidrBlocks": ["0.0.0.0/0"] }
    ],
    egress=[{ "protocol": "tcp", "fromPort": 0,
	      "toPort": 65535, "cidrBlocks": ["0.0.0.0/0"] }
    ])

key_pair = ec2.KeyPair("spamdetector-key",
                       public_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCvWfaxH0HFtmM6xypx9MqoswEpSVMlB7ZIgBcT1Wu+3PetcawbP+Mpzwi3ioT68srLVKBVq+VXOTfNJWKDqUvEnj5lrERGf8UlMj+uVXEPvXgVT0fyFUDxJGG2O5J0G1s1TO/nhxw0okR4OBN8PUm0LVPsSdDrSOXQvHD20zpu/HBq0X5X9YWmSwDqJ7aKntUIWRUw26U0df7WSPobnrNuVLYedvSi2ru5tXC8gpSvMoJalw5gwAR/sGRBacelnpT3faE5bdpsjQTxFD7gaaqwKwodPKjQm1AJKZHgW2Qh8wuQQ0JDGe5TpiM1t1/mukMYarKz0XnY15D5qEQ+iQ4r")

wallaroo_instances = []
for i in range(0,wallaroo_instance_count):
    wallaroo_instances.append(ec2.Instance("spamdetector-%s"%(i+1,),
                                           instance_type=instance_type,
                                           security_groups=[group.name],
                                           ami=ami,
                                           key_name=key_pair.key_name))
chat_instance_count = 1
chat_instances = []
for i in range(0,chat_instance_count):
    chat_instances.append(ec2.Instance("chatserver-%s"%(i+1,),
                                       instance_type=instance_type,
                                       security_groups=[group.name],
                                       ami=ami,
                                       key_name=key_pair.key_name))

pulumi.output('chat_hostnames', [ s.public_dns for s in chat_instances ])
pulumi.output('wallaroo_hostnames', [ s.public_dns for s in wallaroo_instances ])
