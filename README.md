# Buildbot config for winepak
This repo contains the Buildbot config for building winepak applications and runtimes found in the winepak organization. It's loosely based off the Flathub's buildbot pre-repomanager update.

Pushes to an applications master branch will auto build applications when it checks in on a timer. Buildbot will also monitor for GitHub changes via a web hook. You can also force a build if you are an admin on our GitHub organization or have admin credentials.

## master.cfg
### Configs
First Buildbot searches for a `config.json` file with a number of configuration settings needed to run. This file is generated via our [ansible-playbook](https://github.com/winepak/ansible-playbook) but an example is provided in this repo as `config.json.sample`.

### Authentication
This section contains the number of ways to authenticate to Buildbot. We first attempt to authenticate with simple username and password, however, if GitHub authentication is an option we do that. Then GitLab is an option, but GitHub and GitLab shouldn't be used together

### Workers
Workers are loaded from the `workers.json` which is another file generated via our [ansible-playbook](https://github.com/winepak/ansible-playbook) but an example is provided in this repo as `workers.json.sample`.

We set a password for the worker to authenticate with and also provide what arches this worker can build, among other settings.

We also keep track of what workers are available so we know what architectures we can build and on how many machines.

### Change Source
We don't really use the change_source config, instead we use the change_hook_dialects in the www config. This listens for request sent from GitHub or GitLab. Currently only GitHub can be used.

A number of information is gathered like branch, repository, project, category, author, comments, etc.. which are all used to filter builds and start builds.

### Properties Step
A special Buildbot step for setting-up all the properties needed to build a manifest.

### Schedulers
Schedulers start build jobs. Normally Schedulers look for change_sources, however, we look for GitHub change events on the entire winepak organization via the GitHub webhook api we setup under "Change Source".

The `schedulers.AnyBranchScheduler` type will look for any build event and starts the `build-master` which distributes builds and starts x86_64, i386, arch, aarch64, etc.. builds (if available).

The `schedulers.Triggerable` type with trigger later in the config when we need to determine which build platform to target.

The `schedulers.ForceScheduler` can force start a build in the buildbot web interface. You will need to authenticate first to access this build option.

# Build Factories
These are the steps to build a manifest.

# Builders
These are the machines that do the building. We create builders for each architecture automatically based on `workers.json`. `build-master` controls the flow of builds and delegates work to the the arch specific builders (e.g. `build-x86_64`).
