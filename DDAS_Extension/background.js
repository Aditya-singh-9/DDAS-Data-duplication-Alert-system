chrome.downloads.onDeterminingFilename.addListener(function(item, suggest) {
    chrome.storage.local.get(null, function(items) {
        let fileHash = computeFileHash(item);
        if (fileHash in items) {
            alert("Duplicate file detected!");
        } else {
            items[fileHash] = item.filename;
            chrome.storage.local.set(items);
        }
    });
});

function computeFileHash(file) {
    // Here we can use SHA-256 or similar hashing method to compute the hash
    // This is a placeholder function; actual hash computation should be based on file content for privacy
    let hashObj = new jsSHA("SHA-256", "TEXT");
    hashObj.update(file.filename + file.url);  // Simplification using URL and filename, replace this with actual file content hash
    return hashObj.getHash("HEX");
}
