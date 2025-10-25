using System.Net.Http.Json;
using BurgerPOS.Models;

namespace BurgerPOS.Services;

public class PosApiService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<PosApiService> _logger;

    public PosApiService(HttpClient httpClient, ILogger<PosApiService> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    // ==================== HEALTH CHECK ====================
    
    public async Task<bool> TestConnectionAsync()
    {
        try
        {
            var response = await _httpClient.GetAsync("/health");
            if (response.IsSuccessStatusCode)
            {
                var health = await response.Content.ReadFromJsonAsync<HealthResponse>();
                _logger.LogInformation("Backend conectado: {Status}", health?.Status);
                return true;
            }
            return false;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error conectando al backend");
            return false;
        }
    }

    // ==================== CUSTOMERS ====================
    
    public async Task<List<Customer>> GetCustomersAsync(string? search = null, int limit = 100)
    {
        try
        {
            var url = $"/api/customers?limit={limit}";
            if (!string.IsNullOrEmpty(search))
            {
                url += $"&search={Uri.EscapeDataString(search)}";
            }
            
            var customers = await _httpClient.GetFromJsonAsync<List<Customer>>(url);
            return customers ?? new List<Customer>();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error obteniendo clientes");
            return new List<Customer>();
        }
    }
    
    public async Task<CustomerSearchResponse?> SearchCustomerByPhoneAsync(string phone)
{
    try
    {
        _logger.LogInformation("Buscando cliente por teléfono: {Phone}", phone);
        
        var response = await _httpClient.GetAsync($"/api/customers/search-by-phone/{Uri.EscapeDataString(phone)}");
        
        if (response.IsSuccessStatusCode)
        {
            return await response.Content.ReadFromJsonAsync<CustomerSearchResponse>();
        }
        
        return null;
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error buscando cliente por teléfono");
        return null;
    }
}

    public async Task<List<Customer>?> SearchCustomersAsync(string query)
    {
        try
        {
            _logger.LogInformation("Buscando clientes con query: {Query}", query);

            var response = await _httpClient.GetAsync($"/api/customers?search={Uri.EscapeDataString(query)}&limit=10");

            if (response.IsSuccessStatusCode)
            {
                var customers = await response.Content.ReadFromJsonAsync<List<Customer>>();
                _logger.LogInformation("Encontrados {Count} clientes", customers?.Count ?? 0);
                return customers;
            }
            else
            {
                _logger.LogWarning("Error buscando clientes: {StatusCode}", response.StatusCode);
                return new List<Customer>();
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Excepción buscando clientes");
            return new List<Customer>();
        }
    }

    public async Task<Customer?> CreateCustomerAsync(CustomerCreate customer)
    {
        try
        {
            var response = await _httpClient.PostAsJsonAsync("/api/customers", customer);
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadFromJsonAsync<Customer>();
            }
            return null;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creando cliente");
            return null;
        }
    }



    public async Task<Customer?> UpdateCustomerAsync(int customerId, CustomerCreate customer)
    {
        try
        {
            var response = await _httpClient.PutAsJsonAsync($"/api/customers/{customerId}", customer);
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadFromJsonAsync<Customer>();
            }
            return null;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error actualizando cliente");
            return null;
        }
    }
    
    

    // ==================== PRODUCTS ====================

    public async Task<List<Product>> GetProductsAsync(int? categoryId = null)
    {
        try
        {
            var url = "/api/products?available_only=true";
            if (categoryId.HasValue)
            {
                url += $"&category_id={categoryId.Value}";
            }

            var products = await _httpClient.GetFromJsonAsync<List<Product>>(url);
            return products ?? new List<Product>();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error obteniendo productos");
            return new List<Product>();
        }
    }

    // ==================== ORDERS ====================
    
    public async Task<List<Order>> GetOrdersAsync(string? status = null, int limit = 100)
    {
        try
        {
            var url = $"/api/orders?limit={limit}";
            if (!string.IsNullOrEmpty(status))
            {
                url += $"&status={status}";
            }
            
            var orders = await _httpClient.GetFromJsonAsync<List<Order>>(url);
            return orders ?? new List<Order>();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error obteniendo órdenes");
            return new List<Order>();
        }
    }

    // ==================== CATEGORIES ====================
    
    public async Task<List<Category>> GetCategoriesAsync()
    {
        try
        {
            var categories = await _httpClient.GetFromJsonAsync<List<Category>>("/api/categories");
            return categories ?? new List<Category>();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error obteniendo categorías");
            return new List<Category>();
        }
    }
}
