using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using System.Text.Json;

namespace Dossier.Api.Middleware {
    public static class ExceptionMiddlewareExtensions {
        // Extension method on IApplicationBuilder to configure existing UseExceptionHandler middleware
        // To process unhandled exceptions by logging etc.
        public static void ConfigureExceptionHandler(this IApplicationBuilder app, ILogger logger) {
            // Adding inbuilt exception handler to middleware pipeline, but configuring it
            app.UseExceptionHandler(errorApp => {
                errorApp.Run(async context => {
                    context.Response.StatusCode = 500;
                    context.Response.ContentType = "application/json";

                    var exceptionHandlerPathFeature = context.Features.Get<IExceptionHandlerFeature>();
                    var error = exceptionHandlerPathFeature.Error;

                    var errorObj = new {Error = "Internal Server Error", Message = error.Message};
                    var jsonErrorObj = JsonSerializer.Serialize(errorObj);

                    // TODO log error
                    logger.LogInformation("THIS IS A TEST");

                    await context.Response.WriteAsync(jsonErrorObj);
                });
            });
        }
    }
}