# Extended Clusters - A Netbox Plugin

TODO: Write plugin documentation, the outline here is provided as a guide and should be expanded upon.  If more detail is required you are encouraged to expand on the table of contents (TOC) in `mkdocs.yml` to add additional pages.

## Documentation

The documentation contains a

- [User Guide](user/app_overview.md) Overview,  Using the Plugin, and Getting Started.
- [Administrator Guide](admin/install.md) - How to Install, Configure, Upgrade, or Uninstall the Plugin.
- [Developer Guide](dev/contributing.md) - Extending the Plugin, Code Reference, Contribution Guide.

### Contributing to the Documentation

You can find all the Markdown source for the Plugin documentation under the [`docs`](https://github.com/psmware-ltd/arch-decision-rec-app/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient: clone the repository and edit away.

If you need to view the fully-generated documentation site, you can build it with [MkDocs](https://www.mkdocs.org/). A container hosting the documentation can be started using the `invoke` commands (details in the [Development Environment Guide](dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). Using this container, as your changes to the documentation are saved, they will be automatically rebuilt and any pages currently being viewed will be reloaded in your browser.

Any PRs with fixes or improvements are very welcome!
