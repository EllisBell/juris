using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Dossier.Core.Entities;
using Dossier.Core.Interfaces;
using Dossier.Infrastructure.Data;
using Dossier.Infrastructure.ConfigSettings;
using Dossier.Api.ConfigSettings;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.HttpsPolicy;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Microsoft.EntityFrameworkCore;

namespace Dossier.Api
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_2_2);
            services.AddOptions();

            // Link config section in appsettings.json to RepoConfig type
            services.Configure<RepoConfig>(Configuration.GetSection("ConnectionStrings"));

            // Instead of injecting IOptions into DbContext, inject an interface which is in Infra proj
            // Namely, inject the RepoConfig implementation which has the settings configured above
            services.AddScoped<IRepoConfig>(s =>
                    s.GetService<IOptions<RepoConfig>>().Value
            );

            services.AddDbContext<DossierContext>();
            // Providing "open generic types" for generic repository
            // https://stackoverflow.com/questions/33566075/
         //   services.AddScoped(typeof(IRepository<>), typeof(Repository<>)); 
            services.AddScoped<IDbService, DbService>();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
                app.UseHsts();
            }

            app.UseHttpsRedirection();
            app.UseMvc();
        }
    }
}
