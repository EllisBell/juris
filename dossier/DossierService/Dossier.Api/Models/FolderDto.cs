using System.Collections.Generic;
using System.Linq;
using Dossier.Core.Entities;

namespace Dossier.Api.Models {
    public class FolderDto {
        
        public int Id {get; set;}
        public string Name {get; set;}
        public IEnumerable<int> Acordaos {get; set;}

        public static FolderDto FromEntity(Folder f) => new FolderDto() 
        {
            Id = f.Id,
            Name = f.Name,
            Acordaos = f.SavedAcordaos.Select(sa => sa.Id)
        };
    }
}