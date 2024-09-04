document.addEventListener('DOMContentLoaded', function() {
    const statusElement = document.getElementById('status');
    const resultElement = document.getElementById('result');
    const checkNowBtn = document.getElementById('checkNowBtn');

    // Retrieve and display a message about the most recent download or duplicate detection
    chrome.storage.local.get(['lastMessage'], function(result) {
        if (result.lastMessage) {
            statusElement.textContent = result.lastMessage;
        } else {
            statusElement.textContent = "No recent downloads detected.";
        }
    });

    // Handle "Check Now" button click
    checkNowBtn.addEventListener('click', function() {
        statusElement.textContent = "Checking for duplicates...";
        
        // You can replace this with a function that checks for duplicates
        chrome.downloads.search({}, function(items) {
            if (items && items.length > 0) {
                const lastDownload = items[items.length - 1];
                
                // Simplified: just checking last downloaded item's filename
                chrome.storage.local.get(null, function(storedItems) {
                    const fileHash = computeFileHash(lastDownload);
                    
                    if (fileHash in storedItems) {
                        resultElement.textContent = "Duplicate file detected!";
                    } else {
                        resultElement.textContent = "No duplicates found.";
                        // Store the new file's hash
                        storedItems[fileHash] = lastDownload.filename;
                        chrome.storage.local.set(storedItems);
                    }
                });
            } else {
                resultElement.textContent = "No recent downloads to check.";
            }
        });
    });

    // Simplified hash computation for demo purposes
    function computeFileHash(file) {
        // You would replace this with actual file content hashing logic
        return file.filename + file.url;  // Simplified hash for now
    }
});
