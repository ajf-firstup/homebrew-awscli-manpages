#!/bin/bash

aws_path=$(which aws)

# Find the interpreter that the current `aws` CLI binary is using.
aws_python=$(head -1 "$aws_path")

# Remove the leading "#!".
aws_python="/${aws_python#*/}"

# Get the version string. The full output looks like:
#   aws-cli/2.9.12 Python/3.11.1 Darwin/22.2.0 source/arm64 prompt/off
aws_version=$("$aws_path" --version)
aws_version="${aws_version#*aws-cli/}"
aws_version="${aws_version%% *}"

mkdir -p "v$aws_version"
cd "v$aws_version"

man1aws_dir="$PWD"

echo "Building man pages." > /dev/stderr
"$aws_python" ../libexec/gen-man-pages.py

echo
echo "Linking man pages." > /dev/stderr
cd /opt/homebrew/share/man
rm -f man1aws
ln -s "$man1aws_dir" man1aws

exit 0
