# yadvashem
1. Open yadvashem and search for something.
1. Follow `seach_browser.js`
1. ctrl+h (search and replace):
   * `]}` -> `,`
   * `{"d":[` -> ``
1. add `inp = [` at the beginning and `]` at the end
1. remove all enters
1. copy this single line to `dump_ids.py`
1. find a unique name for the output json file and modify `OUTPUT_IDS`
1. in console: python `dump_ids.py`
1. in `pull_books.py` modify:
   * `INPUT_IDS`
   * `BASE_PATH` for downloading images
1. in console: python `pull_books.py`
1. profit

caveats:
1. check the `error.log` file afterwards and figure out what to do
1. currently on OCR
