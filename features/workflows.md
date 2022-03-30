# Workflows

Workflows are an easier way to execute and share commands within Warp. They are searchable by name, description, or command and are easily parameterized. A [global list](https://github.com/warpdotdev/workflows) of commands sourced by the Warp team and community are readily available within the app. Additionally, you can create and manage local workflows specific to you or associated with a particular git repository.

The in app Workflows menu can be accessed through the Command Palette or by pressing `SHIFT-CTRL-R`. Once inside the menu, filter the existing commands by typing in the search bar or click on any of the sections in the side panel to browse by category.

![Press SHIFT-CTRL-R to open the Workflows menu.](../.gitbook/assets/workflows-original.gif)

## Creating Custom Workflows

In addition to the globally sourced commands, Workflows supports the ability to save commonly used commands specific to you or your team by adding workflows defined in YAML files directly to the `~/.warp/workflows` directory or the `.warp/workflows` in the top level of a repository. Local and project workflows can be accessed under the "My Workflows" and "Project Workflows" tab of the workflows menu, respectively.

### Local vs Project Workflows

Local workflows are specific to a single developer. Project workflows are instead associated with a specific git repository and can be accessed by anyone who has cloned the repo. **Currently, project workflows will not appear if you are SSH’d into a remote machine**.

Local Workflows: `~/.warp/workflows`

Project Workflows `{{path_to_project}}/.warp/workflows`

### Workflows File Format

The existing workflows specs within the [Workflows repo](https://github.com/warpdotdev/workflows) should serve as an example for the format. Additionally, a more comprehensive file format is available in [FORMAT.md](https://github.com/warpdotdev/workflows/blob/main/FORMAT.md).

### Adding a Local Workflow

To start, create a workflows subdirectory within your .warp folder

`mkdir -p ~/.warp/workflows`

Then, add your command’s yaml file to this directory and Warp should automatically load it into the workflows menu.

`cp ~/path/to/my_awesome_workflow.yaml ~/.warp/workflows`

### Adding a Project Workflow

You can add a project workflow exactly like you add a local workflow except now the yaml file should live within the repo’s. .warp directory. While cd’d into the repo’s root directory run”

```
mkdir -p .warp/workflows

cp ~/path/to/my_awesome_workflow.yaml .warp/workflows
```

## Contributing to Global Workflows

You can add workflows that all Warp users can use by contributing directly to the [Workflows repo](https://github.com/warpdotdev/workflows). See the [Contributing](https://github.com/warpdotdev/workflows#contributing) section for more details.
