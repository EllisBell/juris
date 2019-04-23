using System.Collections.Generic;
using System.Linq;
using Dossier.Core.Entities;
using System.ComponentModel.DataAnnotations;

namespace Dossier.Api.Models {
    public class FolderDto {
        
        //[Range(1, int.MaxValue)]
        public int Id {get; set;}

        [Required]
        [StringLength(30)]
        public string Name {get; set;}

        public static FolderDto FromEntity(Folder f) => new FolderDto() 
        {
            Id = f.Id,
            Name = f.Name,
        };
    }
}