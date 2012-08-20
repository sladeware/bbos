# BB Build System

Build system is the key component of BB platform. It includes such tools as
*builder*, *toolchain\_manager*, *compiler\_manager* and *loader\_manager*.

## Builder

The builder is the heart of build system. It reads build-files and does
appropriate actions.

### Build file

The _build-file_ is a container for _targets_ and _descriptors_.

All the build files ends with _\_build.py_, except of main application build
file, which has name *build.py* and only one per application. This file is the
entry point for the builder to your application.

On the start up the builder will load all the build files and store them under
the reserved namespace `bb.buildtime`. However builder stores build files it a
special way. For example build file for the BB application
_bb.application\_build.py_ will be stored as `bb.buildtime.application`.

### Targets

Each build-file may contain a _targets_. There are two kind of targets: _images_
and _functions_.

The targets can be used with help of `bb.buildtime` namespace. Suppose you have a target
`bootloader` that will produce a bootloader binary for you. Here is the way you can run it:

    builder.select_target('bb.buildtime.application:bootloader')

#### Images

An _image_ is a form of target that combines a set of objects that will be
later processed by builder and as the result will be created a binary.

    builder.image(
      name     = <string>,
      objects  = <list>,
      filename = <string>
    )

#### Functions

A _function_ is a function that can be called by builder as
target. For exanple functions can be used to create another targets such as
images. For example:

    builder.function(
      name = 'main',
      f = lambda: builder.image('myrobot', myrobot), builder.add_image(':myrobot')
    )

Or

    def main():
      builder.image('myrobot', myrobot)
      builder.add_image(':myrobot')
  
    builder.function(
      name = 'main',
      f = main,
    )
  
Call `builder.select_target('bb.buildtime.application:main')`.

### Descriptors

A _descriptor_ specifies relationship between an object and toolchain that will be
used to process this object. The object can be represented by a class and its instance.

    builder.descriptor(
      object  = Robot,
       = {
        'propeller': {
          sources = ('body.c', 'head.c'),
        }
        'simulator': {
          sources = ('body.py', 'head.py')
        }
      }
    )

This rule will be applied to all the `Robot` instances that builder will
interact with.  In order to add files which are specific to your robot, just
pass its instance as an object:

    myrobot = Robot()

    builder.propeller_plugin(
      myrobot,
      ('mybody.c', 'myhead.c')
    )

As the result your binary will include the next sources: _body.c_, _head.c_,
_mybody.c_, _myhead.c_.

The _source_ can be also represented by a function, where the function may, or
may not return a value. Let us replace the previous sources with the function
`myrobot_c_files` function:

    def myrobot_c_files(myrobot):
      return ('mybody.c', 'myhead.c')

When the function returns a value it will be translated by builder as file
path. When the function returns `None`, this will be simply ignored. The last
case is useful when you need to edit another source file and you are not going
to produce a new one.

## Project

On the last step has to be created project that will include all the images and
rules for the target.

    builder.project(myrobot)

    class Application(bb.build.Project):
      TARGET = myrobot

      def build(self):
        self.add_images(myrobot)
    

This will automatically add images assciated with target `myrobot`.

    builder.select_projects(myrobot)

Once targets were selected you can run build process manually:

    builder.build()
    
Or with help of command-line interface:

    $ bb build

By default builder know only about one target `bb.application`.

## Simple example

This example shows how you can use bb builder for other purposes.

    from bb.build import builder

    robot = object()

    builder.rule(
      robot, {
        'propeller': {
          sources: ('hello.c', 'world.c')
        }
      }
    )
    # ... produce the binary 'robot' for the target
    builder.image(robot, 'robot')
    builder.project(robot)

Now call 'bb build'.


This will create a binary _myrobot_ that you will be able to load later.
