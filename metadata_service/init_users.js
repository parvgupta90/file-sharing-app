db = db.getSiblingDB("file_sharing_db"); // Create or connect to the database
db.createCollection("users"); // Create users collection if not exists

db.users.createIndex({ username: 1 }, { unique: true }); // Ensure username is unique
// init_users.js
db.createUser({
  user: "adminUser",
  pwd: "adminPassword",
  roles: [{ role: "readWrite", db: "fileSharingDB" }],
});

db = db.getSiblingDB("fileSharingDB");

db.users.insertOne({
  username: "demoUser",
  password: "hashedPasswordHere", // Use a hashed password in real implementations
});
