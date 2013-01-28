#!/bin/bash

THIRD_PARTY_DIR_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../third_party"
LATEST_RELEASE_VERSION='0.7.10b'
PROCESSOR_ARCH='i386' # AMD64
TARGET_URL=''

# Check that fritzing is presented.
if test ! -e third_party/fritzing; then
  echo "Fritzing not present. Fetching fritzing-$LATEST_RELEASE_VERSION..."
  if [ "$PROCESSOR_ARCH" == "i386" ]; then
    TARGET_URL="http://fritzing.org/download/$LATEST_RELEASE_VERSION/linux-32bit/fritzing-$LATEST_RELEASE_VERSION.linux.i386.tar.bz2"
  elif [ "$PROCESSOR_ARCH" == "AMD64" ]; then
    curl http://fritzing.org/download/$LATEST_RELEASE_VERSION/linux-64bit/fritzing-$LATEST_RELEASE_VERSION.linux.AMD64.tar.bz2 | tar jx
  else
    echo "Unknown processor arch: $PROCESSOR_ARCH"
    exit 1
  fi
  curl -L $TARGET_URL | tar jx -C $THIRD_PARTY_DIR_PATH
  mv $THIRD_PARTY_DIR_PATH/fritzing-$LATEST_RELEASE_VERSION.linux.$PROCESSOR_ARCH $THIRD_PARTY_DIR_PATH/fritzing
fi

exit 0