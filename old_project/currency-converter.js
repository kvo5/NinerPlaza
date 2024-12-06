// currency-converter.js

// API details for ExchangeRate-API
const API_KEY = '490420bf74e3a539aeeb64f7';
const BASE_URL = 'https://v6.exchangerate-api.com/v6/490420bf74e3a539aeeb64f7/latest/USD';

document.addEventListener('DOMContentLoaded', () => {
    const currencySelect = document.getElementById('currency-select');
    const prices = document.querySelectorAll('.price');
    const bannerContent = document.querySelector('.banner-content');

    // Store the exchange rates globally
    let exchangeRates = {};

    // Load the saved currency preference
    const savedCurrency = localStorage.getItem('selectedCurrency');
    if (savedCurrency) {
        currencySelect.value = savedCurrency;
    }

    currencySelect.addEventListener('change', () => {
        // Save the selected currency
        localStorage.setItem('selectedCurrency', currencySelect.value);
        updatePrices();
    });

    // Function to fetch exchange rates
    async function fetchExchangeRates() {
        try {
            // CHANGE: Added loading indicator
            document.body.style.cursor = 'wait';
            const response = await fetch(BASE_URL);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (data.result === 'success') {
                exchangeRates = data.conversion_rates;
            } else {
                // CHANGE: More specific error for API response issues
                throw new Error(`API returned error: ${data.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error fetching exchange rates:', error);
            // Throw a more user-friendly error
            throw new Error('Unable to fetch current exchange rates. Please try again later.');
        } finally {
            // Remove loading indicator
            document.body.style.cursor = 'default';
        }
    }

    async function updatePrices() {
        const selectedCurrency = currencySelect.value;
        
        // Fetch exchange rates if we haven't already
        if (Object.keys(exchangeRates).length === 0) {
            await fetchExchangeRates();
        }

        for (const priceElement of prices) {
            const usdPrice = parseFloat(priceElement.getAttribute('data-price'));
            try {
                const convertedPrice = convertCurrency(usdPrice, 'USD', selectedCurrency);
                priceElement.textContent = formatPrice(convertedPrice, selectedCurrency);
            } catch (error) {
                console.error('Error converting currency:', error);
                priceElement.textContent = `Error: ${error.message || 'Unknown error'}`;
            }
        }
    
        // Update gift card amounts only if they exist on the page
        if (document.querySelector('.gift-amounts')) {
            updateGiftCardAmounts(selectedCurrency);
        }

        // Update the banner
        updateBanner(selectedCurrency);
    }

    function updateGiftCardAmounts(currency) {
        const giftAmountButtons = document.querySelectorAll('.amount-btn');
        giftAmountButtons.forEach(button => {
            const usdAmount = parseFloat(button.getAttribute('data-price'));
            try {
                const convertedAmount = convertCurrency(usdAmount, 'USD', currency);
                button.textContent = formatPrice(convertedAmount, currency);
            } catch (error) {
                console.error('Error converting gift card amount:', error);
                button.textContent = `Error: ${error.message || 'Unknown error'}`;
            }
        });
    }

    function updateBanner(currency) {
        if (!bannerContent) return; // Skip if banner doesn't exist

        const usdThreshold = 100;
        const convertedThreshold = convertCurrency(usdThreshold, 'USD', currency);
        const formattedThreshold = formatPrice(convertedThreshold, currency);

        const newBannerText = `FREE SHIPPING ON ORDERS OVER ${formattedThreshold}`;
        
        // Update all h1 elements in the banner
        const bannerH1s = bannerContent.querySelectorAll('h1');
        bannerH1s.forEach(h1 => {
            h1.textContent = newBannerText;
        });
    }

    // Simplified convertCurrency function as we now have exchange rates
    function convertCurrency(amount, from, to) {
        if (from !== 'USD') {
            throw new Error('Base currency must be USD');
        }
        if (!exchangeRates[to]) {
            throw new Error(`Exchange rate not available for ${to}`);
        }
        return amount * exchangeRates[to];
    }

    function formatPrice(price, currency) {
        const formatter = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency,
        });
        return formatter.format(price);
    }

    // Initial price update
    updatePrices().catch(error => {
        console.error('Initial update failed:', error);
        prices.forEach(priceElement => {
            priceElement.textContent = `Error: ${error.message || 'Failed to update prices'}`;
        });
    });
});