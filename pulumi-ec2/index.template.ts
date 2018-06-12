const aws = require("@pulumi/aws");

let size = "t2.micro"
let ami = "ami-a7d494df"
let group = new aws.ec2.SecurityGroup("simons-testapp-secgrp", {
    ingress: [
        { protocol: "tcp", fromPort: 22, toPort: 22, cidrBlocks: ["0.0.0.0/0"] },
	{ protocol: "tcp", fromPort: 80, toPort: 80, cidrBlocks: ["0.0.0.0/0"] }
    ],
});

let userData =
`#!/bin/sh
echo "Hello, Pulumi!" > index.html
sudo python -m SimpleHTTPServer 80 &`;

function newInstance(i: number) {
    return new aws.ec2.Instance("simons-testapp-www-" + i, {
	instanceType: size,
	securityGroups: [ group.name ],
	ami: ami,
	userData: userData
    })
}

var instances = []
for (var i:number=1; i <= @INSTANCE_COUNT@; i++) { instances.push(i) };

let servers = instances.map(newInstance);

exports.publicIp = servers[0].publicIp;
exports.publicHostName = servers[0].publicDns

