# Man Pages for AWS CLI

TODO(ajf): Convert this into a proper Homebrew Tap.

Many thanks to:

https://tanguy.ortolo.eu/blog/article153/awscli-manpages

Their solution is a bit slow, and it requires modifying installed files.

My version uses monkey-patching to accomplish something similar.

On a 2022 M2 laptop for v2.9.1, this version takes about 3.5 minutes to create about 12k files.

The Python script in `libexec/gen-man-pages.py` does the actual generation; we have a wrapper
`gen-man-pages.bash` that handle some housekeeping around that script.

## Instructions

```console
$ ./gen-man-pages.bash
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

TODO(ajf): How to ensure that our monkey patching is suitable? Possibly allow-list known-compatible
AWS CLI versions?
