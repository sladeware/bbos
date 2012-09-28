# Build time namespace

Reserved namespace. Do not put here any files, unless you know what you are
doing.

All build-scripts are moved and registered within this namespace. For instance
build-script `bb.os.drivers.onewire.slaves.ds18b20_build` for
`bb.os.drivers.onewire.slaves.ds18b20` will be available as
`bb.buildtime.os.drivers.onewire.slaves.ds18b20`.