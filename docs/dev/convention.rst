Developer Convention
====================

Concept
-------

Path concept ::

   /home/user/lupv-data/ AlKhawarizmi-12345/
   --------------------  ------------------
        record_path         student_dir
   ---------------------------------------
                  student_path

Naming Variables
----------------

Naming variable for instances of Qt Widget

- QTreewidget = foo (e.g foo_files)
- QPlainTextEdit = foo_text (e.g diff_text)
- QButton = foo_button (e.g close_button)
- QLabel = foo_label (e.g logo_label)

We don't prefixes and suffixes the variable name with the widget name,
e.g `foo_TreeWidget` or `bar_text_edit`. It will become painful to
refactor when Qt API changes. See `Designing Qt-Style C++ APIs
<https://doc.qt.io/archives/qq/qq13-apis.html>`_ and `Naming convention
for Qt widgets <https://stackoverflow.com/a/404244/6000005>`_ for more information.
