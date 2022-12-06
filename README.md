# Man Pages for AWS CLI

TODO(ajf): Convert this into a proper Homebrew Tap.

Many thanks to:

https://tanguy.ortolo.eu/blog/article153/awscli-manpages

Their solution is a bit slow, and it requires modifying installed files.

My version uses monkey-patching to accomplish something similar.

On a 2022 M2 laptop for v2.9.1, this version takes about 3.5 minutes to create about 12k files.

You can regenerate them with `bin/gen-man-pages.py`.

## Instructions

Find the version of AWS CLI you're running:

```console
$ aws --version
aws-cli/2.9.1 Python/3.11.0 Darwin/22.1.0 source/arm64 prompt/off
```

Clone this repo and take note of where it ended up:

```console
$ cd

$ mkdir -p Source

$ cd Source

$ git clone https://github.com/ajf-firstup/homebrew-awscli-manpages

$ cd homebrew-awscli-manpages

$ AWSCLI_MANPAGES_DIR="$PWD"
```

Find the matching man page sources and symlink them into `/opt/homebrew/share/man/man1aws`:

```console
$ cd /opt/homebrew/share/man/man1aws

$ ln -s "$AWSCLI_MANPAGES_DIR/v2.9.1" man1aws
```

Then modify your `MANSECT` environment variable (or use the `-S` argument to `man`) to include the
`1aws` section:

```console
$ man -S 1aws aws-elbv2
ELBV2(1aws)                         awscli                         ELBV2(1aws)

NAME
       elbv2 -

DESCRIPTION
       A load balancer distributes incoming traffic across targets, such as
       your EC2 instances. This enables you to increase the availability of
       your application. The load balancer also monitors the health of ...

...

2.9.1                                                              ELBV2(1aws)

```

TODO(ajf): Maybe figure out how to invoke `makewhatis` to re-index the new files?

TODO(ajf): Maybe write a wrapper to automatically detect the AWS CLI version and do all the magic
from that point forward?

TODO(ajf): How to ensure that our monkey patching is suitable? Possibly allow-list known-compatible
AWS CLI versions?
