using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using Dossier.Core.Entities;
using Dossier.Infrastructure.ConfigSettings;

namespace Dossier.Infrastructure.Data {
    public class DossierContext : DbContext {

        private readonly IRepoConfig _repoConfig;
        public DossierContext(IRepoConfig repoConfig) {
            _repoConfig = repoConfig;
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
            => optionsBuilder.UseNpgsql(_repoConfig.DossierConnString);

        protected override void OnModelCreating(ModelBuilder modelBuilder) {
            modelBuilder.Entity<Folder>()
                .Property(p => p.Id)
                .ValueGeneratedOnAdd();

            modelBuilder.Entity<SavedAcordao>()
                .Property(p => p.Id)
                .ValueGeneratedOnAdd();

            modelBuilder.Entity<Comment>()
                .Property(p => p.Id)
                .ValueGeneratedOnAdd();
        }

        public DbSet<Folder> Folders {get; set;}
        public DbSet<SavedAcordao> SavedAcordaos {get; set;}
        public DbSet<Comment> Comments {get; set;}
    }
}