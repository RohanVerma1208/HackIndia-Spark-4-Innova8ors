document.getElementById('usePrompt').onclick = async function() {
    const prompt = document.getElementById('promptInput').value;
    const response = await fetch('/generate-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt }),
    });

    if (response.ok) {
        const data = await response.json();
        const img = document.getElementById('generatedImage');
        img.src = 'data:image/png;base64,' + data.image;
        img.style.display = 'block'; // Show the image

        // Show download and create NFT buttons
        document.getElementById('downloadImage').style.display = 'inline-block';
        document.getElementById('createNFT').style.display = 'inline-block';
    } else {
        alert('Error generating image: ' + (await response.json()).error);
    }
};

document.getElementById('downloadImage').onclick = function() {
    const img = document.getElementById('generatedImage');
    const link = document.createElement('a');
    link.href = img.src;
    link.download = 'generated_image.png'; // Set the default filename
    link.click();
};

document.getElementById('createNFT').onclick = async function() {
    const prompt = document.getElementById('promptInput').value;
    const img = document.getElementById('generatedImage').src.replace(/^data:image\/(png|jpg);base64,/, "");

    const response = await fetch('/create-nft', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt, image: img }),
    });

    if (response.ok) {
        const data = await response.json();
        alert('NFT created successfully! CID: ' + data.cid); // Changed to 'data.cid'
        
        // Redirect to /json after successful NFT creation
        window.location.href = '/json';
    } else {
        alert('Error creating NFT: ' + (await response.json()).error);
    }
};

document.getElementById('getBetterSuggestion').onclick = async function() {
    const prompt = document.getElementById('promptInput').value;
    const response = await fetch('/get-better-suggestion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt }),
    });

    if (response.ok) {
        const data = await response.json();
        document.getElementById('promptInput').value = data.better_prompt;
    } else {
        alert('Error getting better suggestion: ' + (await response.json()).error);
    }
};
