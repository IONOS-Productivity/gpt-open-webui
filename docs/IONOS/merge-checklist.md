# Merge checklist

Things to checks when merging a newer upstream version (upgrading).

## Preparations

You might want to keyword-search the upstream [changelog](https://github.com/open-webui/open-webui/blob/main/CHANGELOG.md) upfront for deperecations, breaking changes and changed or removed features. Note that some critical changes were not mentioned previously.

Look for updated dependencies and spot check what their changes bring (`package.json` and `requirments.txt`).


## Tests

1. Run container build and tests

   ```
   [frontend] $ npm run test:frontend
   [ backend] $ pytest open_webui/test/
   ```

2. Test login methods and logout

   * OIDC (see [testing-signup.md](./testing-signup.md))
   * local usermanagement (see [signup.md](./signup.md))

3. Test the core application functions

   To mention some: signup, chat, knowledgebase, file upload to chats, export, ...

   Use e2e tests where available.

4. Check the design

   * Typography and colors
   * Changes in non-customized Open WebUI translations

     Either by diffing the localization files or going through the UI.
