        const cors = require('cors');
        app.use((cors))
        async function fetchImages(query) {
            try {

                var proxyUrl = 'https://cors-anywhere.herokuapp.com/';
                const response = await fetch(proxyUrl + `https://arq.hamker.dev/wall?query=${encodeURIComponent(query)}`, {
                    headers: {
                        'accept': 'application/json',
                        'X-API-KEY': 'BEDGJR-TCKRYV-CCVEKU-EHSMQV-ARQ',
                        'Access-Control-Allow-Origin': 'https://cors-anywhere.herokuapp.com/',
                        'Access-Control-Allow-Methods': 'GET',
                        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                    }   
                });
                const data = await response.json();

                if (data.ok) {
                    const gallery = document.getElementById('gallery');
                    
                    gallery.innerHTML = ''; // Clear previous results
                    data.result.forEach(async img => {
                        try {
                            const imgResponse = await fetch(img.url_image);
                            if (imgResponse.status === 200) {
                                const item = document.createElement('div');
                                item.classList.add('gallery-item');

                                const imgElement = document.createElement('img');
                                imgElement.src = img.url_image;
                                imgElement.alt = img.file_type;
                                imgElement.onclick = () => window.open(img.url_image, '_blank');

                                item.appendChild(imgElement);
                                gallery.appendChild(item);
                            }
                        } catch (imgError) {
                            console.error(`Error loading image: ${img.url_image}`, imgError);
                        }
                    });
                } else {
                    console.error('Error: API response not ok');
                    swal("Whatever you searched is not available.");
                }
            } catch (error) {
                console.error('Error fetching images:', error);
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                const query = document.getElementById('searchInput').value;
                fetchImages(query);
            }
        }

        // Initial fetch for default query
        fetchImages('anime');
