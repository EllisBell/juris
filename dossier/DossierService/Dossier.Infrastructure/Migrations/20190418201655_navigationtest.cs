using Microsoft.EntityFrameworkCore.Migrations;

namespace Dossier.Infrastructure.Migrations
{
    public partial class navigationtest : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_SavedAcordaos_Folders_FolderId",
                table: "SavedAcordaos");

            migrationBuilder.RenameColumn(
                name: "FolderId",
                table: "SavedAcordaos",
                newName: "folderId");

            migrationBuilder.RenameIndex(
                name: "IX_SavedAcordaos_FolderId",
                table: "SavedAcordaos",
                newName: "IX_SavedAcordaos_folderId");

            migrationBuilder.AddForeignKey(
                name: "FK_SavedAcordaos_Folders_folderId",
                table: "SavedAcordaos",
                column: "folderId",
                principalTable: "Folders",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_SavedAcordaos_Folders_folderId",
                table: "SavedAcordaos");

            migrationBuilder.RenameColumn(
                name: "folderId",
                table: "SavedAcordaos",
                newName: "FolderId");

            migrationBuilder.RenameIndex(
                name: "IX_SavedAcordaos_folderId",
                table: "SavedAcordaos",
                newName: "IX_SavedAcordaos_FolderId");

            migrationBuilder.AddForeignKey(
                name: "FK_SavedAcordaos_Folders_FolderId",
                table: "SavedAcordaos",
                column: "FolderId",
                principalTable: "Folders",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }
    }
}
