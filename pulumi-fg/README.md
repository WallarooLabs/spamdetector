# Notes

# The below is NOT apples-for-apples, just me flailing around.
I'll try to script a run-through that is apples-for-apples, and run it
in both contexts a couple of times to get less noisy data.


# Some initial thoughts

In terms of the time needed to spin up a running cluster of 'things', including
load balancers, security groups, etc, both approaches are comparable, with
Fargate being a bit slower to provision resources.

We likely need to take the option of 'reactive provisioning' off the
table.

What I'd suggest for now is a two-pronged approach, with Pulumi for setting up
infrastructure (EC2 backend), and an awscli script to just stop/start the
relevant instances.



# Deploying/modifying containers in Fargate:
This setup includes two logical services, one for the initializer worker
and another for all the other workers.

- Fresh deploy /w (1, 5) containers: 7:44"
- Teardown :  9:11"
- Re-deploy after teardown: 9:11'
- Bump service members 2->5:  00:50"
- Bump service members 5->10: 02:55"
- Bump service members 10->0: 03:49"
- Bump service members 0->1:  06:05"
- Bump both services ((0,0) -> (1,1)): 02:11"
- Reduce services ((1,1) -> (0,0)): 08:42"


# Deploying/modifying instances in plain EC2:
This setup includes a list of ec2 instances (t2.micro).

- Fresh deploy of 1 ec2 machine: 0:33"
- Fresh deploy of 4 ec2 machines: 2:42"
- Bump count from 4 -> 8 ec2 machines: 1:53"
- Reduce count from 8 -> 1 ec2 machines: 6:18"
- Bump count from 1 -> 8 ec2 machines: 3:48"
- Bump count from 1 -> 5 BOTCHED, NEEDS REDOING
- Bump count from 5 -> 10: 02:53"
