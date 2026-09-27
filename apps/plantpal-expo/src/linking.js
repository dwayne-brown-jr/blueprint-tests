// Deep links, e.g. from the password reset email
export const linking = {
  prefixes: ['plantpal://', 'https://plantpal.app'],
  config: {
    screens: {
      Home: '',
      Plant: 'plant/:id',
      ResetPassword: 'reset-password',   // plantpal://reset-password?uid=<userId>
      Admin: 'admin',
    },
  },
}
