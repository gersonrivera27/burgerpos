using System.Text.Json.Serialization;

namespace BurgerPOS.Models;

// ==================== CATEGORY ====================
public class Category
{
    [JsonPropertyName("id")]
    public int Id { get; set; }

    [JsonPropertyName("name")]
    public string Name { get; set; } = "";

    [JsonPropertyName("description")]
    public string? Description { get; set; }

    [JsonPropertyName("created_at")]
    public DateTime CreatedAt { get; set; }
}

// ==================== CUSTOMER ====================
public class Customer
{
    [JsonPropertyName("id")]
    public int Id { get; set; }
    
    [JsonPropertyName("phone")]
    public string Phone { get; set; } = "";
    
    [JsonPropertyName("name")]
    public string Name { get; set; } = "";
    
    [JsonPropertyName("email")]
    public string? Email { get; set; }
    
    [JsonPropertyName("address_line1")]
    public string? AddressLine1 { get; set; }
    
    [JsonPropertyName("address_line2")]
    public string? AddressLine2 { get; set; }
    
    [JsonPropertyName("city")]
    public string City { get; set; } = "Drogheda";
    
    [JsonPropertyName("county")]
    public string County { get; set; } = "Louth";
    
    [JsonPropertyName("eircode")]
    public string? Eircode { get; set; }
    
    [JsonPropertyName("country")]
    public string Country { get; set; } = "Ireland";
    
    [JsonPropertyName("latitude")]
    public double? Latitude { get; set; }
    
    [JsonPropertyName("longitude")]
    public double? Longitude { get; set; }
    
    [JsonPropertyName("notes")]
    public string? Notes { get; set; }
    
    [JsonPropertyName("is_active")]
    public bool IsActive { get; set; } = true;
    
    [JsonPropertyName("total_orders")]
    public int TotalOrders { get; set; }
    
    [JsonPropertyName("total_spent")]
    public decimal TotalSpent { get; set; }
    
    [JsonPropertyName("created_at")]
    public DateTime CreatedAt { get; set; }
}

public class CustomerCreate
{
    [JsonPropertyName("phone")]
    public string Phone { get; set; } = "";
    
    [JsonPropertyName("name")]
    public string Name { get; set; } = "";
    
    [JsonPropertyName("email")]
    public string? Email { get; set; }
    
    [JsonPropertyName("address_line1")]
    public string? AddressLine1 { get; set; }
    
    [JsonPropertyName("address_line2")]
    public string? AddressLine2 { get; set; }
    
    [JsonPropertyName("city")]
    public string City { get; set; } = "Drogheda";
    
    [JsonPropertyName("county")]
    public string County { get; set; } = "Louth";
    
    [JsonPropertyName("eircode")]
    public string? Eircode { get; set; }
    
    [JsonPropertyName("country")]
    public string Country { get; set; } = "Ireland";
    
    [JsonPropertyName("latitude")]
    public double? Latitude { get; set; }
    
    [JsonPropertyName("longitude")]
    public double? Longitude { get; set; }
    
    [JsonPropertyName("notes")]
    public string? Notes { get; set; }
}

public class CustomerSearchResponse
{
    [JsonPropertyName("found")]
    public bool Found { get; set; }
    
    [JsonPropertyName("customer")]
    public Customer? Customer { get; set; }
}

// ==================== PRODUCT ====================
public class Product
{
    [JsonPropertyName("id")]
    public int Id { get; set; }

    [JsonPropertyName("category_id")]
    public int CategoryId { get; set; }

    [JsonPropertyName("name")]
    public string Name { get; set; } = "";

    [JsonPropertyName("description")]
    public string? Description { get; set; }

    [JsonPropertyName("price")]
    public decimal Price { get; set; }

    [JsonPropertyName("image_url")]
    public string? ImageUrl { get; set; }

    [JsonPropertyName("is_available")]
    public bool IsAvailable { get; set; } = true;

    [JsonPropertyName("created_at")]
    public DateTime CreatedAt { get; set; }
}

// ==================== ORDER ====================
public class Order
{
    [JsonPropertyName("id")]
    public int Id { get; set; }
    
    [JsonPropertyName("order_number")]
    public string OrderNumber { get; set; } = "";
    
    [JsonPropertyName("customer_name")]
    public string? CustomerName { get; set; }
    
    [JsonPropertyName("order_type")]
    public string OrderType { get; set; } = "dine-in";
    
    [JsonPropertyName("status")]
    public string Status { get; set; } = "pending";
    
    [JsonPropertyName("subtotal")]
    public decimal Subtotal { get; set; }
    
    [JsonPropertyName("tax")]
    public decimal Tax { get; set; }
    
    [JsonPropertyName("total")]
    public decimal Total { get; set; }
    
    [JsonPropertyName("payment_method")]
    public string? PaymentMethod { get; set; }
    
    [JsonPropertyName("created_at")]
    public DateTime CreatedAt { get; set; }
}

// ==================== HEALTH CHECK ====================
public class HealthResponse
{
    [JsonPropertyName("status")]
    public string Status { get; set; } = "";
    
    [JsonPropertyName("timestamp")]
    public DateTime Timestamp { get; set; }
}
