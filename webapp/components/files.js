import fs from 'fs';
import path from 'path';

function FileList(props) {
  let files = []
  const directoryPath = path.join(__dirname, '../../output');
  fs.readdir(directoryPath, (err, f) => {
    if (err) {
      return console.log('Unable to scan directory: ' + err);
    } 
    files = f;
  });

  return (
    <div>
      <h2>Files in ../../output:</h2>
      <ul>
        {files.map(file => 
          <li key={file}>{file}</li>
        )}
      </ul>
    </div>
  );
}

export default FileList;