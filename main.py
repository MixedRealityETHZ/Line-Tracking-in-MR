import src.main_app as main_app

# Code suggestion (for the developers).
# The `main.py` will serve two purposes:
# Define and/or create calls to:
#   a) the main application, which is currently done with `main_app.run()`.
#   b) potential input arguments --from the command console or otherwise.

# I recommend that any code file regarding the software's logic
# should be included in the `src` folder (or any of its subdirectories).
# I encourage people to follow this, so that we do not
# stumble upon unexpected errors when running `main.py`,
# due to the importing system of the Python language.

# Other folders may exist in the same hierarchical level (i.e. the root)
# of the project directory tree,
# as long as it is independent of anything relating to the logic of the program.
# Such examples include images, videos, (raw) data etc.

def main():
    main_app.run()


if __name__ == '__main__':
    main()