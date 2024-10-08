// document.getElementById('nftForm').addEventListener('submit', async function(event) {
//     event.preventDefault();

//     const name = document.getElementById('name').value;
//     const prompt = document.getElementById('prompt').value;
//     const nft_cid = document.getElementById('nft_cid').value;

//     // Create JSON metadata
//     const metadata = {
//         name: name,
//         prompt: prompt,
//         nft_cid: nft_cid,
//     };

//     const response = await fetch('/create-metadata', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(metadata)
//     });

//     const result = await response.json();
//     alert(result.message);
//     if (response.ok) {
//         // Optionally redirect to a success page or display success message
//         window.location.href = '/success';  // Redirect or change as necessary
//     }
// });

document.getElementById('nftForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission

    const name = document.getElementById('name').value;
    const prompt = document.getElementById('prompt').value;
    const nft_cid = document.getElementById('nft_cid').value;

    fetch('/create-metadata', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: name, prompt: prompt, nft_cid: nft_cid })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`Error: ${data.error}`);
        } else {
            alert(`Success: ${data.message}`);
            // Optionally, handle the response, e.g., redirect or clear the form
        }
    })
    .catch(error => {
        alert(`Fetch error: ${error}`);
    });
});

