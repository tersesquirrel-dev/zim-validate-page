# zim-validate-page

Usage:
* Copy validation_sample.py to the folder you want to run validation on as validation.py


* Add custom python validation code to the validation.py file.

* In Zim Desktop Wiki use CTRL-SHIFT-V (or other assigned shortcut) to perform the validation on the current page.

* The validation.py file can be anywhere in the parent structure of the notebook.

    So if the folder structure looks like

        Notebook
        |-- Page 1
        |-- Wiki
            |-- Page 2
            |-- Page 3

    If the validation is put in the Wiki folder it will validate any page under Wiki (2 and 3)

    If it were placed in the Notebook folder then it can be used with any page (1, 2, and 3)

    If both Notebook and Wiki contain validation.py scripts then the first one found going towards the root will be used.