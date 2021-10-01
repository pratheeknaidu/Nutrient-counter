var express = require('express');
const app = express();
const Multer = require('multer');
const imgUpload = require('./imgUpload');
const getMessages = require('./getMessages');
const PORT = process.env.PORT || 3001;
const delay = ms => new Promise(res => setTimeout(res, ms))
const path = __dirname + '/frontend/views/';

var cors = require('cors');

app.use(cors())

app.use(express.static(path));

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});

let checkForMessages = async (filename) => {
  console.log(filename)
  console.log(getMessages.messages.has(filename))
  while(!getMessages.messages.has(filename)) {
    // await sleep(2000);
    // await new Promise(resolve => setTimeout(resolve, 2000));
    console.log("in while")
    await delay(5000);
  }
  if(getMessages.messages.has(filename)) {
    console.log("filename found")
    return getMessages.messages.get(filename);
  }
}

getMessages.listenWithCustomAttributes();

// Handles the multipart/form-data
// Adds a .file key to the request object
// the 'storage' key saves the image temporarily for in memory
// You can also pass a file path on your server and it will save the image there
var upload = Multer({
  storage: Multer.MemoryStorage,
  fileFilter: (req, file, cb) => {
      if (file.mimetype == "image/png" || file.mimetype == "image/jpg" || file.mimetype == "image/jpeg") {
          cb(null, true);
      } else {
          cb(null, false);
          return cb(new Error('Only .png, .jpg and .jpeg format allowed!'));
      }
  }
});

// the multer accessing the key 'image', as defined in the `FormData` object on the front end
// Passing the uploadToGcs function as middleware to handle the uploading of request.file
app.post('/api/image-upload-test', upload.single('foodImg'), imgUpload.uploadToGcs, async function(request, response, next) {
  const data = request.body;
  if (request.file && request.file.cloudStoragePublicUrl) {
    data.imageUrl = request.file.cloudStoragePublicUrl;
  }
  data["calorie_result"] =  await checkForMessages(request.file.cloudStorageObject)
  response.send(data);
})

app.get('/api/health-check', function (req, res) {
  res.send('healthy')
})

app.get("/*", (req, res) => {
  res.sendFile(path + "index.html");
})