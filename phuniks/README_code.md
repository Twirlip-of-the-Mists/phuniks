# Phuniks

A 2D physics simulator sandbox, inspired by Phun (now Algodoo), that runs natively on Linux.
It uses Kivy for graphics, and PyMunk for the physics, which in turn uses Chipmunk2D.

## Guide to Widgets and Classes

### master_widget

Kivy root widget added to the sceen by phuniks.build()
Has space and menu widget(s) added it to it
Has the Phuniks instance as head of all data structures

### Phuniks

Class with a single instance, that is an attribute of the master_widget
This is the head of all the Phuniks data structures.

### space_widget

Kivy widget things are drawn on. Basically the sandbox.

### menu_widget

Main Kivy menu widget that can add other menu widgets to the master_widget
Only menu widget that can't be closed

### ShapeWidget

Parent class for Kivy widgets to show the shape of things. Have no physics.
OutlineWidget, PolygonWidget, RectangleWidget, CircleWidget inherit from this.

### Makers

Classes that react to mouse events, and create new components (and joins?)

### Modders

Classes that react to mouse events, and modify existing components or joins

### Joiners

Classes that react to mouse events, and join two existing components

### Assemblies

Each assembly has a pymunk body, and repesent several physical objects (or components)
that have been stapled together, and behave physically as one object. Each has multiple:
  Components: Each component represents a natural object, has an kivy widget, and has multiple:
    Pymunk shapes, for physics. In pymunk, these belong to the body, not the component
    Joins, joining two components, and with a pymunk constraint and a kivy widget
  Staples: Rigid joins of two components, and are what hold assemblies together

Two assemblies can be joined into one, if two things in different assemblies are stapled together.

One assemblies can be split into two, if a staple is deleted

There are many types of joins - hinges, motors, linear springs, rotary springs
