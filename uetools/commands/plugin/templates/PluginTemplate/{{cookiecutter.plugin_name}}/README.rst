{{cookiecutter.plugin_name}}
============================


Features
--------


Folder Structure
----------------


.. code-block::

   {{cookiecutter.plugin_name}}/
   ├── Config
   ├── Content                                     # Plugin Content
   ├── Docs                                        # Sphinx Documentation
   ├── Resources
   ├── Shaders                                     # HLSL Code
   ├── Source
   │   ├── {{cookiecutter.plugin_name}}            # Game Plugin
   │   ├── {{cookiecutter.plugin_name}}Ed          # Editor Extension
   │   ├── {{cookiecutter.plugin_name}}Shader      # Custom Shaders
   │   ├── {{cookiecutter.plugin_name}}Test        # Testing Module
   │   └── python                                  # Python automation
   ├── {{cookiecutter.plugin_name}}.uplugin
   ├── README.rst
   └── setup.py                                    # Python setup


Useful Links
------------

* `Marketplace <https://www.unrealengine.com/marketplace/en-US/product/{{cookiecutter.market_place_id}}>`_
* `Playable demo <https://{{cookiecutter.gitlab_repo}}.itch.io/{{cookiecutter.gitlab_repo}}>`_
* `Bug Tracker <https://gitlab.com/{{cookiecutter.gitlab_org}}/{{cookiecutter.gitlab_repo}}/-/issues>`_
* `Documentation <https://{{cookiecutter.gitlab_org}}.gitlab.io/{{cookiecutter.gitlab_repo}}/>`_
* `Youtube Channel <https://www.youtube.com/@{{cookiecutter.youtube_tag}}>`_
* `Discord Server <{{cookiecutter.discord_server}}>`_
* `Patreon <https://www.patreon.com/{{cookiecutter.patron_handle}}>`_
* `Twitter <https://twitter.com/{{cookiecutter.twitter_handle}}>`_
