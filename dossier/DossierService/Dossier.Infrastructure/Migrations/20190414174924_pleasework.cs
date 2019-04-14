using Microsoft.EntityFrameworkCore.Migrations;

namespace Dossier.Infrastructure.Migrations
{
    public partial class pleasework : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Comments_SavedAcordao_SavedAcordaoId",
                table: "Comments");

            migrationBuilder.DropForeignKey(
                name: "FK_SavedAcordao_Folders_FolderId",
                table: "SavedAcordao");

            migrationBuilder.DropPrimaryKey(
                name: "PK_SavedAcordao",
                table: "SavedAcordao");

            migrationBuilder.RenameTable(
                name: "SavedAcordao",
                newName: "SavedAcordaos");

            migrationBuilder.RenameIndex(
                name: "IX_SavedAcordao_FolderId",
                table: "SavedAcordaos",
                newName: "IX_SavedAcordaos_FolderId");

            migrationBuilder.AddPrimaryKey(
                name: "PK_SavedAcordaos",
                table: "SavedAcordaos",
                column: "Id");

            migrationBuilder.AddForeignKey(
                name: "FK_Comments_SavedAcordaos_SavedAcordaoId",
                table: "Comments",
                column: "SavedAcordaoId",
                principalTable: "SavedAcordaos",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);

            migrationBuilder.AddForeignKey(
                name: "FK_SavedAcordaos_Folders_FolderId",
                table: "SavedAcordaos",
                column: "FolderId",
                principalTable: "Folders",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Comments_SavedAcordaos_SavedAcordaoId",
                table: "Comments");

            migrationBuilder.DropForeignKey(
                name: "FK_SavedAcordaos_Folders_FolderId",
                table: "SavedAcordaos");

            migrationBuilder.DropPrimaryKey(
                name: "PK_SavedAcordaos",
                table: "SavedAcordaos");

            migrationBuilder.RenameTable(
                name: "SavedAcordaos",
                newName: "SavedAcordao");

            migrationBuilder.RenameIndex(
                name: "IX_SavedAcordaos_FolderId",
                table: "SavedAcordao",
                newName: "IX_SavedAcordao_FolderId");

            migrationBuilder.AddPrimaryKey(
                name: "PK_SavedAcordao",
                table: "SavedAcordao",
                column: "Id");

            migrationBuilder.AddForeignKey(
                name: "FK_Comments_SavedAcordao_SavedAcordaoId",
                table: "Comments",
                column: "SavedAcordaoId",
                principalTable: "SavedAcordao",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);

            migrationBuilder.AddForeignKey(
                name: "FK_SavedAcordao_Folders_FolderId",
                table: "SavedAcordao",
                column: "FolderId",
                principalTable: "Folders",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }
    }
}
