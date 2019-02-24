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

Naming variable for instances of Qt Widget.

Common things are abbreviated:

- QButton = foo_button (e.g close_btn)
- QLabel = foo_label (e.g logo_lbl)

I prefer to suffixes them with 'widget' to make me differentiate
faster between `local-global/widget` variable.

- QPlainTextEdit = foo_text (e.g file_content_widget)

But I don't suffixes 'widget' for names that already represent it:

- QTreewidget = (e.g log_tree)
- splitter
- menubar
- statusbar
- toolbar
