// Copyright 2017, Pulumi Corporation.  All rights reserved.

import * as pulumi from "@pulumi/pulumi";
import * as cloud from "@pulumi/cloud";

let workers = new cloud.Service("ts-app-workers", {
    containers: {
        worker: {
            build: "./testapp",
            memory: 100,
            ports: [{ port: 80, external: true }]
	}
    },
    replicas: @INSTANCE_COUNT@
});

export let workerURL = workers.endpoints.apply(e => e["worker"][80].hostname);
