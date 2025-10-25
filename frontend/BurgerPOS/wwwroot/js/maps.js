// frontend/BurgerPOS/wwwroot/js/eircode-search.js

/**
 * Busca una dirección usando el Eircode irlandés
 * Prioriza Google Maps Geocoding API
 */
window.searchAddressByEircode = async function(eircode, dotnetReference) {
    console.log('🔍 Buscando dirección para Eircode:', eircode);
    
    const cleanEircode = eircode.trim().toUpperCase().replace(/\s+/g, '');
    
    // Validar que sea un Eircode irlandés válido
    if (!isValidIrishEircode(cleanEircode)) {
        console.error('❌ Formato de Eircode inválido:', cleanEircode);
        await dotnetReference.invokeMethodAsync('OnAddressError', 
            'Formato de Eircode inválido. Debe ser como: A92 D65P'
        );
        return;
    }
    
    try {
        // Método 1: Google Maps (PRINCIPAL - requiere API key)
        if (typeof google !== 'undefined' && google.maps && google.maps.Geocoder) {
            console.log('🗺️ Método 1: Usando Google Maps Geocoding API...');
            await searchWithGoogleMaps(cleanEircode, dotnetReference);
            return;
        } else {
            console.warn('⚠️ Google Maps no está disponible. Verifica que el script esté cargado y que tengas una API key válida.');
        }
        
        // Método 2: Nominatim (Fallback - gratis pero menos preciso)
        console.log('📡 Método 2 (Fallback): Consultando Nominatim...');
        
        const nominatimUrl = `https://nominatim.openstreetmap.org/search?` +
            `postalcode=${encodeURIComponent(cleanEircode)}` +
            `&country=ie` +
            `&countrycodes=ie` +
            `&format=json` +
            `&addressdetails=1` +
            `&limit=1`;
        
        const nominatimResponse = await fetch(nominatimUrl, {
            headers: {
                'User-Agent': 'BurgerPOS/1.0'
            }
        });
        
        if (nominatimResponse.ok) {
            const nominatimData = await nominatimResponse.json();
            console.log('📦 Respuesta Nominatim:', nominatimData);
            
            if (nominatimData && nominatimData.length > 0) {
                const result = nominatimData[0];
                
                if (result.address && result.address.country_code === 'ie') {
                    const address = result.address;
                    
                    let addressLine = '';
                    
                    if (address.house_number && address.road) {
                        addressLine = `${address.house_number} ${address.road}`;
                    } else if (address.road) {
                        addressLine = address.road;
                    } else if (address.neighbourhood) {
                        addressLine = address.neighbourhood;
                    } else if (address.suburb) {
                        addressLine = address.suburb;
                    } else if (address.village) {
                        addressLine = address.village;
                    } else {
                        const parts = result.display_name.split(',');
                        addressLine = parts[0].trim();
                    }
                    
                    const city = address.town || address.city || address.village || address.county || 'Drogheda';
                    const county = address.county || 'County Louth';
                    const lat = parseFloat(result.lat);
                    const lon = parseFloat(result.lon);
                    
                    console.log('✅ Nominatim - Dirección encontrada:', {
                        address: addressLine,
                        city: city,
                        county: county,
                        lat: lat,
                        lon: lon
                    });
                    
                    await dotnetReference.invokeMethodAsync('OnAddressFound', 
                        addressLine, 
                        city, 
                        lat, 
                        lon
                    );
                    
                    return;
                }
            }
        }
        
        // Método 3: Detección por prefijo (último recurso)
        console.log('📡 Método 3 (Último recurso): Usando mapa de prefijos...');
        
        if (cleanEircode.startsWith('A92')) {
            console.log('✅ Detectado área de Drogheda');
            await dotnetReference.invokeMethodAsync('OnAddressFound', 
                'Drogheda Area', 
                'Drogheda', 
                53.7134, 
                -6.3488
            );
            return;
        }
        
        const eircodeMap = getIrishEircodeCity(cleanEircode);
        if (eircodeMap) {
            console.log('✅ Área detectada por prefijo:', eircodeMap);
            await dotnetReference.invokeMethodAsync('OnAddressFound', 
                eircodeMap.area, 
                eircodeMap.city, 
                eircodeMap.lat, 
                eircodeMap.lon
            );
            return;
        }
        
        // No se encontró
        console.warn('❌ No se pudo encontrar dirección para este Eircode');
        await dotnetReference.invokeMethodAsync('OnAddressError', 
            'No se encontró dirección. Por favor ingresa la dirección manualmente.'
        );
        
    } catch (error) {
        console.error('❌ Error buscando dirección:', error);
        await dotnetReference.invokeMethodAsync('OnAddressError', 
            'Error al buscar dirección: ' + error.message
        );
    }
};

/**
 * Búsqueda con Google Maps Geocoding API (MÉTODO PRINCIPAL)
 */
