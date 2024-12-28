# Author: Prakash Sahu <github.com/prakash4844> <pk484442@gmail.com>

#  This file is the main file for the project. It is the file that will be run to start the program.
#  It will call the necessary functions to start the program. It will also contain the main loop of the program.

import image_cut_and_stitch as ics
from image_cut_and_stitch import calculate_image_cut_res
import typer


# Create a Typer app instance.
# Set the app's help message with the version information.
app = typer.Typer(
    name="Image Cut and Stitch (ICS)",
    no_args_is_help=True,
    invoke_without_command=True,
    help=f"Image cut and stitch. \n\nVersion: {ics.__version__}",
    context_settings={"help_option_names": ["-h", "--help"]},
)


# Define a callback function to display the version information
@app.callback(invoke_without_command=True)
def get_version(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Print version and exit.",  # Help message for the version option
    ),
) -> None:
    """
    Display the version of Image Cut and Stitch (ICS)
    """
    if version:
        typer.echo(f"Image cut and stitch (ICS): Version: {ics.__version__}")  # Print the version information if the version option is provided
        raise typer.Exit()  # Exit the application

app.add_typer(calculate_image_cut_res.app, name="cut")  # Add the 'cut' command to the Typer app

# Execute the Typer app when the script is run directly
if __name__ == "__main__":
    app()  # Run the Typer app