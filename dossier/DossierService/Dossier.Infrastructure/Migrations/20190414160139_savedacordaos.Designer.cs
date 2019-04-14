﻿// <auto-generated />
using System;
using Dossier.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;

namespace Dossier.Infrastructure.Migrations
{
    [DbContext(typeof(DossierContext))]
    [Migration("20190414160139_savedacordaos")]
    partial class savedacordaos
    {
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.SerialColumn)
                .HasAnnotation("ProductVersion", "2.2.2-servicing-10034")
                .HasAnnotation("Relational:MaxIdentifierLength", 63);

            modelBuilder.Entity("Dossier.Core.Entities.Comment", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd();

                    b.Property<string>("Author");

                    b.Property<int?>("SavedAcordaoId");

                    b.Property<string>("Text");

                    b.Property<DateTime>("date");

                    b.HasKey("Id");

                    b.HasIndex("SavedAcordaoId");

                    b.ToTable("Comments");
                });

            modelBuilder.Entity("Dossier.Core.Entities.Folder", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd();

                    b.Property<string>("Name");

                    b.HasKey("Id");

                    b.ToTable("Folders");
                });

            modelBuilder.Entity("Dossier.Core.Entities.SavedAcordao", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd();

                    b.Property<int?>("FolderId");

                    b.Property<int>("OriginalAcordaoId");

                    b.HasKey("Id");

                    b.HasIndex("FolderId");

                    b.ToTable("SavedAcordao");
                });

            modelBuilder.Entity("Dossier.Core.Entities.Comment", b =>
                {
                    b.HasOne("Dossier.Core.Entities.SavedAcordao")
                        .WithMany("Comments")
                        .HasForeignKey("SavedAcordaoId");
                });

            modelBuilder.Entity("Dossier.Core.Entities.SavedAcordao", b =>
                {
                    b.HasOne("Dossier.Core.Entities.Folder")
                        .WithMany("Acordaos")
                        .HasForeignKey("FolderId");
                });
#pragma warning restore 612, 618
        }
    }
}
