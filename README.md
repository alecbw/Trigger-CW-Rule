# Trigger-CW-Rule

CloudWatch Rules with an `Event Pattern` Rule type can be invoked with a [PutEvents call](https://docs.aws.amazon.com/cli/latest/reference/events/put-events.html). However, CloudWatch Rules with a `Schedule` Rule type have no programmatic way to invoke a single time.

This script (designed to be used with Alfred or any other CLI productivity tool) manually triggers a single invocation of a `Schedule` type CloudWatch rule. This works because a Disabled CloudWatch rule with a Rate type of `Schedule` will immediately trigger when Enabled.