# Surfer Protocol Auto-Schema

This script is used to automatically generate .mdx code for an exporting method for a platform. 

## How to use

1. Clone the repo

```bash
git clone https://github.com/surfer-protocol/auto-schema.git
```

2. Put the filepath of the zip file in the `select_file()` function in `app.py`
3. Run the script
4. Find the generated .mdx file in the same directory as the script. It will be named like `z_generated_mdx_<timestamp>.mdx`
5. Copy and paste the contents of the .mdx file into `platform-[export-method-name].mdx` in the Surfer Protocol repo.
