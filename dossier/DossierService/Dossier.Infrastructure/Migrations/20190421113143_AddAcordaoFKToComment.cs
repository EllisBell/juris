using Microsoft.EntityFrameworkCore.Migrations;

namespace Dossier.Infrastructure.Migrations
{
    public partial class AddAcordaoFKToComment : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Comments_SavedAcordaos_SavedAcordaoId",
                table: "Comments");

            migrationBuilder.RenameColumn(
                name: "SavedAcordaoId",
                table: "Comments",
                newName: "AcordaoId");

            migrationBuilder.RenameIndex(
                name: "IX_Comments_SavedAcordaoId",
                table: "Comments",
                newName: "IX_Comments_AcordaoId");

            migrationBuilder.AddForeignKey(
                name: "FK_Comments_SavedAcordaos_AcordaoId",
                table: "Comments",
                column: "AcordaoId",
                principalTable: "SavedAcordaos",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Comments_SavedAcordaos_AcordaoId",
                table: "Comments");

            migrationBuilder.RenameColumn(
                name: "AcordaoId",
                table: "Comments",
                newName: "SavedAcordaoId");

            migrationBuilder.RenameIndex(
                name: "IX_Comments_AcordaoId",
                table: "Comments",
                newName: "IX_Comments_SavedAcordaoId");

            migrationBuilder.AddForeignKey(
                name: "FK_Comments_SavedAcordaos_SavedAcordaoId",
                table: "Comments",
                column: "SavedAcordaoId",
                principalTable: "SavedAcordaos",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }
    }
}
