.. _guide.tools:

Tools
=============

Fritzing
--------

Fritzing is an open source software initiative to support designers and artists
ready to move from physical prototyping to actual product. It was developed at
the University of Applied Sciences of Potsdam.

The Fritzing EDA is represented by :mod:`bb.tools.fritzing`. To
start working with Fritzing you need to setup home directory and user
directory if required::

    from bb.tools import fritzing
    fritzing.set_home_dir("/opt/fritzing")

Suppose we would like to read Propeller D40 part located at
:file:`parts/core/controller_propeller_D40.fzp`::

    propeller_d40 = fritzing.parse("parts/core/controller_propeller_D40.fzp")
    print "Part:", propeller_d40.get_property_value("name")
    print "Package:", propeller_d40.get_property_value("package")
    print "Keywords:", propeller_d40.get_property_value("keywords")
    print "Description:", propeller_d40.get_property_value("description")
    num_pins = propeller_d40.count_pins()
    if not num_pins:
        print "Sorry, but %s does not have pins" % propeller_d40.designator
    else:
        print "Number of pins:", num_pins

Let us find pin ``XO`` (Crystal Output). According to
:file:`parts/core/controller_propeller_D40.fzp` metafile this pin has
unique ID ``connector30``::

    pin = propeller_d40.find_pin("connector30")
    print "Pin with ID 'connector30':", pin.designator # or pin.get_property_value("designator")
    print "Description:", pin.get_property_value("description")

