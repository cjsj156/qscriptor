from scriptor.user_defined_scriptor import ExampleScriptor
import os

if __name__ == "__main__":
    scriptor = ExampleScriptor()
    template = scriptor.make_templates()
    script = scriptor.render_template()
    script_path = scriptor.write_script()

    dir = os.path.dirname(script_path)
    script_name = os.path.basename(script_path)
    print(f"{dir}")
    print(f"{script_name}")