
todo: put your explanation here

1. Singleton

The Singleton pattern could make sure that only a single instance of the rule enigne class exists. Doing so, it could be avoided to accidentally have multiple rule engine objects that could interfere each other when checking on rules and applying actions.

2. Memento

Possibly an alternative to storing light configurations: We could save the state of a light/group/scene in a memento object and re-apply it later to restore a configuration. As an example, a user could maybe want to restore a setting back to a configuration that was once used in the past, earlier in time. Through a momento objcet the user could restore that configuration.