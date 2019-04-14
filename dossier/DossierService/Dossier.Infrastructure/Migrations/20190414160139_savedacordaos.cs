using Microsoft.EntityFrameworkCore.Migrations;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;

namespace Dossier.Infrastructure.Migrations
{
    public partial class savedacordaos : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Comments_Acordao_AcordaoId",
                table: "Comments");

            migrationBuilder.DropTable(
                name: "Acordao");

            migrationBuilder.RenameColumn(
                name: "AcordaoId",
                table: "Comments",
                newName: "SavedAcordaoId");

            migrationBuilder.RenameIndex(
                name: "IX_Comments_AcordaoId",
                table: "Comments",
                newName: "IX_Comments_SavedAcordaoId");

            migrationBuilder.CreateTable(
                name: "SavedAcordao",
                columns: table => new
                {
                    Id = table.Column<int>(nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.SerialColumn),
                    OriginalAcordaoId = table.Column<int>(nullable: false),
                    FolderId = table.Column<int>(nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_SavedAcordao", x => x.Id);
                    table.ForeignKey(
                        name: "FK_SavedAcordao_Folders_FolderId",
                        column: x => x.FolderId,
                        principalTable: "Folders",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateIndex(
                name: "IX_SavedAcordao_FolderId",
                table: "SavedAcordao",
                column: "FolderId");

            migrationBuilder.AddForeignKey(
                name: "FK_Comments_SavedAcordao_SavedAcordaoId",
                table: "Comments",
                column: "SavedAcordaoId",
                principalTable: "SavedAcordao",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Comments_SavedAcordao_SavedAcordaoId",
                table: "Comments");

            migrationBuilder.DropTable(
                name: "SavedAcordao");

            migrationBuilder.RenameColumn(
                name: "SavedAcordaoId",
                table: "Comments",
                newName: "AcordaoId");

            migrationBuilder.RenameIndex(
                name: "IX_Comments_SavedAcordaoId",
                table: "Comments",
                newName: "IX_Comments_AcordaoId");

            migrationBuilder.CreateTable(
                name: "Acordao",
                columns: table => new
                {
                    Id = table.Column<int>(nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.SerialColumn),
                    FolderId = table.Column<int>(nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Acordao", x => x.Id);
                    table.ForeignKey(
                        name: "FK_Acordao_Folders_FolderId",
                        column: x => x.FolderId,
                        principalTable: "Folders",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Acordao_FolderId",
                table: "Acordao",
                column: "FolderId");

            migrationBuilder.AddForeignKey(
                name: "FK_Comments_Acordao_AcordaoId",
                table: "Comments",
                column: "AcordaoId",
                principalTable: "Acordao",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }
    }
}
