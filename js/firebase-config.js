// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyC_Mn61pVpkaNsv4UG0rx5ZBo_sRZvPne4",
  authDomain: "eternal-3feba.firebaseapp.com",
  projectId: "eternal-3feba",
  storageBucket: "eternal-3feba.firebasestorage.app",
  messagingSenderId: "332978389442",
  appId: "1:332978389442:web:a80658fa4d8fc1bb16165b",
  measurementId: "G-PZTN77B0SG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
