// Copyright 2017, Pulumi Corporation.  All rights reserved.
const aws = require("@pulumi/aws");

let size = "t2.micro"
let ami = "ami-0a521172"

let group = new aws.ec2.SecurityGroup("spamdetector-secgrp", {
    ingress: [
        { protocol: "tcp", fromPort: 22,
	  toPort: 22, cidrBlocks: ["0.0.0.0/0"] },
	{ protocol: "tcp", fromPort: 80,
	  toPort: 80, cidrBlocks: ["0.0.0.0/0"] }
    ],
});

let keyPair = new aws.ec2.KeyPair("spamdetector-key", {
    publicKey: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCvWfaxH0HFtmM6xypx9MqoswEpSVMlB7ZIgBcT1Wu+3PetcawbP+Mpzwi3ioT68srLVKBVq+VXOTfNJWKDqUvEnj5lrERGf8UlMj+uVXEPvXgVT0fyFUDxJGG2O5J0G1s1TO/nhxw0okR4OBN8PUm0LVPsSdDrSOXQvHD20zpu/HBq0X5X9YWmSwDqJ7aKntUIWRUw26U0df7WSPobnrNuVLYedvSi2ru5tXC8gpSvMoJalw5gwAR/sGRBacelnpT3faE5bdpsjQTxFD7gaaqwKwodPKjQm1AJKZHgW2Qh8wuQQ0JDGe5TpiM1t1/mukMYarKz0XnY15D5qEQ+iQ4r"})

let startWallaroo =
`#!/bin/sh
nc -k -p 5556 -l 127.0.0.1 > sink.log &
sudo python -m SimpleHTTPServer 80 &`;

function newInstance(n: string) {
    return new aws.ec2.Instance("spamdetector-" + n, {
	instanceType: size,
	securityGroups: [ group.name ],
	ami: ami,
	keyName: keyPair.keyName,
	userData: startWallaroo
    })
}

let chatServer = newInstance("chatServer")
// let wallarooProcessors = ["w1","w2","w3"].map(newInstance);
let wallarooProcessors = ["w1"].map(newInstance);


function getInstanceInfo(i: any) {
    return { "ip" : i.publicIp,
	     "hostname" : i.publicDns
	   }
}

exports.wallarooWorkers = wallarooProcessors.map(getInstanceInfo);
exports.chatServer = getInstanceInfo(chatServer);
