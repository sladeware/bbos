# BB Tools

Tools:

* *builder*
* *uploader*
* *toolchain\_manager*
* *compiler\_manager*
* *loader\_manager*

## Instructions

An _instruction_ specifies rules that will be used by tool in order to process
the object. The object can be represented by a class or an instance. Different
instructions are used by different tools. The instructions meaning is heavely
depends on the system state.

(see _build-script_ and _load-script_).

## Builder

Build system is the key component of BB platform.
The builder is the heart of build system. It reads instructions from
build-scripts and does appropriate actions. The state of BB that represents
builder activity is `bb.STAGE_BUILD_TIME` (see also `bb.is_build_time_stage()`).

All the instructions lives in _build-scripts_.

### Build-script

The _build-script_ is a container of build instructions read by builder.

All the build-scripts ends with _\_build.py_, except of main application build
script, which has name *build.py* and only one per application. This file is the
entry point for the builder to your application.

Once the build process was started, the system will switch to the new state
`bb.BUILDTIME`. Builder will start to import all the build files and store them under
the reserved namespace `bb.buildtime`. Builder stores build scripts in a special
way. For example build-script for the BB application _bb.application\_build.py_
will be stored as `bb.buildtime.application`.

### Targets

The purpose of builder is to build all the _targets_ inside of
application. There is only one type of targets: _image_. Note, builder selects
targets by its own pattern, which cannot be changed. The main driver of this
pattern is mapping (see `bb.Mapping`).

An _image_ is a form of target that combines a set of objects that will be
later processed by builder and as the result will be created a binary.

The image has to be created in initialization stage (`bb.INITIALIZATION_STAGE`)
with help of `Image` class.

    class Bootloader(Image):
	  pass

There are two instructions: `build` and `load`. The `build` instructuin tells to builder how to
build object(s).

### Example

Let us consider instructions available during BUILDTIME stage.

You can use `>>` operator to assign build instructions for builder about your object.

    from bb.buildtime.application import robot

    robot.Arm >> {
      ('propeller', 'catalina'): {
        sources = ('arm.c',),
      }
      'simulator': {
        sources = ('arm.py',)
      }
    }

This instruction will be applied to all the `robot.Arm` instances that builder will
interact with. In order to add files which are specific to your robot, just
pass its instance as an object:

    robot.right_arm >> {
      'propeller': {
        'sources': ('right_arm.c',)
       }
    }

As the result your binary will include the next sources: _arm.c_ and _right\_arm.c_.

Each _source_ or even all _sources_ can be also represented by a function, where
the function may, or may not return a value. Let us replace the previous sources
with the function `myrobot_c_files`:

    def right_arm_c_files(myrobot):
      return ('right_arm.c',)

    robot.right_arm >> {
	  'propeller': {'sources': right_arm_c_files }
	}

When the function returns a value it will be translated by builder as file
path. When the function returns `None`, this will be simply ignored. The last
case is useful when you need to edit another source file and you are not going
to produce a new one.

## Uploader

### Instructions

 * Explain to uploader how to upload an image that is based on the object:

  _object_ << {
    '_uploader_': {
      '_key_': '_value_'
    }
  }

### Load-script

All the load-scripts ends with _\_load.py_, except of main application load
script, which has name *load.py* and only one per application. This file is the
entry point for the uploader to your application.

### Example

The load-instructions can be used only during `LOADTIME` stage and can be applied
only to `Image` derived objects.

    from bb.loadtime.application import robot
	
	board = robot.arm.get_board()
	# Assume there is only one processor on this board
	processor = board.get_processors()[0]
	bootloader = processor.get_bootloader()
	
	bootloader >> {
	  '*' {
	    port = '/dev/ttyUSB0'
	  }
	}
