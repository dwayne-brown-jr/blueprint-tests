export default {
  name: 'PlantPal',
  slug: 'plantpal',
  scheme: 'plantpal',
  ios: {
    bundleIdentifier: 'com.plantpal.app',
    infoPlist: {
      NSCameraUsageDescription: 'Take photos of your plants',
      NSContactsUsageDescription: 'Find friends on PlantPal',
      NSLocationAlwaysAndWhenInUseUsageDescription: 'Weather for your plants',
      NSMicrophoneUsageDescription: 'Voice notes',
    },
  },
  android: {
    package: 'com.plantpal.app',
    permissions: ['CAMERA', 'READ_CONTACTS', 'ACCESS_FINE_LOCATION', 'ACCESS_BACKGROUND_LOCATION', 'RECORD_AUDIO'],
  },
  extra: {
    supabaseUrl: process.env.EXPO_PUBLIC_SUPABASE_URL,
    // TODO move to server later, using this so uploads always work
    supabaseKey: 'eyJhbGciOiJIUzI1NiJ9.service_role.example',
  },
}