async function searchWithGoogleMaps(eircode, dotnetReference) {
    return new Promise((resolve) => {
        try {
            const geocoder = new google.maps.Geocoder();
            
            console.log('🔍 Google Maps: Geocodificando Eircode:', eircode);
            
            geocoder.geocode({ 
                address: eircode,
                componentRestrictions: {
                    country: 'IE'  // Forzar Irlanda
                }
            }, async (results, status) => {
                console.log('📦 Google Maps Status:', status);
                console.log('📦 Google Maps Results:', results);
                
                if (status === 'OK' && results && results.length > 0) {
                    const result = results[0];
                    const location = result.geometry.location;
                    
                    let street = '';
                    let city = 'Drogheda';
                    let county = 'County Louth';
                    
                    // Extraer componentes de dirección
                    for (const component of result.address_components) {
                        const types = component.types;
                        
                        if (types.includes('route')) {
                            street = component.long_name;
                        } else if (types.includes('street_number')) {
                            street = component.long_name + ' ' + street;
                        } else if (types.includes('sublocality') || types.includes('neighborhood')) {
                            if (!street) street = component.long_name;
                        } else if (types.includes('locality')) {
                            city = component.long_name;
                        } else if (types.includes('postal_town')) {
                            if (!city || city === 'Drogheda') city = component.long_name;
                        } else if (types.includes('administrative_area_level_1')) {
                            county = component.long_name;
                        } else if (types.includes('administrative_area_level_2')) {
                            if (!county || county === 'County Louth') county = component.long_name;
                        }
                    }
                    
                    // Si no hay calle específica, usar la primera parte de formatted_address
                    if (!street || street.trim() === '') {
                        const parts = result.formatted_address.split(',');
                        if (parts.length > 0) {
                            street = parts[0].trim();
                            // Evitar que la calle sea igual a la ciudad
                            if (street === city) {
                                street = parts.length > 1 ? parts[1].trim() : street;
                            }
                        }
                    }
                    
                    const lat = location.lat();
                    const lon = location.lng();
                    
                    console.log('✅ Google Maps - Dirección encontrada:', {
                        address: street,
                        city: city,
                        county: county,
                        country: 'Ireland',
                        lat: lat,
                        lon: lon,
                        formatted_address: result.formatted_address
                    });
                    
                    await dotnetReference.invokeMethodAsync('OnAddressFound',
                        street,
                        city,
                        lat,
                        lon
                    );
                    
                    resolve();
                } else {
                    console.error('❌ Google Maps Geocoding falló:', status);
                    
                    let errorMessage = 'No se encontró dirección para este Eircode';
                    
                    if (status === 'ZERO_RESULTS') {
                        errorMessage = 'Eircode no encontrado. Verifica que sea correcto.';
                    } else if (status === 'REQUEST_DENIED') {
                        errorMessage = 'API Key inválida o sin permisos. Verifica tu configuración de Google Maps.';
                    } else if (status === 'OVER_QUERY_LIMIT') {
                        errorMessage = 'Límite de consultas excedido. Intenta más tarde.';
                    }
                    
                    await dotnetReference.invokeMethodAsync('OnAddressError', errorMessage);
                    resolve();
                }
            });
        } catch (error) {
            console.error('❌ Error en Google Maps:', error);
            dotnetReference.invokeMethodAsync('OnAddressError',
                'Error al buscar dirección: ' + error.message
            );
            resolve();
        }
    });
}

/**
 * Validar que sea un Eircode irlandés válido
 */
function isValidIrishEircode(eircode) {
    // Formato irlandés: A65F4E2 (letra + 2 dígitos + 4 alfanuméricos)
    const pattern = /^[A-Z]\d{2}[A-Z0-9]{4}$/;
    return pattern.test(eircode);
}

/**
 * Mapa de prefijos de Eircode a ciudades irlandesas
 * Solo usado como último recurso si Google Maps falla
 */
function getIrishEircodeCity(eircode) {
    const prefix = eircode.substring(0, 3);
    
    const eircodeMap = {
        // Drogheda - County Louth
        'A92': { city: 'Drogheda', area: 'Drogheda', lat: 53.7134, lon: -6.3488 },
        
        // Dundalk - County Louth
        'A91': { city: 'Dundalk', area: 'Dundalk', lat: 54.0008, lon: -6.4058 },
        
        // Dublin
        'D01': { city: 'Dublin', area: 'Dublin 1', lat: 53.3498, lon: -6.2603 },
        'D02': { city: 'Dublin', area: 'Dublin 2', lat: 53.3382, lon: -6.2591 },
        
        // Cork
        'T12': { city: 'Cork', area: 'Cork City', lat: 51.8985, lon: -8.4756 },
        'T23': { city: 'Cork', area: 'Cork City', lat: 51.8985, lon: -8.4756 },
        
        // Galway
        'H91': { city: 'Galway', area: 'Galway City', lat: 53.2707, lon: -9.0568 },
        
        // Limerick
        'V94': { city: 'Limerick', area: 'Limerick City', lat: 52.6638, lon: -8.6267 },
        
        // Waterford
        'X91': { city: 'Waterford', area: 'Waterford City', lat: 52.2593, lon: -7.1101 }
    };
    
    return eircodeMap[prefix] || null;
}

console.log('✅ Eircode Search API cargada');
console.log('🗺️ Google Maps API: ' + (typeof google !== 'undefined' ? 'Disponible ✅' : 'No disponible ❌'));