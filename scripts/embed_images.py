import base64
import glob
import mimetypes
import os
import re


def embed_images(svg_path):
    with open(svg_path, "r") as f:
        content = f.read()

    # Regex to find image tags with xlink:href
    # Matches: <image ... xlink:href="path/to/image.png" ... />
    pattern = re.compile(r'(<image[^>]*xlink:href=")([^"]+)("[^>]*>)')

    def replace_match(match):
        prefix = match.group(1)
        path = match.group(2)
        suffix = match.group(3)

        if path.startswith("data:"):
            return match.group(0)

        if not os.path.exists(path):
            print(f"Warning: Image not found: {path}")
            return match.group(0)

        mime_type, _ = mimetypes.guess_type(path)
        if not mime_type:
            mime_type = "image/png"

        with open(path, "rb") as img_f:
            encoded = base64.b64encode(img_f.read()).decode("utf-8")

        data_uri = f"data:{mime_type};base64,{encoded}"
        return f"{prefix}{data_uri}{suffix}"

    new_content = pattern.sub(replace_match, content)

    with open(svg_path, "w") as f:
        f.write(new_content)
    print(f"Embedded images in {svg_path}")


if __name__ == "__main__":
    output_dir = "output"
    svg_files = glob.glob(os.path.join(output_dir, "*.svg"))
    for svg_file in svg_files:
        embed_images(svg_file)
