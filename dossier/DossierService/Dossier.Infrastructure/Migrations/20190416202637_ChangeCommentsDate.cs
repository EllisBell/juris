using Microsoft.EntityFrameworkCore.Migrations;

namespace Dossier.Infrastructure.Migrations
{
    public partial class ChangeCommentsDate : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "date",
                table: "Comments",
                newName: "Date");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "Date",
                table: "Comments",
                newName: "date");
        }
    }
}
