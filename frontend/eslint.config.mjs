import { eslint } from '@siberiacancode/eslint';

export default eslint(
   {
      typescript: true,
      jsx: true,
      jsxA11y: false,
      react: true,
      stylistic: false,
      next: false,
   },
   {
      rules: {
         'node/prefer-global/process': ['error', 'always'],
         'siberiacancode-react/prop-types': 'off',
         'perfectionist/sort-imports': 'off',
         'siberiacancode-react/function-component-definition': 'off',
         'siberiacancode-jsx-a11y/heading-has-content': 'off',
         'unused-imports/no-unused-vars': 'warn',
         'react-refresh/only-export-components': 'off',
      },
   },
);
