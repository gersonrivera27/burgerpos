using BurgerPOS.Components;
using BurgerPOS.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

// Configurar HttpClient para API
var apiUrl = Environment.GetEnvironmentVariable("API_URL") ?? "http://burger-backend:8000";
Console.WriteLine($"🔗 Configurando API URL: {apiUrl}");

builder.Services.AddHttpClient<PosApiService>(client =>
{
    client.BaseAddress = new Uri(apiUrl);
    client.Timeout = TimeSpan.FromSeconds(30);
});

var app = builder.Build();

// Configure the HTTP request pipeline
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseStaticFiles();
app.UseAntiforgery();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

Console.WriteLine("✅ BurgerPOS Frontend iniciado correctamente");

app.Run();
