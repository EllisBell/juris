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
    [Migration("20190414121144_test2")]
    partial class test2
    {
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.SerialColumn)
                .HasAnnotation("ProductVersion", "2.2.2-servicing-10034")
                .HasAnnotation("Relational:MaxIdentifierLength", 63);

            modelBuilder.Entity("Dossier.Core.Entities.Acordao", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd();

                    b.Property<int?>("FolderId");

                    b.HasKey("Id");

                    b.HasIndex("FolderId");

                    b.ToTable("Acordao");
                });

            modelBuilder.Entity("Dossier.Core.Entities.Comment", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd();

                    b.Property<int?>("AcordaoId");

                    b.Property<string>("Author");

                    b.Property<string>("Text");

                    b.Property<DateTime>("date");

                    b.HasKey("Id");

                    b.HasIndex("AcordaoId");

                    b.ToTable("Comment");
                });

            modelBuilder.Entity("Dossier.Core.Entities.Folder", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd();

                    b.Property<string>("Name");

                    b.HasKey("Id");

                    b.ToTable("Folders");
                });

            modelBuilder.Entity("Dossier.Core.Entities.Acordao", b =>
                {
                    b.HasOne("Dossier.Core.Entities.Folder")
                        .WithMany("Acordaos")
                        .HasForeignKey("FolderId");
                });

            modelBuilder.Entity("Dossier.Core.Entities.Comment", b =>
                {
                    b.HasOne("Dossier.Core.Entities.Acordao")
                        .WithMany("Comments")
                        .HasForeignKey("AcordaoId");
                });
#pragma warning restore 612, 618
        }
    }
}
