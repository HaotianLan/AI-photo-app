import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.example.my',
  appName: 'my',
  webDir: 'dist',
  server: {
    androidScheme: 'https'
  },
  plugins: {
    Camera: {
      permitGallery: true
    },
    Filesystem: {
      readInaccessibleFiles: true
    }
  }
};

export default config;
